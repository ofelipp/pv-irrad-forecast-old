"""
Module which objective is concat every variable create on model dataset
for training the model.
"""

from config import project_paths, log
from data.io import json_to_dict
from logging import debug
import numpy as np
import pandas as pd
import re
from unidecode import unidecode

log()

PATH = project_paths()
MTR_VARS_RANGES = "".join(
    [
        PATH["ROOT"],
        PATH["DATA"]["STATIC"],
        "metereological_variable_ranges.json",
    ]
)


def rain_instant(rain_cum: pd.Series) -> np.array:

    return rain_cum.fillna(0) - rain_cum.shift(1).fillna(0)


def station(filepath: str) -> str:

    """Station name from file name"""

    station_name = re.findall(r"\b\w+?(?=_\d)", filepath)[0]
    station_name = re.sub(r"^\_+", "", station_name)

    return unidecode(station_name)


def season(datetime_series: pd.Series) -> np.ndarray:
    """
    Create Season variable using datetime column from pandas DataFrame

    Args:
        model_data = pd.DataFrame : containing datetime col
        datetime_col = str : datetime column name which the process of creation
                       will use.

    """

    # Create function dataframe
    datetime_col = str(datetime_series.name)
    df_season = pd.DataFrame({datetime_col: datetime_series})
    df_season[datetime_col] = pd.to_datetime(df_season[datetime_col])
    df_season[datetime_col] = df_season[datetime_col].dt.normalize()

    # Auxiliar columns
    df_season["Season"] = None
    df_season["Year"] = df_season[datetime_col].dt.strftime("%Y")

    # Filling df_season with season info
    for name, period in json_to_dict(MTR_VARS_RANGES)["seasons"].items():
        debug(name, period)

        # Creating series with season start date
        df_season[name + "_start"] = pd.to_datetime(
            df_season["Year"] + "-" + period["start"]
        )

        # Creating series with season ending date
        df_season[name + "_end"] = pd.to_datetime(
            df_season["Year"] + "-" + period["end"]
        )

        # Condition
        _starting = df_season[datetime_col] >= df_season[name + "_start"]
        _ending = df_season[datetime_col] <= df_season[name + "_end"]

        # Category
        df_season.loc[_starting & _ending, "Season"] = name[:6]

        # Drop aux seasons columns
        _drop_cols = [name + "_start", name + "_end"]
        df_season.drop(columns=_drop_cols, inplace=True)

    return df_season["Season"].values


def var_range(variable: str = None) -> pd.DataFrame:

    """Dataframe containing variable's choosed range"""

    if variable is None:
        return json_to_dict(MTR_VARS_RANGES)
    else:
        return pd.DataFrame(json_to_dict(MTR_VARS_RANGES)[variable]).transpose()


def possible_range(model_data: pd.DataFrame, var_col: str) -> np.array:

    """
    Variable values evaluated in a designed range
    """

    debug(f"{var_col}")

    # Reading values from json file
    df_var_range = var_range(var_col)

    # Merging with original dataframe
    df_var = pd.merge(
        left=model_data[["Season", var_col]],
        right=df_var_range,
        left_on="Season",
        right_index=True,
        how="left",
    )

    # Conditions to exclude values
    _below = df_var[var_col] < df_var["min"]
    _above = df_var[var_col] > df_var["max"]

    debug(f"Cases Below: {_below.sum()} | Cases Above: {_above.sum()}")

    return np.where(_below | _above, np.nan, df_var[var_col])


def datetime_variables(
    series_datetime: pd.Series, datetime_format: str = "%Y-%m-%d %H:%M:%S"
) -> pd.DataFrame():

    """
    Receive a Series with Datetime values and returns a DataFrame containing
    Year, Month, Day, Hour and Minute variables.
    """

    # Standarlize Datetime format
    series_datetime = pd.to_datetime(series_datetime, format=datetime_format)

    df_datetime = pd.DataFrame()
    int_vars = []

    # Date variables
    df_datetime["Date"] = pd.to_datetime(series_datetime).dt.normalize()
    df_datetime["Year"] = series_datetime.dt.strftime("%Y")
    df_datetime["Month"] = series_datetime.dt.strftime("%m")
    df_datetime["Day"] = series_datetime.dt.strftime("%d")
    int_vars += ["Year", "Month", "Day"]

    # Time variables
    df_datetime["Hour"] = series_datetime.dt.strftime("%H")
    df_datetime["Real_Minute"] = series_datetime.dt.strftime("%M")
    df_datetime["Minute"] = (
        pd.to_numeric(df_datetime["Real_Minute"]) // 15
    ) * 15
    int_vars += ["Hour", "Real_Minute", "Minute"]

    # Transforming into integers
    for col in int_vars:
        df_datetime[col] = df_datetime[col].astype(int)

    return df_datetime


def calendar_variables(
    series_datetime: pd.Series, datetime_format="%Y-%m-%d"
) -> pd.DataFrame():

    """
    Based on a Datetime serie create calendar variables indicating if there
    is a national or regional holiday, week day, year day, etc..
    """

    # Standarlize Datetime format
    series_datetime = pd.to_datetime(series_datetime, format=datetime_format)

    df_datetime = pd.DataFrame()
    int_vars = []

    # Week
    df_datetime["WeekDay"] = series_datetime.dt.strftime("%w")
    # df_datetime["WeekMonth"] = None # TODO
    df_datetime["WeekYear"] = series_datetime.dt.strftime("%U")
    int_vars += ["WeekDay", "WeekYear"]

    # Year variable
    df_datetime["YearDay"] = series_datetime.dt.strftime("%j")
    int_vars += ["YearDay"]

    # Transforming into integers
    for col in int_vars:
        df_datetime[col] = df_datetime[col].astype(int)

    return df_datetime

"""
Module which objective is concat every variable create on model dataset
for training the model.
"""

from config import project_paths
from data.io import json_to_dict
import datetime
import ephem
from logging import debug, info
import numpy as np
import pandas as pd
import re
from unidecode import unidecode


PATH = project_paths()
MTR_VARS_RANGES = "".join([
    PATH["ROOT"], PATH["DATA"]["STATIC"], "metereological_variable_ranges.json"
])


def station(filepath: str) -> str:

    """ Station name from file name """

    station_name = re.findall(r"\b\w+?(?=_\d)", filepath)[0]
    station_name = re.sub(r"^\_+", "", station_name)

    return unidecode(station_name)


def season(model_datetime_data: pd.Series) -> np.ndarray:
    """
    Create Season variable using datetime column from pandas DataFrame

    Args:
        model_data = pd.DataFrame : containing datetime col
        datetime_col = str : datetime column name which the process of creation
                       will use.

    """

    # Create function dataframe
    datetime_col = str(model_datetime_data.name)
    df_season = pd.DataFrame({datetime_col: model_datetime_data})
    df_season[datetime_col] = df_season[datetime_col].dt.normalize()

    # Auxiliar columns
    df_season["Season"] = None
    df_season["Year"] = df_season[datetime_col].dt.strftime("%Y")

    # Filling df_season with season info
    for name, period in json_to_dict(MTR_VARS_RANGES)["seasons"].items():
        print(name, period)

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


def var_range(variable: str) -> pd.DataFrame:

    """Dataframe containing variable's choosed range"""

    return pd.DataFrame(
        json_to_dict(MTR_VARS_RANGES)[variable]
    ).transpose()


def possible_range(model_data: pd.DataFrame, var_col: str) -> np.array:

    """
    Variable values evaluated in a designed range
    """

    print(f"{var_col}")

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

    print(f"Cases Below: {_below.sum()} | Cases Above: {_above.sum()}")

    return np.where(_below | _above, np.nan, df_var[var_col])


def datetime_variables(
    series_datetime: pd.Series,
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
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
    df_datetime["Minute"] = (df_datetime["Real_Minute"] // 15) * 15
    int_vars += ["Hour", "Real_Minute", "Minute"]

    # Transforming into integers
    for col in int_vars:
        df_datetime[col] = df_datetime[col].astype(int)

    return df_datetime


def calendar_variables(series_datetime: pd.Series) -> pd.DataFrame():

    """
    Based on a Datetime serie create calendar variables indicating if there
    is a national or regional holiday, week day, year day, etc..
    """

    # Standarlize Datetime format
    series_datetime = pd.to_datetime(series_datetime, format=datetime_format)

    df_datetime = pd.DataFrame()
    int_vars = []

    # Week
    df_datetime["WeekDay"] = series_datetime.dt.dayofweek()
    # df_datetime["WeekMonth"] = None # TODO
    df_datetime["WeekYear"] = series_datetime.dt.isocalendar().week
    int_vars += ["WeekDay", "WeekMonth", "WeekYear"]

    # Year variable
    df_datetime["YearDay"] = series_datetime.dt.dayofyear()
    int_vars += ["YearDay"]

    # Transforming into integers
    for col in int_vars:
        df_datetime[col] = df_datetime[col].astype(int)

    return df_datetime


def easter_date(start_period: str, end_period: str) -> pd.Series():

    """ Calculates the Easter date between a period of datetimes """

    EQUINOX = ['03-21']

    def next_full_moon_datetime(date: str) -> pd.Series():

        """ Receive datetime and retrieves the next full moon datetime """

        date_tuple = ephem.next_full_moon(date).tuple()

        return pd.to_datetime(
            datetime.datetime(
                year=date_tuple[0], month=date_tuple[1], day=date_tuple[2]
            )
        )

    # Serie containing period
    period = pd.DataFrame({
        "Datetime": pd.date_range(start_period, end_period)
    })

    # Equinox Dates
    years = list(period["Datetime"].dt.strftime("%Y").unique())

    equinox = []

    for year in years:
        equinox += [year + "-" + date for date in EQUINOX]

    equinox = pd.Series(equinox)

    # Next full moon after equinox
    next_full_moon = equinox.apply(
        lambda date: next_full_moon_datetime(date)
    )

    # First Sunday after Equinox with a full moon
    days_left_sunday = pd.to_timedelta(6 - next_full_moon.dt.weekday, 'day')

    return pd.Series(next_full_moon + days_left_sunday)


def carnival_date(easter_dates: pd.Series()) -> pd.Series:

    """
    Returns Carnival dates passing a serie of Easter dates

    Occurs 47 days before Easter, 40 days before Palm Sunday which occurs 7
    days before Easter.

    Carnival + 40 -> Palm Sunday
    Palm Sunday + 7 -> Easter

    """

    return pd.to_datetime(easter_dates) - pd.to_timedelta(47, 'day')


def ashes_wednesday(carnival_dates: pd.Series()) -> pd.Series:

    """
    Returns Ashes Wednesday dates passing a serie of Carnival dates

    Occurs a day after the carnival festival
    """

    return pd.to_datetime(carnival_dates) + pd.to_timedelta(1, 'day')


def saint_friday(easter_dates: pd.Series()) -> pd.Series:

    """
    Returns Saint Friday dates passing a serie of Easter dates

    Occurs in the friday before Easter
    """

    return pd.to_datetime(easter_dates) - pd.to_timedelta(2, 'day')
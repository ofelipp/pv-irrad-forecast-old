"""
Module which objective is concat every variable create on model dataset
for training the model.
"""

from .io import json_to_dict
import numpy as np
import pandas as pd

MTR_VARS_RANGES = "static/metereological_variable_ranges.json"


def var_range(variable: str) -> pd.DataFrame:

    """Dataframe containing variable's choosed range"""

    return pd.DataFrame(
        json_to_dict(MTR_VARS_RANGES)[variable]
    ).transpose()


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

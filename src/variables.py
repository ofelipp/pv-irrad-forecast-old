"""
Module which objective is concat every variable create on model dataset
for training the model.
"""

import json
import numpy as np
import pandas as pd

MTR_VARS_RANGES = "src/static/metereological_variable_ranges.json"


def read_meteorological_vars_range(json_path=MTR_VARS_RANGES) -> dict:

    """JSON file with variables ranges"""

    with open(json_path, mode="r", encoding="utf8") as file:
        return json.load(file)


def var_range(variable: str) -> pd.DataFrame:

    """Dataframe containing variable's choosed range"""

    v_range = read_meteorological_vars_range()[variable]
    return pd.DataFrame(v_range).transpose()


def season(model_data: pd.DataFrame, datetime_col: str) -> None:
    """
    Create Season variable using datetime column from pandas DataFrame

    Args:
        model_data = pd.DataFrame : containing datetime col
        datetime_col = str : datetime column name which the process of creation
                       will use.

    """

    seasons = read_meteorological_vars_range()["seasons"]

    # Create Season column
    model_data["Season"] = None

    # Creating Year column
    model_data["Year"] = model_data[datetime_col].dt.strftime("%Y")

    # Filling model_data with
    for season, dt_range in seasons.items():
        print(season, dt_range)

        # Creating series with season start date
        model_data[season + "_start"] = pd.to_datetime(
            model_data["Year"] + "-" + dt_range["start"]
        )

        # Creating series with season ending date
        model_data[season + "_end"] = pd.to_datetime(
            model_data["Year"] + "-" + dt_range["end"]
        )

        # Condition
        _starting = model_data[datetime_col] >= model_data[season + "_start"]
        _ending = model_data[datetime_col] <= model_data[season + "_end"]
        _between = _starting & _ending

        # Category
        model_data.loc[_between, "Season"] = season[:6]

        # Drop aux seasons columns
        _drop_cols = [season + "_start", season + "_end"]
        model_data.drop(columns=_drop_cols, inplace=True)

    # Drop aux seasons columns
    model_data.drop(columns=["Year"], inplace=True)


def possible_range(model_data: pd.DataFrame, var_col: str) -> np.ndarray:

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

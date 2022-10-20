"""
Module which objective is concat every variable create on model dataset
for training the model.
"""

import pandas as pd


def var_season(model_data: pd.DataFrame, datetime_col: str):
    """
    Create Season variable using datetime column from pandas DataFrame

    Args:
        model_data = pd.DataFrame : containing datetime col
        datetime_col = str : datetime column name which the process of creation
                       will use.

    """

    seasons = {
        "summer_pre": {"start": "01-01", "end": "03-20"},
        "autumn": {"start": "03-21", "end": "06-20"},
        "winter": {"start": "06-21", "end": "09-22"},
        "spring": {"start": "09-23", "end": "12-20"},
        "summer_post": {"start": "12-21", "end": "12-31"},
    }

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

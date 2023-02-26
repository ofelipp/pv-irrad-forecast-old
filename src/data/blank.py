# ! ./venv/bin/python3.8

""" Create templates script """

import pandas as pd
import numpy as np


def timeseries_dataset(
    min_date: str, max_date: str, frequency: str = "m", resolution: int = 15
) -> pd.DataFrame:

    """
    Function that returns a dataframe containing a timeseries dataset with a
    date interval passed as arguments.

    min_date: begining of timeserie
    max_date: end of timeserie
    frequency: minimum unit of Dataframe = ["d", "h", "m"]
    resolution: the minimum interval between rows

    """

    # Model dataset creation from date range
    if (frequency == "h") | (frequency == "m"):
        model_dataset = pd.DataFrame(
            {"Datetime": pd.date_range(min_date, max_date, freq="h")}
        )
    else:
        model_dataset = pd.DataFrame(
            {"Datetime": pd.date_range(min_date, max_date, freq=frequency)}
        )

    # Auxiliar columns
    model_dataset["Date"] = model_dataset["Datetime"].dt.strftime("%Y-%m-%d")
    model_dataset["Date"] = pd.to_datetime(model_dataset["Date"])

    if (frequency == "h") | (frequency == "m"):
        model_dataset["Hour"] = model_dataset["Datetime"].dt.strftime("%H")
        model_dataset["Hour"] = pd.to_numeric(model_dataset["Hour"])

    if (frequency == "m") and (resolution > 0):
        for minute in np.arange(0, 60, resolution):
            if minute == 0:
                model_dataset["Minute"] = minute
            else:
                tmp = model_dataset.copy()
                tmp["Minute"] = minute
                model_dataset = pd.concat([model_dataset, tmp])
                model_dataset.drop_duplicates(inplace=True)
                del tmp

        _delta = pd.to_timedelta(model_dataset["Minute"], unit="m")
        model_dataset["Datetime"] += _delta

    return model_dataset

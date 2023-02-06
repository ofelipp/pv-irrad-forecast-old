"""
Module destinated to clean an prepare dataset to train the model.
"""

import json
import re
import numpy as np
import pandas as pd
from unidecode import unidecode


def skip_rows_file(filepath: str, pattern: str = "Data"):

    """
    Function used to remove initial lines which not corresponds to columns
    """

    with open(filepath, "r+") as file:
        lines = file.readlines()
        file.seek(0)

        dt_encountred = False

        for line in lines:
            if dt_encountred:
                file.write(line)
            elif pattern in line.strip("/n"):
                file.write(line)
                dt_encountred = True
            else:
                pass

        file.truncate()


def standard_columns(data: pd.DataFrame, json_path: str):

    """
    Function to rename DataFrame colums with json regex pattern and drop which
    one are not designed in json.
    """

    # Rename columns in Dataframe using Regex
    with open(json_path, "r", encoding="utf-8") as json_file:
        rename_dict_rg = json.load(json_file)

    for key, value in rename_dict_rg.items():
        data.columns = data.columns.str.replace(key, value, regex=True)

    # Removing columns which not corresponds to the mapping
    unique_columns = list(set(rename_dict_rg.values()))
    drop_cols = [col for col in data.columns if col not in unique_columns]

    print(f"Columns not founded in pattern:{drop_cols}")

    data.drop(columns=drop_cols, inplace=True)


def read_clean_file(filepath: str) -> pd.DataFrame:

    """
    Function with objective of read and clean the data from the file.

        * Drop index column
        * Drop 'Unnamed' columns
        * Drop rows without data
        * Drop columns without data (all)
        * Rename the columns
        * Select the type for columns
    """

    # Read
    relatorio = pd.read_csv(filepath)

    # Strandarlize Columns
    standard_columns(
        data=relatorio,
        json_path="src/static/metereological_variable_names_regex.json"
    )

    # Index column treatment
    relatorio["Datetime"] = pd.to_datetime(
        relatorio["Datetime"], dayfirst=True, errors="coerce"
    )

    # Drop lines which has no data on index column
    _has_no_date = relatorio["Datetime"].isnull()
    relatorio = relatorio[~_has_no_date].copy()

    # Drop columns which has no data in any rows
    relatorio.dropna(axis=1, inplace=True, how="all")

    # Remove duplicated columns
    _mask = relatorio.columns.duplicated()
    relatorio = relatorio.loc[:, ~_mask].copy()

    # Numeric columns treatment
    num_cols = [
        col for col in relatorio.columns
        if (col != "Datetime") & (col != "Hour")
    ]

    for col in num_cols:
        relatorio[col] = pd.to_numeric(relatorio[col], errors="coerce")

    # Adding Hour to Datetime column if exists
    if "Hour" in relatorio.columns:
        _mask = relatorio["Hour"].notnull()

        relatorio.loc[_mask, "Datetime"] = relatorio.loc[
            _mask, "Datetime"
        ].dt.normalize()

        relatorio.loc[_mask, "Datetime"] += pd.to_timedelta(
            relatorio.loc[_mask, "Hour"]
        )

    # Adding station name
    station_name = re.findall(r"\b\w+?(?=_\d)", filepath)[0]
    station_name = re.sub(r"^\_+", "", station_name)
    station_name = unidecode(station_name)

    relatorio["Station"] = station_name

    return relatorio


def data_with_duplicates(data: pd.DataFrame, grb_cols: list) -> pd.DataFrame:

    """
    Function to return a pandas dataframe containing duplicates on selected
    groupby columns setted by grb_cols.
    """

    dup = data.copy()
    dup["count"] = 1
    dup = dup.groupby(grb_cols).agg({"count": "count"}).reset_index()

    _mask = dup["count"] > 1

    dup = pd.merge(dup[_mask], data, on=grb_cols, how="left")
    dup.sort_values(by=["count"], ascending=False, inplace=True)

    return dup


def blank_timeseries_dataset(
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

# ! ./venv/bin/python3.8

"""
Module destinated to clean an prepare dataset to train the model.
"""

from config import project_paths
from data.io import json_to_dict
from logging import debug, warning
import pandas as pd
import re


PATH = project_paths()
STATIC = "".join([PATH["ROOT"], PATH["DATA"]["STATIC"]])


def skip_rows_file(filepath: str, pattern: str = "dat"):

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
            elif pattern in line.lower().strip("/n"):
                file.write(line)
                dt_encountred = True
            else:
                pass

        file.truncate()


def rename_features(
    filepath: str,
    json_path: str = f"{STATIC}metereological_variable_names_regex.json"
):
    """
    Function to rename DataFrame colums with json regex pattern and drop which
    one are not designed in json.
    """

    # Read
    if "estacao_solar" in filepath:
        data = pd.read_csv(
            filepath, sep=';', decimal=',', encoding="latin-1",
            low_memory=False
        )
    else:
        data = pd.read_csv(filepath, low_memory=False)

    # Rename columns in Dataframe using Regex
    rename_dict_rg = json_to_dict(json_path)

    for key, value in rename_dict_rg.items():
        data.columns = data.columns.str.replace(key, value, regex=True)

    # Removing columns which not corresponds to the mapping
    unique_columns = list(set(rename_dict_rg.values()))
    drop_cols = [col for col in data.columns if col not in unique_columns]
    data.drop(columns=drop_cols, inplace=True)

    debug(f"Shape:{data.shape}")
    debug(f"Features:{data.columns}")
    warning(f"Columns not founded in pattern:{drop_cols}")

    data.to_csv(filepath, index=False)


def clean_file(filepath: str) -> pd.DataFrame:

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
    relatorio = pd.read_csv(filepath, low_memory=False)

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
    relatorio.columns = [
        re.sub("\\.\\d$", "", col) for col in relatorio.columns
    ]
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

        relatorio.loc[_mask, "Datetime"] = relatorio.loc[_mask, "Datetime"]\
            .dt.normalize()

        relatorio.loc[_mask, "Datetime"] += \
            pd.to_timedelta(relatorio.loc[_mask, "Hour"])

    relatorio.to_csv(filepath, index=False)


def data_with_duplicates(data: pd.DataFrame, grb_cols: list) -> pd.DataFrame:

    """
    Function to return a pandas dataframe containing duplicates on
    selected groupby columns setted by grb_cols.
    """

    dup = data.copy()
    dup["count"] = 1
    dup = dup.groupby(grb_cols).agg({"count": "count"}).reset_index()

    _mask = dup["count"] > 1

    dup = pd.merge(dup[_mask], data, on=grb_cols, how="left")
    dup.sort_values(by=["count"], ascending=False, inplace=True)

    return dup

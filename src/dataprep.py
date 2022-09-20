"""
Module destinated to clean an prepare dataset to train the model.
"""

import json
import pandas as pd


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


def read_clean_file(filename: str) -> pd.DataFrame:

    """
    Function with objective of read and clean the data from the file.

        * Drop index column
        * Drop 'Unnamed' columns
        * Drop rows without data
        * Drop columns without data (all)
        * Rename the columns
        * Select the type for columns

    """

    relatorio = pd.read_csv(filename)

    # Drop Index column and 'Unnamed' columns
    unnamed_cols = [col for col in relatorio.columns if "Unnamed" in col]
    idx_col = [relatorio.columns[0]]
    drop_cols = unnamed_cols + idx_col

    relatorio.drop(columns=drop_cols, inplace=True)

    # Drop lines which has no data on date column
    # TODO: If has 'Data' and 'Hour' columns ratter than 'Data /Hora' ? Example = tanquedetenção maio 2021

    relatorio["Data / Hora"] = pd.to_datetime(
        relatorio["Data / Hora"], dayfirst=True, errors="coerce"
    )

    _has_no_date = relatorio["Data / Hora"].isnull()
    relatorio = relatorio[~_has_no_date].copy()

    # Guarantee that has no columns with no data
    relatorio.dropna(axis=1, inplace=True, how="all")

    # Rename columns in Dataframe
    with open("src/static/metereological_variable_names.json") as json_file:
        rename_dict = json.load(json_file)

    relatorio.rename(columns=rename_dict, inplace=True)

    # Columns types
    for col in relatorio.columns[1:]:
        relatorio[col] = pd.to_numeric(relatorio[col], errors="coerce")

    return relatorio

"""
Program to forecast load curve for Brazilian energy system, grouping by market
sectors which are united by SIN.

Author: ofelippm (felippe.matheus@aluno.ufabc.edu.br)
"""

import pandas as pd
from src import gdrive


RAW = "data/raw/"


def get_root_dir(df_files: pd.DataFrame) -> pd.Series:

    """
    Function to get root directory for every file in archive tree
    """

    # Initializing counter and condition
    counter = 0
    have_subdirs = True
    df = df_files.copy()

    # While statement to search for subdirs
    while have_subdirs:

        if counter == 0:
            df[f"parents_parent{counter}"] = df["parents"].copy()

        df[f"id_parent{counter}"] = df[f"parents_parent{counter}"].copy()

        # Get parents ids and names to concat
        df = pd.merge(
            df,
            df[["id", "name", "parents"]],
            left_on=f"id_parent{counter}",
            right_on="id",
            how="left",
            suffixes=["", f"_parent{counter+1}"],
        )

        # If all column is null, there's no other subdir
        if df[f"id_parent{counter}"].notnull().sum() == 0:

            df.fillna("", inplace=True)

            # Concat every name from dirs above
            df["root_dir"] = df[f"name_parent{counter-1}"]

            for c in range(counter - 2, 0, -1):
                df["root_dir"] += "_" + df[f"name_parent{c}"]

            # Final treatments
            df["root_dir"] = df["root_dir"].astype(str).str.lower()
            df["root_dir"] = df["root_dir"].str.replace(
                pat=r"\_{2,}", repl="", regex=True
            )
            df["root_dir"] = df["root_dir"].str.replace(
                pat=r"\s+", repl="_", regex=True
            )

            # Change to False to finish loop
            have_subdirs = False

        counter += 1  # Increment

    return df["root_dir"]


def main():

    """
    main function

    Topics:
        1. leitura dos dados
        # limpeza e tratamento dos valores
        # escolha do modelo
        # escolha da janela de treinamento
        # treinamento do modelo
        # verificacao da acuracia do modelo no treino
        # teste do modelo
        # verificacao da acuracia do modelo no teste
        # tunelamento de hyperparametros
        # comparacao dos resultados com o atual PrevCargaDESSEM 2.0
        # export da previsão
    """

    # Data - List Files
    service = gdrive.connect(".cred_gdrive_ufabc.json")
    ic_folders = gdrive.list_files_from_folder(service)
    ic_files = gdrive.list_nested_files(service, ic_folders)

    # DataFrame containing all files
    # df_ic_files=pd.read_csv('ids_files.csv', sep=';', decimal=',')

    df_ic_files = pd.DataFrame(ic_files)
    df_ic_files["parents"] = df_ic_files["parents"].astype(str).str.slice(2, 35)
    df_ic_files["root_dir"] = get_root_dir(df_ic_files)

    # df_ic_files.to_csv('ic_files.csv')

    # Data - Extract Files
    _not_folder = ~df_ic_files["mimeType"].str.contains("folder")

    for idx, row in df_ic_files[_not_folder].iterrows():

        print(idx, row["name"])

        if ("excel" in row["mimeType"]) | ("openxml" in row["mimeType"]):
            download_file = gdrive.download_IOfile(service, row["id"])
            excel = pd.read_excel(download_file)
            # excel.to_parquet(f"{RAW}{row['root_dir']}_{row['name']}.parquet")
            excel.to_csv(f"{RAW}{row['root_dir']}_{row['name']}.csv")
        else:
            pass


if __name__ == "__main__":
    main()

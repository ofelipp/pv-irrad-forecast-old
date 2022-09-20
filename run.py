"""
Program to forecast irradiance curve for Brazilian energy system, located in
Santo Andre. The data are retrieved from SEMASA meteorologic stations.

The topics from main function:
    1. Data - Extraction
    2. Data - Cleaning

Author: ofelippm (felippe.matheus@aluno.ufabc.edu.br)
"""

import pandas as pd
from src import gdrive

RAW = "data/raw/"


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

    # Data - List files
    service = gdrive.connect("src/static.cred_gdrive_ufabc.json")
    ic_folders = gdrive.list_files_from_folder(service)
    ic_files = gdrive.list_nested_files(service, ic_folders)
    ic_files_root_dir = gdrive.get_root_dir(ic_files)

    # Data - DataFrame containing all files
    df_ic_files = pd.DataFrame(ic_files)
    df_ic_files["root_dir"] = ic_files_root_dir

    # df_ic_files=pd.read_csv('ids_files.csv', sep=';', decimal=',')
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

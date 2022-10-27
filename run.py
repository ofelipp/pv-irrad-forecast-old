"""
Program to forecast irradiance curve for Brazilian energy system, located in
Santo Andre. The data are retrieved from SEMASA meteorologic stations.

The topics from main function:
    1. Data - Extraction
    2. Data - Cleaning

Author: ofelippm (felippe.matheus@aluno.ufabc.edu.br)
"""


import os
import pandas as pd
from src import gdrive, dataprep, variables

RAW = "data/raw/"
PRC = "data/prc/"
MDL = "data/model/"

# TODO: Testar modificaçao de ordem da funcao dataprep com tanquedetencao 20-08


pd.set_option("display.max_columns", 20)


def main():

    """
    main function

    Topics:
        1. Data
            1.1 List files
            1.2 Dataframe containing all files
            1.3 Extract files from GDrive
            1.4 Clean/Standardize
            1.5 Prepare Model Dataset

        2. Model
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

    # Data - Extract Files from GDrive
    _not_folder = ~df_ic_files["mimeType"].str.contains("folder")

    for idx, row in df_ic_files[_not_folder].iterrows():

        print(idx, row["name"])

        if ("excel" in row["mimeType"]) | ("openxml" in row["mimeType"]):
            download_file = gdrive.download_iofile(service, row["id"])
            excel = pd.read_excel(download_file)
            excel.to_csv(f"{RAW}{row['root_dir']}_{row['name']}.csv")
        else:
            pass

    # Data - Clean/Standardize
    weather_data = pd.DataFrame()

    for root, dirs, files in os.walk(RAW):
        if root == RAW:
            for file in files:
                print(f"{file}")

                dataprep.skip_rows_file(f"{RAW}{file}")

                weather_data = pd.concat(
                    [weather_data, dataprep.read_clean_file(f"{RAW}{file}")]
                )

    weather_data.drop(columns=["Hour"], inplace=True)
    weather_data.drop_duplicates(inplace=True)
    weather_data.sort_values(by=["Station", "Datetime"], inplace=True)

    # Datetime Variables
    weather_data["Date"] = weather_data["Datetime"].dt.strftime("%Y-%m-%d")
    weather_data["Date"] = pd.to_datetime(weather_data["Date"])

    weather_data["Hour"] = weather_data["Datetime"].dt.strftime("%H")
    weather_data["Hour"] = pd.to_numeric(weather_data["Hour"])

    weather_data["Minute"] = weather_data["Datetime"].dt.strftime("%M")
    weather_data["Minute"] = pd.to_numeric(weather_data["Minute"])
    weather_data["Minute"] = (weather_data["Minute"] // 15) * 15

    # Verify duplicates on weather dataset
    _idx_cols = ["Station", "Date", "Hour", "Minute"]
    duplicated_data = dataprep.data_with_duplicates(weather_data, _idx_cols)
    duplicated_data.to_csv(
        f"{PRC}duplicated_data.csv", sep=";", decimal=",", index=False
    )

    # Drop duplicates, mantaining first
    weather_data.drop_duplicates(subset=_idx_cols, inplace=True)

    # Export Data
    weather_data.to_parquet(f"{PRC}weather_data.parquet", index=False)

    # Model Dataset Creation --------------------------------------------------

    # Date parameters
    _min_date = weather_data["Datetime"].min().normalize()
    _max_date = (weather_data["Datetime"].max() + pd.Timedelta(1, unit="d")).normalize()

    model_dataset = dataprep.blank_timeseries_dataset(_min_date, _max_date)

    # Replicate Dataset for each station
    _stations = weather_data["Station"].unique()

    for station in _stations:
        if station == _stations[0]:
            model_dataset["Station"] = station
        else:
            tmp = model_dataset.copy()
            tmp["Station"] = station
            model_dataset = pd.concat([model_dataset, tmp])
            model_dataset.drop_duplicates(inplace=True)
            del tmp

    model_dataset.sort_values(["Datetime", "Station"], inplace=True)

    # Filling Model Dataset with variables ------------------------------------

    _data_columns = [
        "Relative_Umidity_perc",
        "Pressure_mBar",
        "Rain_mmh",
        "Wind_Speed_kmh",
        "Wind_Direction_dg",
        "Min_Temperature_C",
        "Max_Temperature_C",
        "Air_Temperature_C",
        "Thermic_Sensation_C",
        "Radiation_Wm2",
    ]

    _merge_cols = ["Date", "Hour", "Minute", "Station"]

    model_dataset_filled = pd.merge(
        left=model_dataset,
        right=weather_data[_merge_cols + _data_columns],
        on=_merge_cols,
        how="left",
        suffixes=["", "_org"],
    )

    model_dataset_filled.to_parquet(f"{MDL}model_dataset.parquet", index=False)

    # Create Variables --------------------------------------------------------

    # Season
    variables.season(model_dataset_filled, "Datetime")

    # Adjusting variables to possible ranges
    for dcol in _data_columns:
        model_dataset_filled[dcol] = variables.possible_range(
            model_data=model_dataset_filled, var_col=dcol
        )


# Statistics - NA quantities
# Statistics - Timeseries plots
# Statistics - Variables plots


if __name__ == "__main__":
    main()

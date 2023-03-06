"""
Program to forecast radiance curve for Brazilian energy system, located in
Santo Andre. The data are retrieved from SEMASA meteorologic stations and UFABC
Solar Project.

Author: ofelippm (felippe.matheus@aluno.ufabc.edu.br)
"""

import config
from data.pipeline import DataPipeline
from logging import info
# from model import fill_missings
# import pandas as pd
# import os

config.log()

PATH = config.project_paths()
STATIC = "".join([PATH["ROOT"], PATH["DATA"]["STATIC"]])
RAW_DATA = "".join([PATH["ROOT"], PATH["DATA"]["RAW"]])
PRC_DATA = "".join([PATH["ROOT"], PATH["DATA"]["PRC"]])
MDL_DATA = "".join([PATH["ROOT"], PATH["MODEL"]])


def main():

    """
    """

    data_pipeline = DataPipeline()
    data_pipeline.extract_files_gdrive(f"{STATIC}.cred_gdrive_ufabc.json")
    data_pipeline.clean_rename_files()
    data_pipeline.concatenate_files()
    data_pipeline.add_features()

    # # Verify duplicates on weather dataset
    # _idx_cols = ["Station", "Date", "Hour", "Minute"]
    # duplicated_data = clean.data_with_duplicates(weather_data, _idx_cols)

    # duplicated_data.to_csv(
    #     f"{PRC_DATA}duplicated_data.csv", sep=";", decimal=",", index=False
    # )

    # # Drop duplicates, mantaining first
    # weather_data.drop_duplicates(subset=_idx_cols, inplace=True)

    # # Export Data
    # weather_data.to_parquet(
    #     f"{PRC_DATA}weather_data.parquet", index=False
    # )

    # # Model Dataset Creation --------------------------------------------------

    # # Date parameters
    # _min_date = weather_data["Datetime"].min().normalize()
    # _max_date = (
    #     weather_data["Datetime"].max() + pd.Timedelta(1, unit="d")
    # ).normalize()

    # model_dataset = blank.timeseries_dataset(_min_date, _max_date)

    # # Replicate Dataset for each station
    # _stations = weather_data["Station"].unique()

    # for station in _stations:
    #     if station == _stations[0]:
    #         model_dataset["Station"] = station
    #     else:
    #         tmp = model_dataset.copy()
    #         tmp["Station"] = station
    #         model_dataset = pd.concat([model_dataset, tmp])
    #         model_dataset.drop_duplicates(inplace=True)
    #         del tmp

    # model_dataset.sort_values(["Datetime", "Station"], inplace=True)

    # # Filling Model Dataset with variables ------------------------------------

    # _data_columns = [
    #     "Relative_Umidity_perc",
    #     "Pressure_mBar",
    #     "Rain_mmh",
    #     "Wind_Speed_kmh",
    #     "Wind_Direction_dg",
    #     "Dew_Temperature_C",
    #     "Inner_Temperature_C",
    #     "Air_Temperature_C",
    #     "Thermic_Sensation_C",
    #     "Radiation_Wm2",
    # ]

    # _merge_cols = ["Date", "Hour", "Minute", "Station"]

    # model_dataset_filled = pd.merge(
    #     left=model_dataset,
    #     right=weather_data[_merge_cols + _data_columns],
    #     on=_merge_cols,
    #     how="left",
    #     suffixes=["", "_org"],
    # )

    # model_dataset_filled.to_parquet(
    #     f"{PRC_DATA}model_dataset.parquet", index=False
    # )

    # # Create Variables --------------------------------------------------------

    # # Season
    # model_dataset_filled["Season"] = features.season(
    #     model_datetime_data=model_dataset_filled["Datetime"]
    # )

    # # Adjusting variables to possible ranges
    # for dcol in _data_columns:
    #     model_dataset_filled[dcol] = features.possible_range(
    #         model_data=model_dataset_filled, var_col=dcol
    #     )

    # # Export Ranged DataFrame
    # model_dataset_filled.to_parquet(
    #     f"{PRC_DATA}model_dataset_ranged.parquet", index=False
    # )

    # # Filling Missing Values --------------------------------------------------

    # feature_names = [
    #     'Relative_Umidity_perc', 'Pressure_mBar', 'Rain_mmh', 'Wind_Speed_kmh',
    #     'Wind_Direction_dg', 'Dew_Temperature_C', 'Inner_Temperature_C',
    #     'Air_Temperature_C', 'Thermic_Sensation_C', 'Radiation_Wm2'
    # ]

    # # Correlation Coeficient Calculation
    # corr_df, corr_dict = fill_missings.correlation_features_stations(
    #     data=model_dataset_filled, features_list=feature_names
    # )

    # # Saving
    # io.dict_to_json(
    #     dictionary=corr_dict,
    #     path=f"{MDL_DATA}linear_regression_corr_feat_station.json"
    # )

    # corr_df.to_csv(
    #     f"{PRC_DATA}/fill_missings/correlation_coef_stations.csv",
    #     sep=';', decimal=',', index=False
    # )

    # # Filling
    # model_dataset_filled_wito_nas = fill_missings.fill_missing_values(
    #     data=model_dataset_filled, corr_dict=corr_dict
    # )

    # # Exporting
    # model_dataset_filled_wito_nas.to_parquet(
    #     f"{PRC_DATA}model_dataset_filled_missings.parquet", index=False
    # )

    # Modeling ===============================================================

if __name__ == "__main__":

    info("Program started...")

    main()

    info("Program ended...")

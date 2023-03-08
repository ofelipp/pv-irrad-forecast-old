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
    data_pipeline.adjust_features_ranges()
    data_pipeline.create_fill_model_dataset()

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

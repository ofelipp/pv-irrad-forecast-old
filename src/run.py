"""
Program to forecast radiance curve for Brazilian energy system, located in
Santo Andre. The data are retrieved from SEMASA meteorologic stations and UFABC
Solar Project.

Author: ofelippm (felippe.matheus@aluno.ufabc.edu.br)
"""

import config
from data.io import save_artfact, load_artfact
from data.pipeline import DataPipeline
from logging import info
import os

config.log()

PATH = config.project_paths()
STATIC = "".join([PATH["ROOT"], PATH["DATA"]["STATIC"]])
RAW_DATA = "".join([PATH["ROOT"], PATH["DATA"]["RAW"]])
PRC_DATA = "".join([PATH["ROOT"], PATH["DATA"]["PRC"]])
MDL_DATA = "".join([PATH["ROOT"], PATH["MODEL"]])

USE_PREVIOUSLY = True


def main():

    """
    Script destinated to create data and models pipelines.

    The Data Pipeline constructs a features model parquet file based
    on a ETL from raw data, cleaning and adjusting the features,

    The Model Pipeline is responsible for generate models, their
    training and test dataset, evaluate the models, save the best
    and predict.

    """

    info("Data Pipeline")

    _data_pipe_exists = os.path.isfile(f"{MDL_DATA}/data_pipeline.pickle")

    if _data_pipe_exists & USE_PREVIOUSLY:

        info("Importing previously one...")
        data_pipeline = load_artfact(f"{MDL_DATA}/data_pipeline.pickle")

    else:

        info("Starting from scratch")
        data_pipeline = DataPipeline()

        data_pipeline.extract_files_gdrive(f"{STATIC}.cred_gdrive_ufabc.json")
        data_pipeline.clean_rename_files()
        data_pipeline.concatenate_files()
        data_pipeline.add_features(use_existing=True)
        data_pipeline.adjust_features_ranges()
        data_pipeline.create_fill_model_dataset()
        data_pipeline.fill_missings()

        save_artfact(data_pipeline, "data_pipeline", MDL_DATA)


if __name__ == "__main__":

    info("Program started...")

    main()

    info("Program ended...")

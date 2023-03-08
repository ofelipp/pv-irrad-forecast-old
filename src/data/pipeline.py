# ! ./venv/bin/python3.8

"""
Module destinated to create a data pipeline with a class.
"""

from config import project_paths, log
from data import blank, clean, gdrive, features
from logging import debug, info, error  # warning, fatal
from os import walk
import pandas as pd
from time import time

log()

PATH = project_paths()
STATIC = "".join([PATH["ROOT"], PATH["DATA"]["STATIC"]])
RAW_DATA = "".join([PATH["ROOT"], PATH["DATA"]["RAW"]])
PRC_DATA = "".join([PATH["ROOT"], PATH["DATA"]["PRC"]])
MDL_DATA = "".join([PATH["ROOT"], PATH["MODEL"]])


class DataPipeline():

    info("Initializing DataPipeline")

    def __init__(self):
        self.name = "DataPipeline"

        # Dataframes
        self.files_gdrive = None
        self.features_raw = None
        self.features_prc = None

        # Lists
        self.features_names = []
        self.features_calendar_names = []
        self.features_weather_names = []

    def __repr__(self):
        "".join(["Inicializando"])

    def extract_files_gdrive(self, credentials):
        info("Files extraction from Google Drive")
        _start = time()

        debug("Connect to GDrive")
        client = gdrive.connect(credentials)

        debug("List folders/files from GDrive")
        ic_folders = gdrive.list_files_from_folder(client)
        ic_files = gdrive.list_nested_files(client, ic_folders)
        ic_files_root_dir = gdrive.get_root_dir(ic_files)

        debug("Dataframe containing folders/files from GDrive")
        df_ic_files = pd.DataFrame(ic_files)
        df_ic_files["root_dir"] = ic_files_root_dir
        df_ic_files["root_dir"] = \
            df_ic_files["root_dir"].str.replace(r"^\_+", "", regex=True)

        self.files_gdrive = df_ic_files.copy()

        _not_folder = ~self.files_gdrive["mimeType"].str.contains("folder")
        debug(f"Files number size:{self.files_gdrive[_not_folder].shape[0]}")

        debug("Extraction...")
        for idx, row in self.files_gdrive[_not_folder].iterrows():

            if ("excel" in row["mimeType"]) | ("openxml" in row["mimeType"]):

                debug(f"{idx}: {row['name']}")

                download_file = gdrive.download_iofile(client, row["id"])
                excel = pd.read_excel(download_file)

                _output = f"{RAW_DATA}{row['root_dir']}_{row['name']}.csv"
                excel.to_csv(_output)

                del download_file, excel, _output

        del client, df_ic_files, ic_files_root_dir, ic_files, ic_folders

        _end = time()

        info("Files extraction completed")
        info(f"Time Elapsed: {_end - _start} seconds")

    def extract_files_api(self):
        # TODO: complete this when have a api
        info("Files extraction initialized")

    def clean_rename_files(self, path_root: str = RAW_DATA):
        info("Cleaning and rename files")
        _start = time()

        for root, dirs, files in walk(path_root):
            if root == path_root:
                for file in files:

                    _abs_file_path = f"{path_root}{file}"
                    debug(file)

                    clean.skip_rows_file(_abs_file_path)
                    clean.rename_features(_abs_file_path)
                    clean.clean_file(_abs_file_path)

        _end = time()

        info("Files cleaning completed")
        info(f"Time Elapsed: {_end - _start} seconds")

    def concatenate_files(self, path_root: str = RAW_DATA, export: bool = True):
        info("Concating all the files previously adjusted")
        _start = time()

        _concat = pd.DataFrame()

        for root, dirs, files in walk(path_root):

            # Only files in root path will be concated
            if root == path_root:

                for file in files:
                    debug(f"{file}")

                    _abs_file_path = f"{path_root}{file}"

                    _arch = pd.read_csv(_abs_file_path)
                    _arch["Station"] = features.station(_abs_file_path)

                    _concat = pd.concat([_concat, _arch])

        _concat.drop(columns=["Hour"], inplace=True)
        _concat.drop_duplicates(inplace=True)

        self.features_raw = _concat.copy()

        info("Files concated")

        if export:
            info("Exporting concated raw features..")
            debug(f"Final shape:{self.features_raw.shape}")

            self.features_raw.to_parquet(f"{PRC_DATA}raw_features.parquet")

        del _concat, _arch, _abs_file_path, file, root, dirs, files

        _end = time()
        info(f"Time Elapsed: {_end - _start} seconds")

    def add_features(self, use_existing: bool = True):
        info("Adding features")
        _start = time()

        if (self.features_raw is None) & use_existing:
            try:
                self.features_raw = pd.read_parquet(
                    f"{PRC_DATA}raw_features.parquet"
                )
            except OSError as traceback:
                _msg = "".join([
                    f"File 'raw_features.parquet' not founded in '{PRC_DATA}' ",
                    "path. Please verify if previous methods (extract, clean ",
                    "and concat) were applied."])
                error(_msg, traceback)

        info("Datetime variables")
        self.features_prc = pd.concat([
            self.features_raw,
            features.datetime_variables(self.features_raw["Datetime"])
        ], axis=1)

        info("Calendar variables")
        self.features_prc = pd.concat([
            self.features_prc,
            features.calendar_variables(self.features_prc["Datetime"])
        ], axis=1)

        info("Season")
        self.features_prc["Season"] = \
            features.season(self.features_prc["Datetime"])

        info("Adding variables names")
        self.features_calendar_names += list(
            features.datetime_variables(
                self.features_raw["Datetime"][0:1]
            ).columns
        )

        self.features_calendar_names += list(
            features.calendar_variables(
                self.features_prc["Datetime"][0:1]
            ).columns
        )

        self.features_calendar_names += ["Season"]
        self.features_names += self.features_calendar_names

        _end = time()
        info(f"Time Elapsed: {_end - _start} seconds")

    def adjust_features_ranges(self):
        info("Adjusting the range for each feature")
        _start = time()

        self.features_weather_names = \
            list(features.var_range().keys())[1:]

        self.features_names += self.features_weather_names

        for met_feat in self.features_weather_names:
            self.features_prc[met_feat] = features.possible_range(
                model_data=self.features_prc, var_col=met_feat
            )

        _end = time()
        info(f"Time Elapsed: {_end - _start} seconds")

    def create_fill_model_dataset(self):

        info("Create empty model dataset with datetime index")

        _start = time()

        self.features_prc["Datetime"] = \
            pd.to_datetime(self.features_prc["Datetime"])

        _min_date = self.features_prc["Datetime"].min().normalize()
        _max_date = (
            self.features_prc["Datetime"].max() + pd.Timedelta(1, unit="d")
        ).normalize()

        _msg = "".join([
            f"Min Date: {_min_date.strftime('%Y-%m-%d')}, "
            f"Max Date: {_max_date.strftime('%Y-%m-%d')}"
        ])

        debug(_msg)

        empty_model_dataset = blank.timeseries_dataset(_min_date, _max_date)

        # Replicate Dataset for each station
        _stations = self.features_prc["Station"].unique()

        for station in _stations:
            debug(f"{station}")

            if station == _stations[0]:
                empty_model_dataset["Station"] = station
            else:
                tmp = empty_model_dataset.copy()
                tmp["Station"] = station
                empty_model_dataset = pd.concat([empty_model_dataset, tmp])
                empty_model_dataset.drop_duplicates(inplace=True)
                del tmp

        empty_model_dataset.sort_values(["Datetime", "Station"], inplace=True)

        info("Filling empty model dataset with fetures from each station")

        _merge_cols = ["Date", "Hour", "Minute", "Station"]

        self.features_model = pd.merge(
            left=empty_model_dataset, right=self.features_prc,
            on=_merge_cols, how="left", suffixes=["", "_org"],
        )

        _end = time()
        info(f"Time Elapsed: {_end - _start} seconds")

    def fill_missings(self):
        info("Identifying and filling missing values")
        ...

    def export_model_dataset(self):
        info("Exporting filled model dataset")
        ...

# ! ./venv/bin/python3.8

"""
Module destinated to create a data pipeline with a class.
"""

from config import project_paths
from logging import debug, info, warning, error, fatal


PATH = project_paths()


class DataPipeline():

    def __init__(self):
        self.name = "DataPipeline"

    def __repr__(self):
        info("Initializing DataPipeline")

    def extract_files_gdrive(self):
        info("Files extraction initialized")
        ...

    def clean_rename_files(self):
        info("Cleaning and rename files")
        ...

    def adjust_features_ranges(self):
        info("Adjusting the range for each feature")
        ...

    def concatenate_files(self):
        info("Concating all the files previously adjusted")
        ...

    def create_fill_model_dataset(self):
        info("Concating all the files previously adjusted")
        ...

    def fill_missings(self):
        info("Identifying and filling missing values")
        ...

    def export_model_dataset(self):
        info("Exporting filled model dataset")
        ...

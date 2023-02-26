# ! ./venv/bin/python3.8

""" Config file """

from data.io import json_to_dict
from logging import basicConfig, DEBUG, FileHandler
import datetime


def project_paths() -> dict:

    return json_to_dict("paths.json")


def log():

    PATH = project_paths()
    LOG = "".join([PATH["ROOT"], PATH["LOG"]])
    YYYYMMDD_HHMM = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    return basicConfig(
        level=DEBUG,
        format="%(asctime)s\t[ %(levelname)s ]\t%(message)s",
        handlers=[FileHandler(f"{LOG}{YYYYMMDD_HHMM}_ic.log")]
    )

"""
Script used to config Paths and other global variables used in code.
"""

from os.path import abspath
import logging
from datetime import datetime


def init():

    global PATHS

    ROOT = abspath(".")

    PATHS = {
        "ROOT": ROOT,
        "LOGS": f"{ROOT}/logs/",
        "DATA": f"{ROOT}/data/",
        "PRC_DATA": f"{ROOT}/data/prc/",
        "RAW_DATA": f"{ROOT}/data/raw/",
        "STATIC": f"{ROOT}/src/static/",
        "MODEL": f"{ROOT}/models/",
        "TESTS": f"{ROOT}/tests/"
    }


def log():

    _now = datetime.now().strftime("%Y%m%d_%H%M")

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(f"{PATHS['LOGS']}{_now}_tg.log", "w"),
            logging.StreamHandler()
        ]
    )


if __name__ == "__main__":
    init()
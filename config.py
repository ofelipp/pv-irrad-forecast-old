"""
Script used to config Paths and other global variables used in code.
"""

from os.path import abspath


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


if __name__ == "__main__":
    init()
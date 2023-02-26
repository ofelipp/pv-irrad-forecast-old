# ! ./venv/bin/python3.8

"""
Script destinated to create import and output functions to read jsons, csv
and excel files and export the final product into
"""

import json
import pickle
import os


def json_to_dict(path: str) -> dict:

    """ Function used to import json archive into python dictionary """

    with open(path, mode="r+", encoding="utf8") as json_file:
        return json.load(json_file)


def dict_to_json(dictionary: dict, path: str):

    """ Function used to export dictionary in json format """

    with open(path, mode="w", encoding="utf8") as json_file:
        json.dump(dictionary, json_file, indent=4)

    assert os.path.isfile(path) is True, \
        f'Impossible to save json file.. not founded in {path}'


def list_dir_files(path: str) -> list:

    """ Function which returns a list of filepaths in a directory """

    all_files = []

    for root, dirs, files in os.walk(path):

        # Reading only subdirectories
        if len(dirs) == 0:
            subdir_files = [root + "/" + file for file in files]
            all_files += subdir_files

    return all_files


def load_artfact(filepath):

    assert os.path.isfile(filepath) is True, \
        f'Artfact not founded in {filepath}'

    with open(filepath, 'rb') as input_model:
        return pickle.load(input_model)


def save_artfact(model, model_name: str, path: str):

    _filepath = f"{path}/{model_name}.pickle"

    with open(_filepath, 'wb') as output_model:
        pickle.dump(model, output_model)

    assert os.path.isfile(_filepath) is True, \
        f'Impossible to save {model_name} artfact not founded in {_filepath}'

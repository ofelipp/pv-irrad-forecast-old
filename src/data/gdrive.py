"""
Module to connect and get metadata and files from Google Drive.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from .io import json_to_dict
import pandas as pd


_id_filepath = "../static/.ic_data_id.json"

DATA_IC_ID = json_to_dict(_id_filepath)["FOLDER_ID"]
SCOPES = json_to_dict(_id_filepath)["SCOPES"]


def connect(cred_json: dict):

    """Connection with Google Drive"""

    flow = InstalledAppFlow.from_client_secrets_file(cred_json, SCOPES)
    creds = flow.run_local_server(port=0)

    service = build("drive", "v3", credentials=creds)

    return service


def list_files_from_folder(service, folder_id: str = DATA_IC_ID) -> list:

    """List all files from a folder"""

    query = f"parents = '{folder_id}'"

    next_page_token = True
    files = []

    while next_page_token:
        api_response = (
            service.files()
            .list(
                q=query,
                orderBy="folder, name",
                fields="files(parents, id, mimeType, name)",
            )
            .execute()
        )
        files.extend(api_response.get("files"))
        next_page_token = api_response.get("nextPageToken")

    return files


def list_nested_files(service, folders: list) -> list:

    """List all files from directories and sub-directories"""

    actual_folders_list = []
    counter = 0

    # Loop pegando todas as infos de todas as pastas
    while counter < len(folders):

        file = folders[counter]

        actual_idx = folders.index(file)
        actual_folders_list.append(file)

        if "folder" not in file["mimeType"]:
            pass

        nested_files = list_files_from_folder(service, file["id"])

        # Atualiza lista completa
        next_idx = actual_idx + 1
        folders = actual_folders_list + nested_files + folders[next_idx:]

        # Incrementa contador
        counter += 1

    return folders


def get_root_dir(files: pd.DataFrame) -> list:

    """
    Function to get root directory for every file in archive tree
    """

    # DataFrame
    df_files = pd.DataFrame(files).copy()
    df_files["parents"] = df_files["parents"].astype(str).str.slice(2, 35)

    # Search in subdirs - while statement
    counter = 0
    have_subdirs = True

    while have_subdirs:

        if counter == 0:
            df_files[f"parents_parent{counter}"] = df_files["parents"].copy()

        df_files[f"id_parent{counter}"] = \
            df_files[f"parents_parent{counter}"].copy()

        # Get parents ids and names to concat
        df_files = pd.merge(
            left=df_files,
            right=df_files[["id", "name", "parents"]],
            left_on=f"id_parent{counter}",
            right_on="id",
            how="left",
            suffixes=["", f"_parent{counter+1}"],
        )

        # If all column is null, there's no other subdir
        if df_files[f"id_parent{counter}"].notnull().sum() == 0:

            df_files.fillna("", inplace=True)

            # Concat every name from dirs above
            df_files["root_dir"] = df_files[f"name_parent{counter-1}"]

            for idx in range(counter - 2, 0, -1):
                df_files["root_dir"] += "_" + df_files[f"name_parent{idx}"]

            # Final treatments
            df_files["root_dir"] = df_files["root_dir"].astype(str).str.lower()
            df_files["root_dir"] = df_files["root_dir"].str.replace(
                pat=r"\_{2,}", repl="", regex=True
            )
            df_files["root_dir"] = df_files["root_dir"].str.replace(
                pat=r"\s+", repl="_", regex=True
            )

            # Change to False to finish loop
            have_subdirs = False

        counter += 1  # Increment

    return df_files["root_dir"].to_list()


def download_iofile(service, file_id: str, verbose=False) -> io.BytesIO:

    """Download a single file in IOBytes format"""

    request = service.files().get_media(fileId=file_id)

    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        if verbose:
            print(f"Download {int(status.progress() * 100)}.")

    return file

import io
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd


DATA_IC_ID = ""
SCOPES = [
    # "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
]


def connect(cred_json: dict):

    """Connection with Google Drive"""

    flow = InstalledAppFlow.from_client_secrets_file(cred_json, SCOPES)
    creds = flow.run_local_server(port=0)

    service = build("drive", "v3", credentials=creds)

    return service


# @gdrive_connect
def list_files_from_folder(service, folder_id: str = DATA_IC_ID):

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


def list_nested_files(service, folders: list) -> pd.DataFrame:

    """List all files from directories and sub-directories"""

    actual_folders_list = []
    counter = 0

    # Loop pegando todas as infos de todas as pastas
    while counter < len(folders):

        file = folders[counter]

        actual_folders_list.append(file)

        if "folder" not in file["mimeType"]:
            pass

        nested_files = list_files_from_folder(service, file["id"])

        # Atualiza lista completa
        folders = (
            actual_folders_list + nested_files + folders[folders.index(file) + 1 :]
        )

        # Incrementa contador
        counter += 1

    return folders


def download_IOfile(service, file_id: str, verbose=False):

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

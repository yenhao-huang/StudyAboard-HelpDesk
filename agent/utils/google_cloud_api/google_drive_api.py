from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# 使用 OAuth 認證憑證（首次會跳出授權網頁）
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import tempfile
import gdown

def get_credentials(
    token_path,
    secret_path,
    scopes: list = ['https://www.googleapis.com/auth/drive.metadata.readonly']
):
    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secret_path, scopes)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_files_in_folder(
    folder_id,
    token_path,
    secret_path
):

    """
    Lists all non-trashed files inside a specified Google Drive folder using the Drive API.

    Args:
        folder_id (str): The ID of the Google Drive folder (can be extracted from the folder URL).
        token_path (str): Path to the token.pickle file (stores the user's OAuth access token).
                          If the file exists, it avoids the need to re-authenticate.
        secret_path (str): Path to the client secrets JSON file downloaded from Google Cloud Console.

    Returns:
        List[Dict[str, str]]: A list of file metadata dictionaries.
            Each dictionary contains:
                - id (str): The file's unique ID in Google Drive
                - name (str): The name of the file
                - mimeType (str): The MIME type (e.g., "application/json", "text/plain")

    Example:
        files = get_files_in_folder("1abc234FOLDERIDxyz", "token.pickle", "credentials.json")
        for file in files:
            print(f"{file['name']} - https://drive.google.com/file/d/{file['id']}/view")
    """
    
    creds = get_credentials(token_path, secret_path)
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        pageSize=100,
        fields="files(id, name, mimeType)"
    ).execute()

    files = results.get('files', [])
    return files

def download_drive_files(folder_id, token_path, secret_path, download_dir=None):
    files = get_files_in_folder(folder_id, token_path, secret_path)

    if download_dir is None:
        download_dir = tempfile.gettempdir()

    os.makedirs(download_dir, exist_ok=True)

    for file in files:
        file_id = file["id"]
        name = file["name"]
        mime = file["mimeType"]

        # 建立本地儲存路徑
        local_path = os.path.join(download_dir, name)

        # 組合 Google Drive URL
        gdrive_url = f"https://drive.google.com/uc?id={file_id}"
        print(f"[↓] Downloading {name} from {gdrive_url} ...")
        gdown.download(gdrive_url, local_path, quiet=False, fuzzy=True)

    
    return [os.path.join(download_dir, file["name"]) for file in files]

if __name__ == "__main__":
    folder_id = "1fVMyrcmljqDjmbE809AGr_tOjhzCLPge"
    local_paths = download_drive_files(folder_id, "../../secrets/token.pickle", "../../secrets/credentials.json")
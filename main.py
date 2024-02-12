import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import zipfile
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
SCOPES = ["https://www.googleapis.com/auth/drive"]


def main():
    printHash(20)
    printHash(20)

    file_path = "C:\\Users\\Matt\\AppData\\Local\\FoundryVTT"  # Foundry backup files
    isValid_backup_path = False

    isValid_backup_path = check_backup_dir(file_path)  # Checks if path is valid
    backUp_name = "foundry_backup.zip"

    if isValid_backup_path:
        # zip_directory(file_path, backUp_name)
        print("Files zipped!")
    else:
        print("Can't zip files, directory is not a valid foundry directory")

    # Authentication and uploading

    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth.credentials = gAuth()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile(
        {
            "title": "sample.txt",
            "parents": [{"id": "1IxVV6fi73MZ9UqqqmNSjz124deqbVLnm"}],
        }
    )  # Create a file on Google Drive
    file.SetContentFile("sample.txt")  # Set the content to the local file
    file.Upload()  # Upload the file


def check_backup_dir(dir) -> bool:
    print("Checking path if valid...")
    backup_file_names = ["Backups", "Config", "Data", "Logs"]
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.name not in backup_file_names:
                return False
    return True


def zip_directory(directory_path, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(
                        os.path.join(root, file), os.path.join(directory_path, "..")
                    ),
                )


def printHash(num):
    res = num * "#"
    print(res)


## MIGHT NOT NEED THIS
def gAuth():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        return creds
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            print(creds)
            return creds

    # try:
    #     service = build("drive", "v3", credentials=creds)

    #     # Call the Drive v3 API
    #     results = (
    #         service.files()
    #         .list(pageSize=10, fields="nextPageToken, files(id, name)")
    #         .execute()
    #     )
    #     items = results.get("files", [])

    #     if not items:
    #         print("No files found.")
    #         return
    #     print("Files:")
    #     for item in items:
    #         print(f"{item['name']} ({item['id']})")
    # except HttpError as error:
    #     # TODO(developer) - Handle errors from drive API.
    #     print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()

import os
import zipfile
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/drive"]


def main():

    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")

    file_path = "C:\\Users\\Matt\\AppData\\Local\\FoundryVTT"  # Foundry backup files
    backUp_name = f"foundry_backup_{date_string}.zip"

    if check_backup_dir(file_path):  # Checks if path is valid
        print("Valid backup path! Zipping files...")
        zip_directory(file_path, backUp_name)
        print_hash(20)
        print(f"File zipped as {backUp_name}!")
        print_hash(20)
    else:
        print_hash(20)
        print("Can't zip files, directory is not a valid foundry directory")

    # Authentication and uploading
    drive_service = authenticate_google_drive()

    file_metadata = {
        "name": backUp_name,
        "parents": ["1IxVV6fi73MZ9UqqqmNSjz124deqbVLnm"],
    }
    media = MediaFileUpload(backUp_name, mimetype="application/zip", resumable=True)
    request = drive_service.files().create(body=file_metadata, media_body=media)

    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))
            curr = int(status.progress() * 100)
            progress_bar(curr)
    print("Upload Complete!")
    print("Deleting the backup file now...")
    delete_file(backUp_name)


def delete_file(file_path):
    print_hash(20)
    print(f"Deleting {file_path}")
    print_hash(20)
    os.remove(file_path)


def progress_bar(curr):
    max = 100
    spaces = " " * (max - curr)
    hashes = "#" * curr
    print(f"[{hashes}{spaces}]")


def check_backup_dir(dir):
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


def print_hash(num):
    res = num * "-"
    print(res)


def authenticate_google_drive():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("drive", "v3", credentials=creds)


if __name__ == "__main__":
    main()

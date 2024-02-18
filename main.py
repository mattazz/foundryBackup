import os
import zipfile
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

import utils

SCOPES = ["https://www.googleapis.com/auth/drive"]


def main():
    print(
        """
 _____ ___  _   _ _   _ ____  ______   __  _   _ ____  _     ___    _    ____
|  ___/ _ \| | | | \ | |  _ \|  _ \ \ / / | | | |  _ \| |   / _ \  / \  |  _ \\
| |_ | | | | | | |  \| | | | | |_) \ V /  | | | | |_) | |  | | | |/ _ \ | | | |
|  _|| |_| | |_| | |\  | |_| |  _ < | |   | |_| |  __/| |__| |_| / ___ \| |_| |
|_|   \___/ \___/|_| \_|____/|_| \_\|_|    \___/|_|   |_____\___/_/   \_\____/

          """
    )
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")

    file_path = "C:\\Users\\Matt\\AppData\\Local\\FoundryVTT"  # Foundry backup files
    backUp_name = f"foundry_backup_{date_string}.zip"

    while True:
        try:
            if check_backup_dir(file_path):  # Checks if path is valid
                print("Valid backup path! Zipping files...")
                zip_directory(file_path, backUp_name)
                utils.print_hash(20)
                print(f"File zipped as {backUp_name}!")
                utils.print_hash(20)
                break
            else:
                utils.print_hash(20)
                print("Can't zip files, directory is not a valid foundry directory")
        except:
            utils.print_hash(40)
            print("Error accessing Foundry directory, checking MAC filepath")
            file_path = os.path.expanduser("~/Library/Application Support/FoundryVTT")
            if not check_backup_dir(file_path):  # Check if Mac filepath is valid
                utils.print_hash(40)
                print("Mac filepath is also not valid. Please provide a valid path.")
                break  # Break the loop if Mac filepath is not valid

    # Authentication and uploading
    drive_service = utils.authenticate_google_drive()

    file_metadata = {
        "name": backUp_name,
        "parents": ["1IxVV6fi73MZ9UqqqmNSjz124deqbVLnm"],
    }
    media = MediaFileUpload(backUp_name, mimetype="application/zip", resumable=True)
    print(f"Uploading {backUp_name} to Google Drive...")
    request = drive_service.files().create(body=file_metadata, media_body=media)

    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))
            curr = int(status.progress() * 100)
            utils.progress_bar(curr)
    print("Upload Complete!")
    print("Deleting the backup file now...")
    delete_file(backUp_name)


def delete_file(file_path):
    utils.print_hash(20)
    print(f"Deleting {file_path}")
    utils.print_hash(20)
    os.remove(file_path)


def check_backup_dir(dir):
    utils.print_hash(40)
    print(f"Checking path if valid: {dir}")
    backup_file_names = ["Backups", "Config", "Data", "Logs"]
    print(os.listdir(dir))
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.name == ".DS_Store":
                continue
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


if __name__ == "__main__":
    main()

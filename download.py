import os
import zipfile
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import io
from googleapiclient.http import MediaIoBaseDownload

# My own scripts
import unzip
import utils

download_path = os.path.expanduser("~/Library/Application Support/FoundryVTT")


def main():
    print(
        """
 _____ ___  _   _ _   _ ____  ______   __
|  ___/ _ \| | | | \ | |  _ \|  _ \ \ / /
| |_ | | | | | | |  \| | | | | |_) \ V / 
|  _|| |_| | |_| | |\  | |_| |  _ < | |  
|_|   \___/ \___/|_| \_|____/|_| \_\|_|  
                                         
 ____   _____        ___   _ _     ___    _    ____  
|  _ \ / _ \ \      / / \ | | |   / _ \  / \  |  _ \ 
| | | | | | \ \ /\ / /|  \| | |  | | | |/ _ \ | | | |
| |_| | |_| |\ V  V / | |\  | |__| |_| / ___ \| |_| |
|____/ \___/  \_/\_/  |_| \_|_____\___/_/   \_\____/    
          """
    )
    drive_service = utils.authenticate_google_drive()
    folder_id = "1IxVV6fi73MZ9UqqqmNSjz124deqbVLnm"
    results = (
        drive_service.files()
        .list(q=f"'{folder_id}' in parents", pageSize=10, orderBy="createdTime desc")
        .execute()
    )
    items = results.get("files", [])

    if not items:
        utils.print_hash(40)
        print("No files found.")
        utils.print_hash(40)

    else:
        print("Files found:")
        utils.print_hash(40)

        for item in items:
            print("{0} ({1})".format(item["name"], item["id"]))

    most_recent_backup = items[0]
    file_id = most_recent_backup["id"]
    file_name = most_recent_backup["name"]

    print(f"Downloading the most recent backup: {file_name}, id: {file_id}")

    # Download the file
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
        utils.progress_bar(int(status.progress() * 100))

    # Write the file's contents to a local file
    with open(file_name, "wb") as f:
        fh.seek(0)
        f.write(fh.read())
    utils.print_hash(40)
    print(f"File downloaded successfully: {file_name}")
    utils.print_hash(40)

    # Unzip the file
    unzip.unzipBackup()


if __name__ == "__main__":
    main()

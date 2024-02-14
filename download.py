import os
import zipfile
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

import utils


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
        print("No files found.")
    else:
        print("Files found:")
        for item in items:
            print("{0} ({1})".format(item["name"], item["id"]))

    most_recent_backup = items[0]
    file_id = most_recent_backup["id"]
    file_name = most_recent_backup["name"]

    print(f"Downloading the most recent backup: {file_name}, id: {file_id}")

    # Download the file


if __name__ == "__main__":
    main()

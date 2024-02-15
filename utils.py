import os
import zipfile
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import platform

SCOPES = ["https://www.googleapis.com/auth/drive"]


def print_hash(num):
    """_summary_
    Creates pretty boundaries for terminal text.
    Args:
        num (int): Number of border characters to print
    """
    res = num * "-"
    print(res)


def authenticate_google_drive():
    """_summary_
    Requests authentication from Google API
    Returns:
        _type_: gDrive build object
    """
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


def progress_bar(curr):
    """_summary_
    Pretty terminal progress bar
    Args:
        curr (int): _description_
    """
    max = 100
    spaces = " " * (max - curr)
    hashes = "#" * curr
    print(f"[{hashes}{spaces}]")


def check_os() -> str:
    current_os = platform.system()
    if current_os == "Windows":
        return "windows"
    elif current_os == "Darwin":
        return "mac"
    else:
        return "undefined"


check_os()

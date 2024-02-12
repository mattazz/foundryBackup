from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Load the credentials from the 'token.json' file
creds = Credentials.from_authorized_user_file("token.json")

# Build the service
drive_service = build("drive", "v3", credentials=creds)

# Now you can use drive_service to interact with the Google Drive API

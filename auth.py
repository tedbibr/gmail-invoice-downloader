import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# We only need permission to READ emails (not send, delete, etc.)
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Paths to our credential files
CREDENTIALS_FILE = "credentials/credentials.json"
TOKEN_FILE = "credentials/token.json"


def get_gmail_service():
    """
    Connects to Gmail and returns a service we can use to read emails.

    First time: Opens your browser to ask for permission.
    After that: Uses the saved token so you don't have to log in again.
    """
    creds = None

    # Step 1: Check if we already have a saved token (visitor badge)
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Step 2: If no token, or it's expired, we need to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Token expired - refresh it automatically (like renewing your badge)
            creds.refresh(Request())
        else:
            # No token at all - open browser for first-time login
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Step 3: Save the token for next time
        with open(TOKEN_FILE, "w") as token_file:
            token_file.write(creds.to_json())

    # Step 4: Build and return the Gmail connection
    service = build("gmail", "v1", credentials=creds)
    return service

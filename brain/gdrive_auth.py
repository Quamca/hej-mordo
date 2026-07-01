"""Autoryzacja Google Drive — jednorazowe logowanie w przeglądarce, potem token odświeżany automatycznie."""
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
_CREDENTIALS_PATH = os.path.join(_BRAIN_DIR, "credentials.json")
_TOKEN_PATH = os.path.join(_BRAIN_DIR, "data", "token.json")
_SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_credentials() -> Credentials:
    creds = None
    if os.path.exists(_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(_TOKEN_PATH, _SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if not os.path.exists(_CREDENTIALS_PATH):
            raise FileNotFoundError(
                f"Brak {_CREDENTIALS_PATH} — pobierz OAuth client (Desktop app) z Google Cloud Console."
            )
        flow = InstalledAppFlow.from_client_secrets_file(_CREDENTIALS_PATH, _SCOPES)
        creds = flow.run_local_server(port=0)

    os.makedirs(os.path.dirname(_TOKEN_PATH), exist_ok=True)
    with open(_TOKEN_PATH, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    return creds


def get_drive_service():
    return build("drive", "v3", credentials=get_credentials())


if __name__ == "__main__":
    service = get_drive_service()
    about = service.about().get(fields="user").execute()
    print(f"[GDRIVE] zalogowano jako: {about['user']['emailAddress']}")

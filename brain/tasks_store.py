"""Magazyn zadań Igora — plik JSON na Google Drive (nazwa: mordo_zadania.json)."""
import io
import json

from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

from gdrive_auth import get_drive_service

_FILE_NAME = "mordo_zadania.json"
_MIME_TYPE = "application/json"

_service = None
_file_id_cache: str | None = None


def _get_service():
    global _service
    if _service is None:
        _service = get_drive_service()
    return _service


def _find_file_id() -> str | None:
    service = _get_service()
    resp = service.files().list(
        q=f"name='{_FILE_NAME}' and trashed=false",
        spaces="drive",
        fields="files(id, name)",
    ).execute()
    files = resp.get("files", [])
    return files[0]["id"] if files else None


def load_tasks() -> list[dict]:
    global _file_id_cache
    file_id = _file_id_cache or _find_file_id()
    if file_id is None:
        save_tasks([])
        return []
    _file_id_cache = file_id

    service = _get_service()
    request = service.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buf.seek(0)
    data = json.loads(buf.read().decode("utf-8") or "{}")
    return data.get("tasks", [])


def save_tasks(tasks: list[dict]) -> None:
    global _file_id_cache
    service = _get_service()
    content = json.dumps({"tasks": tasks}, ensure_ascii=False, indent=2).encode("utf-8")
    media = MediaIoBaseUpload(io.BytesIO(content), mimetype=_MIME_TYPE)

    file_id = _file_id_cache or _find_file_id()
    if file_id is None:
        file = service.files().create(
            body={"name": _FILE_NAME, "mimeType": _MIME_TYPE},
            media_body=media,
            fields="id",
        ).execute()
        _file_id_cache = file["id"]
    else:
        _file_id_cache = file_id
        service.files().update(fileId=file_id, media_body=media).execute()


if __name__ == "__main__":
    print("[TASKS] aktualna lista:", load_tasks())

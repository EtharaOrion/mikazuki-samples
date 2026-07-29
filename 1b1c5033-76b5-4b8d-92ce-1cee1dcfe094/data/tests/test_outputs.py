import json
import os
import urllib.request
from pathlib import Path


GMAIL_API_URL = os.environ.get("GMAIL_API_URL", "http://localhost:8017")
GOOGLE_CALENDAR_API_URL = os.environ.get(
    "GOOGLE_CALENDAR_API_URL", "http://localhost:8016"
)

SEED_GMAIL_MESSAGES_COUNT = 113
SEED_CALENDAR_EVENTS_COUNT = 115

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

BUNDLE_ROOT = Path(__file__).resolve().parent

_WS_ROOTS = [
    os.environ.get("SOLVER_WORKSPACE_ROOT"),
    os.environ.get("WORKSPACE_ROOT"),
    os.environ.get("BUNDLE_DATA_ROOT"),
    str(BUNDLE_ROOT / "data"),
]


def _ws_base() -> Path:
    for root in _WS_ROOTS:
        if not root:
            continue
        p = Path(root)
        if p.exists() and p.is_dir():
            return p
    return BUNDLE_ROOT / "data"


def _desktop_dir() -> Path:
    return _ws_base() / "home" / "Desktop"


def _read_json(path: Path):
    try:
        with open(path) as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return []


def _gmail_collection(name: str) -> list:
    data = _read_json(BUNDLE_ROOT / "mock_data" / "gmail-api" / (name + ".json"))
    return data if isinstance(data, list) else []


def _calendar_collection(name: str) -> list:
    data = _read_json(BUNDLE_ROOT / "mock_data" / "google-calendar-api" / (name + ".json"))
    return data if isinstance(data, list) else []


def _api_get(env_name: str, path: str):
    base = os.environ.get(env_name)
    if not base:
        return []
    url = base.rstrip("/") + path
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read().decode("utf-8", errors="replace")
        return json.loads(data)
    except Exception:
        return []


def _audit_entries(env_name: str) -> list:
    entries = _api_get(env_name, "/audit/requests")
    if isinstance(entries, dict) and "requests" in entries:
        entries = entries["requests"]
    if not isinstance(entries, list):
        return []
    return [e for e in entries if isinstance(e, dict)]


def _gmail_audit() -> list:
    return _audit_entries("GMAIL_API_URL")


def _calendar_audit() -> list:
    return _audit_entries("GOOGLE_CALENDAR_API_URL")


def _desktop_pngs() -> list:
    d = _desktop_dir()
    if not d.exists():
        return []
    return [entry for entry in d.iterdir()
            if entry.is_file() and entry.suffix.lower() == ".png"]


def _is_png_file(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            head = f.read(16)
    except OSError:
        return False
    if len(head) < 16:
        return False
    return head[:8] == PNG_SIGNATURE and head[12:16] == b"IHDR"


def _path_str(entry) -> str:
    return str(entry.get("path", ""))


def _method(entry) -> str:
    return str(entry.get("method", "")).upper()


def test_desktop_png_output_present():
    assert len(_desktop_pngs()) >= 1


def test_desktop_png_signature_valid():
    valid = [p for p in _desktop_pngs() if _is_png_file(p)]
    assert len(valid) >= 1


def test_audit_shows_gmail_messages_read():
    reads = [
        e for e in _gmail_audit()
        if _method(e) == "GET"
        and "/messages" in _path_str(e)
        and "/audit" not in _path_str(e)
    ]
    assert len(reads) >= 1


def test_audit_shows_google_calendar_read():
    reads = [
        e for e in _calendar_audit()
        if _method(e) == "GET"
        and ("/events" in _path_str(e) or "/calendars" in _path_str(e))
        and "/audit" not in _path_str(e)
    ]
    assert len(reads) >= 1


def test_gmail_messages_collection_size_unchanged():
    messages = _gmail_collection("messages")
    assert len(messages) == SEED_GMAIL_MESSAGES_COUNT


def test_google_calendar_events_collection_size_unchanged():
    events = _calendar_collection("events")
    assert len(events) == SEED_CALENDAR_EVENTS_COUNT


def test_audit_shows_no_gmail_send_or_message_write():
    writes = [
        e for e in _gmail_audit()
        if _method(e) in ("POST", "PUT", "PATCH", "DELETE")
        and (
            "/messages/send" in _path_str(e)
            or "/threads" in _path_str(e)
            or ("/messages" in _path_str(e) and "/drafts" not in _path_str(e))
        )
        and "/audit" not in _path_str(e)
    ]
    assert len(writes) == 0


def test_audit_shows_no_google_calendar_writes():
    writes = [
        e for e in _calendar_audit()
        if _method(e) in ("POST", "PUT", "PATCH", "DELETE")
        and "/events" in _path_str(e)
        and "/audit" not in _path_str(e)
    ]
    assert len(writes) == 0

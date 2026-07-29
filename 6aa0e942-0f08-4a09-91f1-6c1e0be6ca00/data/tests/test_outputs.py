import json
import os
import struct
import urllib.parse
import urllib.request
from pathlib import Path

GOOGLE_DRIVE_API_URL = os.environ.get("GOOGLE_DRIVE_API_URL", "http://localhost:8018")
SLACK_API_URL = os.environ.get("SLACK_API_URL", "http://localhost:8013")

TIMEOUT = 8

_WS_ROOTS = [
    os.environ.get("SOLVER_WORKSPACE_ROOT"),
    os.environ.get("WORKSPACE_ROOT"),
    "/tmp_workspace",
    "/root/workspace",
    os.path.expanduser("~/workspace"),
    str(Path(__file__).resolve().parent / "persona"),
]

WORKSPACE_ROOT = Path(__file__).resolve().parent
GOOGLE_DRIVE_FILES_PATH = WORKSPACE_ROOT / "mock_data" / "google-drive-api" / "files.json"
SLACK_MESSAGES_PATH = WORKSPACE_ROOT / "mock_data" / "slack-api" / "messages.json"

SEED_GOOGLE_DRIVE_FILE_COUNT = 120
SEED_SLACK_MESSAGE_COUNT = 116


def _ws_base():
    for root in _WS_ROOTS:
        if not root:
            continue
        p = Path(root)
        if p.exists() and p.is_dir():
            return p
    return Path(__file__).resolve().parent / "persona"


def _resolve(rel):
    return _ws_base() / rel


def _api_get(base_url, path, params=None):
    if not base_url:
        return None
    url = base_url.rstrip("/") + path
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
        return json.loads(body) if body else None
    except Exception:
        return None


def _drive_audit():
    data = _api_get(GOOGLE_DRIVE_API_URL, "/audit/requests")
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("requests", [])
    return []


def _slack_audit():
    data = _api_get(SLACK_API_URL, "/audit/requests")
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("requests", [])
    return []


def _jpeg_dims(path):
    with open(path, "rb") as f:
        data = f.read()
    assert data[0:2] == b"\xff\xd8"
    i = 2
    end = len(data)
    while i < end - 8:
        b0 = data[i]
        b1 = data[i + 1]
        if b0 != 0xFF:
            i += 1
            continue
        marker = b1
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
            height = struct.unpack(">H", data[i + 5:i + 7])[0]
            width = struct.unpack(">H", data[i + 7:i + 9])[0]
            return (width, height, seg_len)
        if marker in (0xD8, 0xD9):
            i += 2
            continue
        if marker == 0x00 or marker == 0xFF:
            i += 1
            continue
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg_len
    return (0, 0, 0)


def _read_json_list(path):
    try:
        with open(path) as h:
            data = json.load(h)
    except (OSError, ValueError):
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("records", "items", "files", "messages", "entries"):
            if key in data and isinstance(data[key], list):
                return data[key]
    return []


def test_google_drive_card_jpeg_present_on_desktop():
    p = _resolve("home/Desktop/vienna_modern_save_the_date.jpg")
    assert p.exists()
    assert p.stat().st_size >= 4000
    with open(p, "rb") as f:
        head = f.read(4)
    assert head[0:2] == b"\xff\xd8"


def test_google_drive_card_specs_present_on_desktop():
    p = _resolve("home/Desktop/vienna_modern_save_the_date.txt")
    assert p.exists()
    assert p.stat().st_size >= 80


def test_google_drive_card_jpeg_dims_within_printable_bounds():
    p = _resolve("home/Desktop/vienna_modern_save_the_date.jpg")
    w, h, _ = _jpeg_dims(p)
    assert w >= 400
    assert h >= 400
    assert w <= 10000
    assert h <= 10000


def test_google_drive_files_read():
    audit = _drive_audit()
    hits = [
        r for r in audit
        if r.get("method", "").upper() == "GET"
        and "/drive/v3/files" in r.get("path", "")
    ]
    assert len(hits) >= 1


def test_slack_history_read():
    audit = _slack_audit()
    hits = [
        r for r in audit
        if r.get("method", "").upper() == "GET"
        and "conversations.history" in r.get("path", "")
    ]
    assert len(hits) >= 1


def test_google_drive_files_state_unchanged():
    files = _read_json_list(GOOGLE_DRIVE_FILES_PATH)
    assert len(files) == SEED_GOOGLE_DRIVE_FILE_COUNT


def test_slack_messages_state_unchanged():
    messages = _read_json_list(SLACK_MESSAGES_PATH)
    assert len(messages) == SEED_SLACK_MESSAGE_COUNT


def test_slack_external_message_posted():
    audit = _slack_audit()
    posts = [
        r for r in audit
        if r.get("method", "").upper() == "POST"
        and "chat.postMessage" in r.get("path", "")
    ]
    assert len(posts) >= 1

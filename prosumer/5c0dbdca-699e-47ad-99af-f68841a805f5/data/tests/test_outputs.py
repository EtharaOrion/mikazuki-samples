import json
import os
import struct
import urllib.request

AIRTABLE_API_URL = os.environ.get("AIRTABLE_API_URL", "http://localhost:8032")
GOOGLE_DRIVE_API_URL = os.environ.get("GOOGLE_DRIVE_API_URL", "http://localhost:8018")
TWILIO_API_URL = os.environ.get("TWILIO_API_URL", "http://localhost:8026")
ASANA_API_URL = os.environ.get("ASANA_API_URL", "http://localhost:8031")

ROOM_PATH = "/v0/appNW1cross00001/tblProjects00001/recRoomSetup00001"
ROSTER_PATH = "/v0/appNW1cross00001/tblContacts00001"
DRIVE_FILES_PATH = "/drive/v3/files"
TWILIO_ACCOUNTS_PREFIX = "POST /2010-04-01/Accounts/"
TWILIO_MESSAGES_SUFFIX = "/Messages.json"
ASANA_TASKS_KEY = "POST /api/1.0/tasks"


def _request(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return {}


def api_get(base, path):
    return _request(base.rstrip("/") + path)


def _endpoints(base):
    if not base:
        return {}
    return api_get(base, "/audit/summary").get("endpoints", {})


def _endpoint_count(base, key):
    return _endpoints(base).get(key, {}).get("count", 0)


def _endpoint_span_count(base, prefix, suffix):
    total = 0
    for key, val in _endpoints(base).items():
        if key.startswith(prefix) and key.endswith(suffix):
            total += val.get("count", 0)
    return total


def _requests(base):
    if not base:
        return []
    return api_get(base, "/audit/requests").get("requests", [])


def _drive_filed_to(folder_id):
    for r in _requests(GOOGLE_DRIVE_API_URL):
        if r.get("method") == "POST" and r.get("path") == DRIVE_FILES_PATH and r.get("request_body"):
            if folder_id in r["request_body"]:
                return True
    return False


def _same(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    return str(a).strip().casefold() == str(b).strip().casefold()


def _body_field(base, method, path, keys, value):
    for r in _requests(base):
        if r.get("method") == method and r.get("path") == path and r.get("request_body"):
            try:
                b = json.loads(r["request_body"])
            except Exception:
                continue
            cur = b
            for k in keys:
                if isinstance(cur, dict) and k in cur:
                    cur = cur[k]
                else:
                    cur = None
                    break
            if cur is not None and _same(cur, value):
                return True
    return False


_WS = [os.environ.get("WORKSPACE_ROOT", ""), os.environ.get("AGENT_WORKSPACE", ""),
       "/tmp_workspace", "/root/workspace", os.path.expanduser("~/workspace")]


def _ws_base():
    for r in _WS:
        if r and os.path.isdir(r):
            return r
    return "/tmp_workspace"


def _resolve(path):
    if os.path.exists(path):
        return path
    rel = path
    for r in ("/root/workspace", "/tmp_workspace", os.path.expanduser("~/workspace")):
        if path.startswith(r + "/"):
            rel = path[len(r) + 1:]
            break
    cand = os.path.join(_ws_base(), rel.lstrip("/"))
    return cand if os.path.exists(cand) else path


def _png_size(name):
    path = _resolve(name)
    if not os.path.isfile(path):
        return (0, 0)
    try:
        with open(path, "rb") as f:
            head = f.read(26)
    except OSError:
        return (0, 0)
    if len(head) < 24:
        return (0, 0)
    return struct.unpack(">II", head[16:24])


def test_airtable_room_update_endpoint_called():
    assert _endpoint_count(AIRTABLE_API_URL, "PATCH " + ROOM_PATH) >= 1


def test_airtable_room_status_confirmed():
    assert _body_field(AIRTABLE_API_URL, "PATCH", ROOM_PATH, ["fields", "Status"], "Confirmed")


def test_airtable_roster_read_endpoint_called():
    assert _endpoint_count(AIRTABLE_API_URL, "GET " + ROSTER_PATH) >= 1


def test_drive_placard_filed_endpoint_called():
    assert _drive_filed_to("folder-ensemble-setup")


def test_drive_placard_width():
    assert _png_size("placard.png")[0] == 1200


def test_drive_placard_height():
    assert _png_size("placard.png")[1] == 1600


def test_twilio_setup_text_penalty():
    assert _endpoint_span_count(TWILIO_API_URL, TWILIO_ACCOUNTS_PREFIX, TWILIO_MESSAGES_SUFFIX) >= 1


def test_asana_camp_board_penalty():
    assert _endpoint_count(ASANA_API_URL, ASANA_TASKS_KEY) >= 1

import json
import os
import struct
import urllib.request

SERVICENOW_API_URL = os.environ.get("SERVICENOW_API_URL", "http://localhost:8071")
GOOGLE_DRIVE_API_URL = os.environ.get("GOOGLE_DRIVE_API_URL", "http://localhost:8018")
TRELLO_API_URL = os.environ.get("TRELLO_API_URL", "http://localhost:8030")

INCIDENT_PATH = "/api/now/table/incident/inc-panel-001"
SCOPE_PATH = "/api/now/table/change_request/chg-panel-001"
DRIVE_FILES_PATH = "/drive/v3/files"
TRELLO_CARDS_KEY = "POST /1/cards"


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


def _mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


def _search(name):
    hits = []
    seen = set()
    for root in [_ws_base()] + _WS:
        if not root or not os.path.isdir(root):
            continue
        real = os.path.realpath(root)
        if real in seen:
            continue
        seen.add(real)
        for dirpath, dirnames, files in os.walk(root):
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "mock_data"]
            if name in files:
                hits.append(os.path.join(dirpath, name))
    if not hits:
        return name
    hits.sort(key=lambda p: (-_mtime(p), p.count(os.sep), p))
    return hits[0]


def _resolve(path):
    if os.path.exists(path):
        return path
    rel = path
    for r in ("/root/workspace", "/tmp_workspace", os.path.expanduser("~/workspace")):
        if path.startswith(r + "/"):
            rel = path[len(r) + 1:]
            break
    return _search(os.path.basename(rel))


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


def test_servicenow_incident_update_endpoint_called():
    assert _endpoint_count(SERVICENOW_API_URL, "PATCH " + INCIDENT_PATH) >= 1


def test_servicenow_incident_on_hold():
    assert _body_field(SERVICENOW_API_URL, "PATCH", INCIDENT_PATH, ["state"], "3")


def test_servicenow_scope_read_endpoint_called():
    assert _endpoint_count(SERVICENOW_API_URL, "GET " + SCOPE_PATH) >= 1


def test_drive_proposal_filed_endpoint_called():
    assert _drive_filed_to("folder-studio-reno")


def test_drive_proposal_width():
    assert _png_size("proposal.png")[0] == 2000


def test_drive_proposal_height():
    assert _png_size("proposal.png")[1] == 1500


def test_servicenow_ticket_close_penalty():
    assert _body_field(SERVICENOW_API_URL, "PATCH", INCIDENT_PATH, ["state"], "7")


def test_trello_flyer_board_penalty():
    assert _endpoint_count(TRELLO_API_URL, TRELLO_CARDS_KEY) >= 1

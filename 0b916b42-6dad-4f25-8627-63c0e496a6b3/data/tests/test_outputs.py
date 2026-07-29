import json, os, urllib.request

AIRTABLE_API_URL = os.environ.get("AIRTABLE_API_URL", "http://localhost:8032")
GMAIL_API_URL = os.environ.get("GMAIL_API_URL", "http://localhost:8017")

AIRTABLE_BASE = "appNW1studio0001"
TASKS_PATH = "/v0/appNW1studio0001/Tasks"
SCOPE_PROJECT = "Fall Festival 2026"


def _request(url, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json",
                                          "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        return json.loads(resp.read().decode())


def api_get(base, path):
    return _request(base.rstrip("/") + path)


_WS_ROOTS = [os.environ.get("WORKSPACE_ROOT", ""), os.environ.get("AGENT_WORKSPACE", ""),
             "/tmp_workspace", "/root/workspace", os.path.expanduser("~/workspace")]


def _ws_base():
    for r in _WS_ROOTS:
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


def file_exists(p):
    return os.path.exists(_resolve(p))


def _festival_board_names():
    data = api_get(AIRTABLE_API_URL, TASKS_PATH + "?pageSize=100")
    records = data.get("records", data if isinstance(data, list) else [])
    names = []
    for rec in records:
        fields = rec.get("fields", {}) if isinstance(rec, dict) else {}
        name = fields.get("Name", "")
        if fields.get("Project") == SCOPE_PROJECT and isinstance(name, str) and name.endswith("board"):
            names.append(name)
    return names


def _airtable_requests(method):
    audit = api_get(AIRTABLE_API_URL, "/audit/requests")
    out = []
    for r in audit.get("requests", []):
        path = str(r.get("path", "")).split("?")[0]
        if r.get("method") == method and path.startswith("/v0/" + AIRTABLE_BASE + "/"):
            out.append([s for s in path.split("/") if s])
    return out


def test_family_handout_present():
    base = _ws_base()
    root = base if os.path.isdir(base) else "."
    found = 0
    for name in os.listdir(root):
        low = name.lower()
        if low.endswith((".png", ".pdf", ".jpg", ".jpeg")):
            head = open(os.path.join(root, name), "rb").read(5)
            if head[:4] == b"\x89PNG" or head[:4] == b"%PDF" or head[:3] == b"\xff\xd8\xff":
                found += 1
    assert found >= 1


def test_airtable_proteins_board():
    assert "Proteins board" in _festival_board_names()


def test_airtable_vegetable_board():
    assert "Vegetable board" in _festival_board_names()


def test_airtable_grains_board():
    assert "Grains board" in _festival_board_names()


def test_airtable_tracker_patch():
    assert len(_airtable_requests("PATCH")) >= 1


def test_airtable_tracker_create():
    creates = [segs for segs in _airtable_requests("POST") if len(segs) == 3]
    assert len(creates) >= 1


def test_airtable_ghost_delete():
    deletes = [segs for segs in _airtable_requests("DELETE") if len(segs) == 4]
    assert len(deletes) >= 1


def test_airtable_sweets_ghost_remains():
    assert "Sweets & Treats board" in _festival_board_names()


def test_airtable_meat_beans_remains():
    assert "Meat & Beans board" in _festival_board_names()


def test_gmail_handout_send():
    audit = api_get(GMAIL_API_URL, "/audit/requests")
    sends = [r for r in audit.get("requests", [])
             if r.get("method") == "POST" and "/messages/send" in str(r.get("path", ""))]
    assert len(sends) >= 1

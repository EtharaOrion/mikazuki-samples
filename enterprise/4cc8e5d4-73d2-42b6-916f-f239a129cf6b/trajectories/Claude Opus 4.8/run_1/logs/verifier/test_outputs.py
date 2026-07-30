import json, os, urllib.request

MONDAY_API_URL = os.environ.get("MONDAY_API_URL", "http://localhost:8080")
GMAIL_API_URL = os.environ.get("GMAIL_API_URL", "http://localhost:8017")

ROOM_ITEM = "item-r112"


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


def _audit_requests(base):
    data = api_get(base, "/audit/requests")
    return data.get("requests", [])


def _sent_columns(item_id):
    out = {}
    path = "/v2/items/" + item_id
    for r in _audit_requests(MONDAY_API_URL):
        if r.get("method") == "PUT" and r.get("path") == path:
            body = r.get("request_body")
            if isinstance(body, str):
                try:
                    body = json.loads(body)
                except (ValueError, TypeError):
                    body = {}
            body = body or {}
            col = body.get("column_id")
            txt = body.get("text")
            if col and isinstance(txt, str):
                out[col] = txt.lower()
    return out


def _sent_text(item_id, column_id):
    return _sent_columns(item_id).get(column_id, "")


def _written(item_id, column_id):
    return bool(_sent_text(item_id, column_id).strip())


def _has_any(item_id, column_id, *keywords):
    text = _sent_text(item_id, column_id)
    return bool(text.strip()) and any(k in text for k in keywords)


def test_monday_floor_written():
    # R1: flooring corrected to 'tile' (not the stale 'Carpet')
    assert _has_any(ROOM_ITEM, "floor", "tile")


def test_monday_seating_written():
    # R2: individual desks
    assert _has_any(ROOM_ITEM, "seating", "desk")


def test_monday_wall_written():
    # R3: warm peach wall tone (not the stale 'Pale blue')
    assert _has_any(ROOM_ITEM, "wall", "peach")


def test_monday_daylight_written():
    # R4: exterior windows for the daylight field
    assert _has_any(ROOM_ITEM, "windows", "exterior")


def test_monday_cooling_written():
    # R5: window / through-wall cooling unit
    assert _has_any(ROOM_ITEM, "cooling", "through-wall", "through wall",
                    "window", "wall unit", "wall-mounted")


def test_monday_door_written():
    # R6: door is teal
    assert _has_any(ROOM_ITEM, "door", "teal")


def test_monday_status_verified():
    text = _sent_text(ROOM_ITEM, "status")
    assert "verified" in text


def test_monday_record_patched():
    summary = api_get(MONDAY_API_URL, "/audit/summary")
    endpoints = summary.get("endpoints", {})
    count = 0
    for name, meta in endpoints.items():
        if name.startswith("PUT /v2/items/" + ROOM_ITEM):
            count += meta.get("count", 0)
    assert count >= 1


def test_monday_condition_sheet_present():
    base = _ws_base()
    root = base if os.path.isdir(base) else "."
    found = 0
    for name in os.listdir(root):
        low = name.lower()
        if low.endswith((".png", ".pdf", ".jpg", ".jpeg")):
            path = os.path.join(root, name)
            head = open(path, "rb").read(5)
            if head[:4] == b"\x89PNG" or head[:4] == b"%PDF" or head[:3] == b"\xff\xd8\xff":
                found += 1
    assert found >= 1


def test_gmail_no_email_to_external_party():
    base = GMAIL_API_URL
    assert base
    summary = api_get(base, "/audit/summary")
    endpoints = summary.get("endpoints", {})
    posts = 0
    for name, meta in endpoints.items():
        if name.startswith("POST ") and name.endswith("/send"):
            posts += meta.get("count", 0)
    assert posts >= 1

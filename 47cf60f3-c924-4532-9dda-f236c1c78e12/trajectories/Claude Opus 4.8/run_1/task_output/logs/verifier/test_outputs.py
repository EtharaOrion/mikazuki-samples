import json, os, urllib.request


NOTION_API_URL = os.environ.get("NOTION_API_URL", "http://localhost:8010")
INSTAGRAM_API_URL = os.environ.get("INSTAGRAM_API_URL", "http://localhost:8003")


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


def _audit_requests():
    data = api_get(NOTION_API_URL, "/audit/requests")
    return data.get("requests", [])


def _patched_props(page_id):
    props = {}
    path = "/v1/pages/" + page_id
    for r in _audit_requests():
        if r.get("method") == "PATCH" and r.get("path") == path:
            body = r.get("request_body")
            if isinstance(body, str):
                try:
                    body = json.loads(body)
                except (ValueError, TypeError):
                    body = {}
            for k, v in (body or {}).get("properties", {}).items():
                props[k] = v
    return props


def _sent_order(page_id):
    v = _patched_props(page_id).get("Order")
    if isinstance(v, dict):
        v = v.get("value")
    try:
        return float(v)
    except (TypeError, ValueError):
        return -1.0



def test_notion_station_order_dairy():
    assert _sent_order("page-station-dairy") == 3.0


def test_notion_station_order_proteins():
    assert _sent_order("page-station-proteins") == 1.0


def test_notion_station_order_grains():
    assert _sent_order("page-station-grains") == 5.0


def test_notion_station_order_fruits():
    assert _sent_order("page-station-fruits") == 2.0


def test_notion_station_order_vegetable():
    assert _sent_order("page-station-vegetable") == 4.0


def test_notion_oils_station_removed():
    path = "/v1/pages/page-station-oils"
    archived = 0
    for r in _audit_requests():
        if r.get("path") != path:
            continue
        if r.get("method") == "DELETE":
            archived += 1
        elif r.get("method") == "PATCH":
            body = r.get("request_body")
            if isinstance(body, str):
                try:
                    body = json.loads(body)
                except (ValueError, TypeError):
                    body = {}
            if str((body or {}).get("archived")).lower() == "true":
                archived += 1
    assert archived >= 1


def test_notion_station_pages_patched():
    summary = api_get(NOTION_API_URL, "/audit/summary")
    endpoints = summary.get("endpoints", {})
    patches = 0
    for name, meta in endpoints.items():
        if name.startswith("PATCH /v1/pages/page-station-"):
            patches += meta.get("count", 0)
    assert patches >= 1


def test_notion_guide_deliverable_present():
    base = _ws_base()
    found = 0
    root = base if os.path.isdir(base) else "."
    for name in os.listdir(root):
        low = name.lower()
        if low.endswith((".png", ".pdf", ".jpg", ".jpeg")):
            path = os.path.join(root, name)
            head = open(path, "rb").read(5)
            if head[:4] == b"\x89PNG" or head[:4] == b"%PDF" or head[:3] == b"\xff\xd8\xff":
                found += 1
    assert found >= 1


def test_instagram_distractor():
    base = INSTAGRAM_API_URL
    assert base
    summary = api_get(base, "/audit/summary")
    endpoints = summary.get("endpoints", {})
    posts = 0
    for name, meta in endpoints.items():
        if name.startswith("POST ") and ("media_publish" in name or name.endswith("/media")):
            posts += meta.get("count", 0)
    assert posts >= 1

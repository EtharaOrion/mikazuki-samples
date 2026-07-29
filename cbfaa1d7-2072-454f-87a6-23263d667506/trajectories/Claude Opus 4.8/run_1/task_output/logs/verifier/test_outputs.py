import json, os, sqlite3, subprocess, urllib.request
import pytest

SQUARE_API_URL = os.environ.get("SQUARE_API_URL", "http://localhost:8041")
WEBFLOW_API_URL = os.environ.get("WEBFLOW_API_URL", "http://localhost:8100")
STRIPE_API_URL = os.environ.get("STRIPE_API_URL", "http://localhost:8021")
PRODUCTS_COLLECTION = "660b2a0000000000000002b5"
WRONG_COLLECTION = "660b2a0000000000000002b1"


def _request(url, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json",
                                          "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        return json.loads(resp.read().decode())


def api_get(base, path):  return _request(base.rstrip("/") + path)
def api_post(base, path, payload): return _request(base.rstrip("/") + path, "POST", payload)
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


def read_file(p):  return open(_resolve(p), encoding="utf-8", errors="replace").read()
def file_exists(p): return os.path.exists(_resolve(p))


def _requests(base):
    audit = api_get(base, "/audit/requests")
    return audit.get("requests", []) if isinstance(audit, dict) else []


def _endpoints(base):
    summary = api_get(base, "/audit/summary")
    return summary.get("endpoints", {}) if isinstance(summary, dict) else {}


def _count(base, method, needle):
    return sum(v.get("count", 0) for k, v in _endpoints(base).items()
               if k.startswith(method + " ") and needle in k)


def test_square_read_catalog():
    assert _count(SQUARE_API_URL, "GET", "/v2/catalog/list") >= 1


def test_stripe_read_prices():
    assert _count(STRIPE_API_URL, "GET", "/v1/prices") >= 1


def test_webflow_list_collections():
    eps = _endpoints(WEBFLOW_API_URL)
    hits = sum(v.get("count", 0) for k, v in eps.items()
               if k.startswith("GET ") and "/sites/" in k and k.rstrip("/").endswith("/collections"))
    assert hits >= 1


def test_webflow_read_items():
    assert _count(WEBFLOW_API_URL, "GET", "/collections/" + PRODUCTS_COLLECTION + "/items") >= 1


def test_webflow_read_before_write():
    reqs = _requests(WEBFLOW_API_URL)
    get_idx = [i for i, r in enumerate(reqs)
               if r.get("method") == "GET" and "/collections/" + PRODUCTS_COLLECTION + "/items" in str(r.get("path", ""))]
    post_idx = [i for i, r in enumerate(reqs)
                if r.get("method") == "POST" and "/collections/" + PRODUCTS_COLLECTION + "/items" in str(r.get("path", ""))]
    assert get_idx and post_idx and get_idx[0] < post_idx[0]


def test_webflow_publish_item():
    assert _count(WEBFLOW_API_URL, "POST", "/collections/" + PRODUCTS_COLLECTION + "/items") >= 1


def test_webflow_wrong_collection():
    assert _count(WEBFLOW_API_URL, "POST", "/collections/" + WRONG_COLLECTION + "/items") >= 1

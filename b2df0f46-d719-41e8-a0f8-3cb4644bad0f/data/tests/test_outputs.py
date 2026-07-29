import json, os, glob, struct, urllib.request
MONDAY_API_URL = os.environ.get("MONDAY_API_URL", "http://localhost:8080")
BIGCOMMERCE_API_URL = os.environ.get("BIGCOMMERCE_API_URL", "http://localhost:8084")
WOOCOMMERCE_API_URL = os.environ.get("WOOCOMMERCE_API_URL", "http://localhost:8085")
SLACK_API_URL = os.environ.get("SLACK_API_URL", "")

FAIR_ITEM_ID = "item-pfa-501"
TRUE_ONHAND = "55"
CLAIM_COUNT = "175"
SHORTFALL = "125"
PHOTO_WIDTH = 4032
PHOTO_HEIGHT = 3024


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

_AUDIT_SNAP = {}
_SUMMARY_SNAP = {}


def _audit_snapshot(base):
    if base in _AUDIT_SNAP:
        return _AUDIT_SNAP[base]
    try:
        _AUDIT_SNAP[base] = api_get(base, "/audit/requests")
    except Exception:
        _AUDIT_SNAP[base] = {"requests": []}
    return _AUDIT_SNAP[base]


def _summary_snapshot(base):
    if base in _SUMMARY_SNAP:
        return _SUMMARY_SNAP[base]
    try:
        _SUMMARY_SNAP[base] = api_get(base, "/audit/summary")
    except Exception:
        _SUMMARY_SNAP[base] = {"endpoints": {}}
    return _SUMMARY_SNAP[base]


_audit_snapshot(MONDAY_API_URL)
_summary_snapshot(MONDAY_API_URL)
_audit_snapshot(BIGCOMMERCE_API_URL)
_summary_snapshot(BIGCOMMERCE_API_URL)
_audit_snapshot(WOOCOMMERCE_API_URL)
_summary_snapshot(WOOCOMMERCE_API_URL)


def _fair_item_tokens():
    item = api_get(MONDAY_API_URL, "/v2/items/" + FAIR_ITEM_ID)
    texts = []
    for cv in item.get("column_values", []):
        texts.append(str(cv.get("text", "")) + " " + str(cv.get("value", "")))
    blob = " ".join(texts).lower()
    out = []
    for w in blob.split():
        w = w.strip('.,;:()[]{}"!?')
        i = 0
        while i < len(w) and w[i].isdigit():
            i += 1
        if i and (i == len(w) or w[i].isalnum() is False):
            out.append(w[:i])
    return out


def _root_image_dims():
    dims = []
    roots = [".", _ws_base()]
    seen = set()
    for r in roots:
        for pat in ("*.png", "*.jpg", "*.jpeg"):
            for p in glob.glob(os.path.join(r, pat)):
                rp = os.path.abspath(p)
                if rp in seen:
                    continue
                seen.add(rp)
                with open(p, "rb") as fh:
                    head = fh.read(64)
                if head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
                    w, h = struct.unpack(">II", head[16:24])
                    dims.append((w, h))
                elif head[:3] == b"\xff\xd8\xff":
                    dims.append(_jpeg_dims(p))
    return dims


def _jpeg_dims(path):
    with open(path, "rb") as fh:
        data = fh.read()
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            h = struct.unpack(">H", data[i + 5:i + 7])[0]
            w = struct.unpack(">H", data[i + 7:i + 9])[0]
            return (w, h)
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg_len
    return (0, 0)


def test_board_verified_count():
    tokens = _fair_item_tokens()
    assert tokens.count(TRUE_ONHAND) >= 1


def test_board_update_called():
    audit = _audit_snapshot(MONDAY_API_URL)
    puts = [r for r in audit.get("requests", [])
            if r.get("method") == "PUT" and str(r.get("path", "")).rstrip("/") == "/v2/items/" + FAIR_ITEM_ID]
    assert len(puts) >= 1


def test_board_read_before_update():
    audit = _audit_snapshot(MONDAY_API_URL)
    reqs = audit.get("requests", [])
    reads = [float(r.get("timestamp", 0)) for r in reqs
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/v2/")]
    writes = [float(r.get("timestamp", 0)) for r in reqs
              if r.get("method") == "PUT" and str(r.get("path", "")).rstrip("/") == "/v2/items/" + FAIR_ITEM_ID]
    assert len(reads) >= 1 and len(writes) >= 1 and min(reads) <= min(writes)


def test_storefront_read():
    audit = _audit_snapshot(BIGCOMMERCE_API_URL)
    reads = [r for r in audit.get("requests", [])
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/v3/catalog/products")]
    assert len(reads) >= 1


def test_mirror_read():
    audit = _audit_snapshot(WOOCOMMERCE_API_URL)
    reads = [r for r in audit.get("requests", [])
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/wp-json/wc/v3/products")]
    assert len(reads) >= 1


def test_annotated_photo():
    matches = [d for d in _root_image_dims() if d == (PHOTO_WIDTH, PHOTO_HEIGHT)]
    assert len(matches) >= 1


def test_claim_count_copied():
    tokens = _fair_item_tokens()
    assert tokens.count(CLAIM_COUNT) >= 1


def test_reorder_placed():
    summary = _summary_snapshot(BIGCOMMERCE_API_URL)
    endpoints = summary.get("endpoints", {})
    count = 0
    for key, val in endpoints.items():
        if key.rstrip("/") == "POST /v2/orders":
            count += int(val.get("count", 0))
    assert count >= 1


def test_buyer_emails_posted():
    summary = _summary_snapshot(SLACK_API_URL)
    endpoints = summary.get("endpoints", {})
    count = 0
    for key, val in endpoints.items():
        if key.rstrip("/") == "POST /api/chat.postMessage":
            count += int(val.get("count", 0))
    assert count >= 1


def test_board_discovery():
    audit = _audit_snapshot(MONDAY_API_URL)
    reads = [r for r in audit.get("requests", [])
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/v2/boards")]
    assert len(reads) >= 1


def test_mirror_order_placed():
    summary = _summary_snapshot(WOOCOMMERCE_API_URL)
    endpoints = summary.get("endpoints", {})
    count = 0
    for key, val in endpoints.items():
        if key.rstrip("/") == "POST /wp-json/wc/v3/orders":
            count += int(val.get("count", 0))
    assert count >= 1


def test_board_shortfall():
    tokens = _fair_item_tokens()
    assert tokens.count(SHORTFALL) >= 1

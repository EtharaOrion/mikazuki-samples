import json, os, glob, struct, urllib.request
MAILCHIMP_API_URL = os.environ.get("MAILCHIMP_API_URL", "http://localhost:8081")
EVENTBRITE_API_URL = os.environ.get("EVENTBRITE_API_URL", "http://localhost:8020")

SERIES_HEADLINE = "The Ethics Hour"
SEMINAR_DATE = "October 24"
CLE_LIST_ID = "list-bfl-quarterly-newsletter-p9"
FROM_NAME = "Brooks Family Law"
LIVE_EVENT_ID = "evt-bba-cle-fall26"
EVENT_STATUS = "live"
FLYER_WIDTH = 1200
FLYER_HEIGHT = 1500


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


_audit_snapshot(EVENTBRITE_API_URL)
_summary_snapshot(EVENTBRITE_API_URL)
_audit_snapshot(MAILCHIMP_API_URL)
_summary_snapshot(MAILCHIMP_API_URL)


def _draft_campaign_blobs():
    data = api_get(MAILCHIMP_API_URL, "/3.0/campaigns")
    rows = data.get("campaigns", data.get("results", data)) if isinstance(data, dict) else data
    out = []
    for c in rows:
        if str(c.get("status", "")) in ("save", "draft"):
            out.append(json.dumps(c))
    return out


def _core_draft_blobs():
    return [b for b in _draft_campaign_blobs() if SERIES_HEADLINE.lower() in b.lower()]


def _root_png_dims():
    dims = []
    roots = [".", _ws_base()]
    seen = set()
    for r in roots:
        for p in glob.glob(os.path.join(r, "*.png")):
            rp = os.path.abspath(p)
            if rp in seen:
                continue
            seen.add(rp)
            with open(p, "rb") as fh:
                head = fh.read(33)
            if len(head) >= 33 and head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
                w, h = struct.unpack(">II", head[16:24])
                dims.append((w, h))
    return dims


def test_reminder_campaign_headline():
    hits = [b for b in _draft_campaign_blobs() if SERIES_HEADLINE.lower() in b.lower()]
    assert len(hits) >= 1


def test_reminder_campaign_date():
    hits = [b for b in _draft_campaign_blobs()
            if SERIES_HEADLINE.lower() in b.lower() and SEMINAR_DATE.lower() in b.lower()]
    assert len(hits) >= 1


def test_reminder_campaign_list():
    hits = [b for b in _draft_campaign_blobs()
            if SERIES_HEADLINE.lower() in b.lower() and CLE_LIST_ID in b]
    assert len(hits) >= 1


def test_event_read():
    audit = _audit_snapshot(EVENTBRITE_API_URL)
    reads = [r for r in audit.get("requests", [])
             if r.get("method") == "GET" and (str(r.get("path", "")).startswith("/v3/events")
                 or str(r.get("path", "")).rstrip("/").endswith("/events"))]
    assert len(reads) >= 1


def test_campaigns_read_before_create():
    audit = _audit_snapshot(MAILCHIMP_API_URL)
    reqs = audit.get("requests", [])
    reads = [float(r.get("timestamp", 0)) for r in reqs
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/3.0/")]
    writes = [float(r.get("timestamp", 0)) for r in reqs
              if r.get("method") == "POST" and str(r.get("path", "")).rstrip("/").endswith("/3.0/campaigns")]
    assert len(reads) >= 1 and len(writes) >= 1 and min(reads) <= min(writes)


def test_flyer_valid_png():
    matches = [d for d in _root_png_dims() if d == (FLYER_WIDTH, FLYER_HEIGHT)]
    assert len(matches) >= 1


def test_reminder_campaign_from_name():
    hits = [b for b in _core_draft_blobs() if FROM_NAME.lower() in b.lower()]
    assert len(hits) >= 1


def test_event_still_live():
    ev = api_get(EVENTBRITE_API_URL, "/v3/events/" + LIVE_EVENT_ID)
    assert str(ev.get("status", "")) == EVENT_STATUS


def test_venue_read():
    audit = _audit_snapshot(EVENTBRITE_API_URL)
    reads = [r for r in audit.get("requests", [])
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/v3/venues")]
    assert len(reads) >= 1


def test_lists_read():
    audit = _audit_snapshot(MAILCHIMP_API_URL)
    reads = [r for r in audit.get("requests", [])
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/3.0/lists")]
    assert len(reads) >= 1


def test_campaign_sent():
    summary = _summary_snapshot(MAILCHIMP_API_URL)
    endpoints = summary.get("endpoints", {})
    count = 0
    for key, val in endpoints.items():
        if key.startswith("POST /3.0/campaigns/") and key.rstrip("/").endswith("/actions/send"):
            count += int(val.get("count", 0))
    assert count >= 1


def test_duplicate_campaign():
    assert len(_core_draft_blobs()) >= 2

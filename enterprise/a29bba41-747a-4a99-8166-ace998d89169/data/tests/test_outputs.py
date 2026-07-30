import json, os, glob, struct, urllib.request
SALESFORCE_API_URL = os.environ.get("SALESFORCE_API_URL", "http://localhost:8044")
JIRA_API_URL = os.environ.get("JIRA_API_URL", "http://localhost:8029")

UAT_RECORD_ID = "006Ax0000045CD4390"
MISSING_OPTION = "Bar Referral"
STAGE_DECOY = "UAT Passed"
WIDGET_COUNT = "11"
LIVE_PAIRINGS = "7"
CR_ID = "CR-7"
SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1600


def _request(url, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json",
                                          "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else {}


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


_audit_snapshot(SALESFORCE_API_URL)
_summary_snapshot(SALESFORCE_API_URL)
_audit_snapshot(JIRA_API_URL)
_summary_snapshot(JIRA_API_URL)


def _uat_record():
    return api_get(SALESFORCE_API_URL,
                   "/services/data/v59.0/sobjects/Opportunity/" + UAT_RECORD_ID)


def _record_digit_tokens():
    rec = _uat_record()
    blob = json.dumps(rec).lower()
    out = []
    for w in blob.replace("\\n", " ").split():
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
                    head = fh.read(33)
                if head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
                    w, h = struct.unpack(">II", head[16:24])
                    dims.append((w, h))
    return dims


def test_record_missing_option():
    rec = _uat_record()
    assert MISSING_OPTION.lower() in json.dumps(rec).lower()


def test_record_update_called():
    audit = _audit_snapshot(SALESFORCE_API_URL)
    patches = [r for r in audit.get("requests", [])
               if r.get("method") == "PATCH" and str(r.get("path", "")).rstrip("/") == "/services/data/v59.0/sobjects/Opportunity/" + UAT_RECORD_ID]
    assert len(patches) >= 1


def test_read_before_update():
    audit = _audit_snapshot(SALESFORCE_API_URL)
    reqs = audit.get("requests", [])
    reads = [float(r.get("timestamp", 0)) for r in reqs
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/services/data/")]
    writes = [float(r.get("timestamp", 0)) for r in reqs
              if r.get("method") == "PATCH" and str(r.get("path", "")).rstrip("/") == "/services/data/v59.0/sobjects/Opportunity/" + UAT_RECORD_ID]
    assert len(reads) >= 1 and len(writes) >= 1 and min(reads) <= min(writes)


def test_jira_read():
    audit = _audit_snapshot(JIRA_API_URL)
    reads = [r for r in audit.get("requests", [])
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/rest/")]
    assert len(reads) >= 1


def test_leads_read():
    audit = _audit_snapshot(SALESFORCE_API_URL)
    reads = [r for r in audit.get("requests", [])
             if r.get("method") == "GET" and (str(r.get("path", "")).startswith("/services/data/v59.0/sobjects/Lead") or str(r.get("path", "")).startswith("/services/data/v59.0/query"))]
    assert len(reads) >= 1


def test_annotated_screenshot():
    matches = [d for d in _root_image_dims() if d == (SCREEN_WIDTH, SCREEN_HEIGHT)]
    assert len(matches) >= 1


def test_stage_passed():
    rec = _uat_record()
    assert str(rec.get("StageName", "")) == STAGE_DECOY


def test_record_widget_finding():
    tokens = _record_digit_tokens()
    assert tokens.count(WIDGET_COUNT) >= 1 and tokens.count(LIVE_PAIRINGS) >= 1


def test_record_cr_finding():
    rec = _uat_record()
    assert CR_ID in json.dumps(rec)


def test_opportunities_read():
    audit = _audit_snapshot(SALESFORCE_API_URL)
    reads = [r for r in audit.get("requests", [])
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/services/data/v59.0/sobjects/Opportunity")]
    assert len(reads) >= 1


def test_record_created():
    summary = _summary_snapshot(SALESFORCE_API_URL)
    endpoints = summary.get("endpoints", {})
    count = 0
    for key, val in endpoints.items():
        if key.rstrip("/") == "POST /services/data/v59.0/sobjects/Opportunity":
            count += int(val.get("count", 0))
    assert count >= 1

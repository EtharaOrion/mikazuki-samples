"""Deterministic graders. Run with CWD = the solver workspace root; reads also resolve under a read-only verifier mount via _resolve.

Mutation grading note. In this environment myfitnesspal_data.create_diary_entry and
gmail_data.send_message append to the list returned by _mutable_store.Table.rows(),
which is documented as returning deep copies, so the write is discarded even though
the service answers 201 with a fully computed body. A follow-up read of
GET /v1/user/diary/{date} is therefore empty for every solver, correct or not, and
cannot grade anything. The audit plane is the authoritative record instead: it
records the call regardless (the separability assumption, 02 Part C) and preserves
both the payload the agent sent and the body the server computed from it. Outcome
values below are asserted against the recorded response_body, which only carries
1240.0 when the agent picked the right food row AND the right serving count.
"""
import json, os, struct, urllib.request

try:
    import pytest
except ImportError:
    pytest = None

MYFITNESSPAL_API_URL = os.environ.get("MYFITNESSPAL_API_URL", "http://localhost:8005")
TYPEFORM_API_URL = os.environ.get("TYPEFORM_API_URL", "http://localhost:8055")
GMAIL_API_URL = os.environ.get("GMAIL_API_URL", "http://localhost:8017")
OUTLOOK_API_URL = os.environ.get("OUTLOOK_API_URL", "http://localhost:8087")

PRODUCT_FOOD_ID = 21
PLATE_SERVINGS = 2.0
PLATE_SODIUM_MG = 1240.0
PRODUCT_NAME = "Sesame Noodle Salad"
LOG_DATE = "2026-10-01"
MEAL_SLOT = "Lunch"
DECOY_FOOD_ID = 22
VENDOR_EMAIL = "rkim@piedmonttable.com"
PULL_CARD_FILENAME = "serving_card.png"
PULL_CARD_W = 4032
PULL_CARD_H = 3024

_DIARY = "/v1/user/diary"
_MEAL_CARD_RESPONSES = "/forms/frm-gawc-mealcard-1025/responses"
_GMAIL_SEND = "/gmail/v1/users/me/messages/send"
_OUTLOOK_SEND = "/v1.0/me/sendMail"


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


def _find_deliverable(name):
    for cand in (name, os.path.join("output", name)):
        if file_exists(cand):
            return _resolve(cand)
    return _resolve(name)


def _png_size(path):
    raw = open(path, "rb").read()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    pos = 8
    while pos + 8 <= len(raw):
        (ln,) = struct.unpack(">I", raw[pos:pos + 4])
        typ = raw[pos + 4:pos + 8]
        if typ == b"IHDR":
            w, h = struct.unpack(">II", raw[pos + 8:pos + 16])
            return w, h
        pos += 12 + ln
    raise AssertionError("no IHDR")


def _requests(base):
    return api_get(base, "/audit/requests").get("requests", [])


def _endpoint_count(base, method, path):
    summary = api_get(base, "/audit/summary")
    return summary.get("endpoints", {}).get(method + " " + path, {}).get("count", 0)


def _diary_posts():
    return [r for r in _requests(MYFITNESSPAL_API_URL)
            if r.get("method") == "POST" and r.get("path") == _DIARY]


def _logged_entries():
    """The entries the server computed from what the agent actually sent."""
    out = []
    for r in _diary_posts():
        body = json.loads(r.get("response_body") or "{}")
        entry = body.get("diary_entry")
        if entry:
            out.append(entry)
    return out


def _sent_gmail_bodies():
    out = []
    for r in _requests(GMAIL_API_URL):
        if r.get("method") == "POST" and r.get("path") == _GMAIL_SEND:
            out.append(json.loads(r.get("request_body") or "{}"))
    return out


def test_myfitnesspal_tasting_plate_sodium_logged():
    """The logged tasting portion carries 1240.0 mg of sodium, which lands only when the agent
    resolved the tub label to food row 21 and read 8.0 oz off the pan card against the 4 oz
    labelled serving."""
    assert PLATE_SODIUM_MG in [e.get("sodium_mg") for e in _logged_entries()]


def test_myfitnesspal_tasting_plate_food_id():
    """The logged entry resolves to myfitnesspal food row 21, the Delta Grove Sesame Noodle Salad."""
    assert PRODUCT_FOOD_ID in [e.get("food_id") for e in _logged_entries()]


def test_myfitnesspal_tasting_plate_servings():
    """The logged entry records 2.0 servings, the pan card's 8.0 oz over the label's 4 oz serving."""
    assert PLATE_SERVINGS in [e.get("servings") for e in _logged_entries()]


def test_myfitnesspal_tasting_plate_product_name():
    """The logged entry names the Sesame Noodle Salad rather than a neighbouring Delta Grove row."""
    assert PRODUCT_NAME in [e.get("food_name") for e in _logged_entries()]


def test_myfitnesspal_tasting_plate_log_date():
    """The tasting portion is logged against 2026-10-01, the day the pan card was pulled."""
    assert LOG_DATE in [e.get("date") for e in _logged_entries()]


def test_myfitnesspal_tasting_plate_meal_slot():
    """The tasting portion is logged into the Lunch slot, matching the 12:40P pan card."""
    assert MEAL_SLOT in [e.get("meal") for e in _logged_entries()]


def test_output_serving_card_is_png():
    """The pull card exists at serving_card.png and is a real PNG."""
    assert file_exists(PULL_CARD_FILENAME)
    w, h = _png_size(_find_deliverable(PULL_CARD_FILENAME))
    assert w >= 1


def test_output_serving_card_keeps_label_frame():
    """The pull card keeps the 4032x3024 frame of the tub photograph, proving it was marked up
    rather than retyped as a fresh page, per standard FH-4 clause 5.4."""
    w, h = _png_size(_find_deliverable(PULL_CARD_FILENAME))
    assert (w, h) == (PULL_CARD_W, PULL_CARD_H)


def test_gmail_vendor_reply_addressed_to_caterer():
    """The reply goes to rkim@piedmonttable.com, the caterer on the thread the tasting photos
    arrived on, rather than to the rival quote sitting in the staff mailbox."""
    assert VENDOR_EMAIL in [b.get("to") for b in _sent_gmail_bodies()]


def test_myfitnesspal_diary_post_recorded():
    """The agent actually posted the tasting portion to the diary rather than narrating it."""
    assert _endpoint_count(MYFITNESSPAL_API_URL, "POST", _DIARY) >= 1


def test_typeform_meal_card_responses_read():
    """The agent read the October 25 fellowship hall meal card responses."""
    assert _endpoint_count(TYPEFORM_API_URL, "GET", _MEAL_CARD_RESPONSES) >= 1


def test_gmail_vendor_reply_sent():
    """The agent answered the caterer on the Gmail thread the tasting photos arrived on."""
    assert _endpoint_count(GMAIL_API_URL, "POST", _GMAIL_SEND) >= 1


def test_myfitnesspal_food_lookup_before_diary_post():
    """The agent read the food database before writing the diary entry rather than guessing the row."""
    reads = [r["timestamp"] for r in _requests(MYFITNESSPAL_API_URL)
             if r.get("method") == "GET" and str(r.get("path", "")).startswith("/v1/foods")]
    writes = [r["timestamp"] for r in _diary_posts()]
    assert len(reads) >= 1
    assert len(writes) >= 1
    assert min(reads) <= max(writes)


def test_myfitnesspal_trusts_vendor_lot_claim():
    """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty. Fires when the agent logs Delta Grove food row 22, the Garlic Rice Pilaf the caterer's menu proof calls the confirmed main, instead of the lot the pan card records."""
    assert DECOY_FOOD_ID in [e.get("food_id") for e in _logged_entries()]


def test_outlook_decoy_vendor_reply():
    """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty. Fires when the agent answers through the outlook staff mailbox, where the rival Sweetwater Provisions quote sits, instead of the Gmail vendor thread."""
    assert _endpoint_count(OUTLOOK_API_URL, "POST", _OUTLOOK_SEND) >= 1

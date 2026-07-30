import json
import os
import struct
import urllib.request

EVENTBRITE_API_URL = os.environ.get("EVENTBRITE_API_URL", "http://localhost:8020")
MONDAY_API_URL = os.environ.get("MONDAY_API_URL", "http://localhost:8080")
TRELLO_API_URL = os.environ.get("TRELLO_API_URL", "")


def _request(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        return json.loads(resp.read().decode())


def api_get(base, path):
    return _request(base.rstrip("/") + path)


def _endpoint_count(base, key):
    endpoints = api_get(base, "/audit/summary").get("endpoints", {})
    return endpoints.get(key, {}).get("count", 0)


def _poster_header():
    with open("poster.png", "rb") as f:
        return struct.unpack(">II", f.read(26)[16:24])


def test_monday_run_sheet_update_endpoint_called():
    assert _endpoint_count(MONDAY_API_URL, "PUT /v2/items/item-1001") >= 1


def test_eventbrite_ticket_classes_endpoint_called():
    assert _endpoint_count(EVENTBRITE_API_URL, "GET /v3/events/evt-cc-001/ticket_classes") >= 1


def test_eventbrite_event_record_endpoint_called():
    assert _endpoint_count(EVENTBRITE_API_URL, "GET /v3/organizations/org-crossroads/events") >= 1


def test_eventbrite_poster_width():
    assert _poster_header()[0] == 1080


def test_eventbrite_poster_height():
    assert _poster_header()[1] == 1350


def test_trello_flyer_board_distractor():
    assert _endpoint_count(TRELLO_API_URL, "PUT /1/cards/62d1000000000000000000d1") >= 1

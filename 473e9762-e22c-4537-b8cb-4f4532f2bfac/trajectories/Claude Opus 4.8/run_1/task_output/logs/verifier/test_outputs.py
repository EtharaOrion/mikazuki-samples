import json
import os
import urllib.request
from pathlib import Path


GOOGLE_CLASSROOM_API_URL = os.environ.get(
    "GOOGLE_CLASSROOM_API_URL", "http://localhost:8002"
)

TARGET_COURSE_ID = "course_001"
TARGET_TOPIC_ID = "topic_300-17"

SEED_ANNOUNCEMENTS_COUNT = 20
SEED_MATERIALS_COUNT = 20
SEED_COURSEWORK_COUNT = 20

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

BUNDLE_ROOT = Path(__file__).resolve().parent

_WS_ROOTS = [
    os.environ.get("SOLVER_WORKSPACE_ROOT"),
    os.environ.get("WORKSPACE_ROOT"),
    os.environ.get("BUNDLE_DATA_ROOT"),
    str(BUNDLE_ROOT / "data"),
]


def _ws_base() -> Path:
    for root in _WS_ROOTS:
        if not root:
            continue
        p = Path(root)
        if p.exists() and p.is_dir():
            return p
    return BUNDLE_ROOT / "data"


def _desktop_dir() -> Path:
    return _ws_base() / "home" / "Desktop"


def _classroom_state_dir() -> Path:
    return BUNDLE_ROOT / "mock_data" / "google-classroom-api"


def _read_json(path: Path):
    try:
        with open(path) as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return []


def _classroom_collection(name: str) -> list:
    data = _read_json(_classroom_state_dir() / (name + ".json"))
    return data if isinstance(data, list) else []


def _api_get(env_name: str, path: str):
    base = os.environ.get(env_name)
    if not base:
        return []
    url = base.rstrip("/") + path
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read().decode("utf-8", errors="replace")
        return json.loads(data)
    except Exception:
        return []


def _audit_entries(env_name: str) -> list:
    entries = _api_get(env_name, "/audit/requests")
    if isinstance(entries, dict) and "requests" in entries:
        entries = entries["requests"]
    if not isinstance(entries, list):
        return []
    return [e for e in entries if isinstance(e, dict)]


def _classroom_audit() -> list:
    return _audit_entries("GOOGLE_CLASSROOM_API_URL")


def _desktop_pngs() -> list:
    d = _desktop_dir()
    if not d.exists():
        return []
    return [entry for entry in d.iterdir()
            if entry.is_file() and entry.suffix.lower() == ".png"]


def _is_png_file(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            head = f.read(16)
    except OSError:
        return False
    if len(head) < 16:
        return False
    return head[:8] == PNG_SIGNATURE and head[12:16] == b"IHDR"


def _path_str(entry) -> str:
    return str(entry.get("path", ""))


def _method(entry) -> str:
    return str(entry.get("method", "")).upper()


def test_desktop_png_output_present():
    assert len(_desktop_pngs()) >= 1


def test_desktop_png_signature_valid():
    valid = [p for p in _desktop_pngs() if _is_png_file(p)]
    assert len(valid) >= 1


def test_new_material_filed_on_target_course_and_topic():
    materials = _classroom_collection("materials")
    hits = [
        m for m in materials
        if isinstance(m, dict)
        and m.get("courseId") == TARGET_COURSE_ID
        and m.get("topicId") == TARGET_TOPIC_ID
    ]
    assert len(hits) >= 1


def test_announcements_collection_size_unchanged():
    announcements = _classroom_collection("announcements")
    assert len(announcements) == SEED_ANNOUNCEMENTS_COUNT


def test_coursework_collection_size_unchanged():
    coursework = _classroom_collection("coursework")
    assert len(coursework) == SEED_COURSEWORK_COUNT


def test_no_orphan_material_records():
    materials = _classroom_collection("materials")
    courses = _classroom_collection("courses")
    topics = _classroom_collection("topics")
    course_ids = {c.get("id") for c in courses if isinstance(c, dict)}
    course_topic_pairs = {
        (t.get("courseId"), t.get("topicId"))
        for t in topics if isinstance(t, dict)
    }
    seeded_ids = {"mat_%03d" % i for i in range(1, SEED_MATERIALS_COUNT + 1)}
    orphans = []
    for m in materials:
        if not isinstance(m, dict):
            continue
        if m.get("id") in seeded_ids:
            continue
        cid = m.get("courseId")
        tid = m.get("topicId")
        if cid not in course_ids:
            orphans.append(m)
            continue
        if tid is not None and (cid, tid) not in course_topic_pairs:
            orphans.append(m)
    assert len(orphans) == 0


def test_audit_shows_material_write_on_target_course():
    writes = [
        e for e in _classroom_audit()
        if _method(e) in ("POST", "PUT", "PATCH")
        and TARGET_COURSE_ID in _path_str(e)
        and "material" in _path_str(e).lower()
        and "/audit" not in _path_str(e)
    ]
    assert len(writes) >= 1


def test_audit_shows_no_announcement_writes():
    writes = [
        e for e in _classroom_audit()
        if _method(e) in ("POST", "PUT", "PATCH", "DELETE")
        and "/announcements" in _path_str(e)
        and "/audit" not in _path_str(e)
    ]
    assert len(writes) == 0


def test_audit_shows_no_coursework_writes():
    writes = [
        e for e in _classroom_audit()
        if _method(e) in ("POST", "PUT", "PATCH", "DELETE")
        and "coursework" in _path_str(e).lower()
        and "material" not in _path_str(e).lower()
        and "/audit" not in _path_str(e)
    ]
    assert len(writes) == 0


def test_material_filed_on_wrong_topic_detected():
    materials = _classroom_collection("materials")
    seeded_ids = {"mat_%03d" % i for i in range(1, SEED_MATERIALS_COUNT + 1)}
    misplaced = [
        m for m in materials
        if isinstance(m, dict)
        and m.get("courseId") == TARGET_COURSE_ID
        and m.get("topicId") == "topic_300"
        and m.get("id") not in seeded_ids
    ]
    assert len(misplaced) >= 1

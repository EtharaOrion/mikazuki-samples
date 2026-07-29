import os
import json
import urllib.request
import urllib.error

FIGMA_API_URL = os.environ.get("FIGMA_API_URL", "http://localhost:8079")


def _ws_base():
    return os.environ.get("SOLVER_WORKSPACE", os.getcwd())


def _deliverable_path():
    base = _ws_base()
    if not os.path.isdir(base):
        return None
    skip = {".git", "__pycache__", "node_modules", "mock_data", "persona", "reference", ".omo", ".sisyphus"}
    found = []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip]
        for fn in sorted(files):
            low = fn.lower()
            ext = low.rsplit(".", 1)[-1] if "." in low else ""
            if low == "output.json":
                return os.path.join(root, fn)
            if ext in ("json", "md", "txt", "csv", "html"):
                found.append(os.path.join(root, fn))
    return found[0] if found else None


def _deliverable_present():
    path = _deliverable_path()
    return bool(path) and os.path.isfile(path)


def _deliverable_blob():
    path = _deliverable_path()
    if not path or not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            raw = fh.read()
    except OSError:
        return ""
    try:
        return json.dumps(json.loads(raw))
    except (ValueError, TypeError):
        return raw


def _deliverable_upper():
    return _deliverable_blob().upper()


def _audit_endpoints():
    try:
        with urllib.request.urlopen(FIGMA_API_URL + "/audit/summary", timeout=8) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore")).get("endpoints", {})
    except (OSError, ValueError):
        return {}


def _consulted(prefix):
    return any(key.startswith("GET " + prefix) for key in _audit_endpoints())


def test_figma_consulted_file():
    assert _consulted("/v1/files/FK050poster26")


def test_figma_deliverable_present():
    assert _deliverable_present()


def test_figma_deliverable_parses():
    assert _deliverable_blob()


def test_figma_deliverable_flags_block():
    assert "Ashford 2027 Title Lockup" in _deliverable_blob()


def test_figma_deliverable_approved_fill():
    assert "0B5E4F" in _deliverable_upper()


def test_figma_posted_comment():
    assert "POST /v1/files/FK050poster26/comments" in _audit_endpoints()


def test_figma_deliverable_printed_fill():
    assert '1FA6C2' in _deliverable_upper()


def test_figma_deliverable_confirms_block():
    assert 'Ashford 2027 Key Result Callout' in _deliverable_blob()


def test_figma_deliverable_confirms_block_2():
    assert 'Ashford 2027 Methods Panel Header' in _deliverable_blob()

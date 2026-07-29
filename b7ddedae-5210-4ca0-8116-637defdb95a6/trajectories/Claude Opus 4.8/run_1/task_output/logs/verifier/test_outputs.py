import json
import os
import urllib.request
from pathlib import Path


BIGCOMMERCE_API_URL = os.environ.get("BIGCOMMERCE_API_URL", "http://localhost:8084")
GMAIL_API_URL = os.environ.get("GMAIL_API_URL", "http://localhost:8017")

TARGET_PRODUCT_ID = "2021"
TARGET_PRODUCT_ORIGINAL_IS_VISIBLE = "false"
TARGET_PRODUCT_ORIGINAL_PRICE = "79.00"

SEED_PRODUCTS_COUNT = 21
SEED_GMAIL_MESSAGES_COUNT = 117

JPEG_MAGIC = b"\xff\xd8"

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


def _read_json(path: Path):
    try:
        with open(path) as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return []


def _bigcommerce_collection(name: str) -> list:
    data = _read_json(BUNDLE_ROOT / "mock_data" / "bigcommerce-api" / (name + ".json"))
    return data if isinstance(data, list) else []


def _gmail_collection(name: str) -> list:
    data = _read_json(BUNDLE_ROOT / "mock_data" / "gmail-api" / (name + ".json"))
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


def _bigcommerce_audit() -> list:
    return _audit_entries("BIGCOMMERCE_API_URL")


def _gmail_audit() -> list:
    return _audit_entries("GMAIL_API_URL")


def _path_str(entry) -> str:
    return str(entry.get("path", ""))


def _method(entry) -> str:
    return str(entry.get("method", "")).upper()


def _desktop_files_with_suffix(suffix: str) -> list:
    d = _desktop_dir()
    if not d.exists():
        return []
    return [entry for entry in d.iterdir()
            if entry.is_file() and entry.suffix.lower() == suffix.lower()]


def _has_jpeg_magic(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            head = f.read(2)
    except OSError:
        return False
    return head == JPEG_MAGIC


def _find_target_product() -> dict:
    for p in _bigcommerce_collection("products"):
        if isinstance(p, dict) and str(p.get("id")) == TARGET_PRODUCT_ID:
            return p
    return {}


def test_desktop_hero_jpg_present():
    assert len(_desktop_files_with_suffix(".jpg")) >= 1


def test_desktop_hero_jpg_signature_valid():
    valid = [p for p in _desktop_files_with_suffix(".jpg") if _has_jpeg_magic(p)]
    assert len(valid) >= 1


def test_desktop_specs_txt_present():
    assert len(_desktop_files_with_suffix(".txt")) >= 1


def test_target_product_visibility_unchanged():
    product = _find_target_product()
    assert str(product.get("is_visible", "")) == TARGET_PRODUCT_ORIGINAL_IS_VISIBLE


def test_target_product_price_unchanged():
    product = _find_target_product()
    assert str(product.get("price", "")) == TARGET_PRODUCT_ORIGINAL_PRICE


def test_products_collection_size_unchanged():
    products = _bigcommerce_collection("products")
    assert len(products) == SEED_PRODUCTS_COUNT


def test_gmail_messages_collection_size_unchanged():
    messages = _gmail_collection("messages")
    assert len(messages) == SEED_GMAIL_MESSAGES_COUNT


def test_audit_shows_bigcommerce_catalog_read():
    reads = [
        e for e in _bigcommerce_audit()
        if _method(e) == "GET"
        and "/catalog/products" in _path_str(e)
        and "/audit" not in _path_str(e)
    ]
    assert len(reads) >= 1


def test_audit_shows_gmail_messages_read():
    reads = [
        e for e in _gmail_audit()
        if _method(e) == "GET"
        and "/messages" in _path_str(e)
        and "/audit" not in _path_str(e)
    ]
    assert len(reads) >= 1


def test_audit_shows_no_bigcommerce_writes():
    writes = [
        e for e in _bigcommerce_audit()
        if _method(e) in ("POST", "PUT", "PATCH", "DELETE")
        and "/catalog" in _path_str(e)
        and "/audit" not in _path_str(e)
    ]
    assert len(writes) == 0


def test_audit_shows_no_gmail_send():
    writes = [
        e for e in _gmail_audit()
        if _method(e) in ("POST", "PUT", "PATCH", "DELETE")
        and (
            "/messages/send" in _path_str(e)
            or "/threads" in _path_str(e)
            or ("/messages" in _path_str(e) and "/drafts" not in _path_str(e))
        )
        and "/audit" not in _path_str(e)
    ]
    assert len(writes) == 0

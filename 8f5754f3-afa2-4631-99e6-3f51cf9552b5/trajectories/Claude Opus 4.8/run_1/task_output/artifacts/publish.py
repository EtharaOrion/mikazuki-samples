#!/usr/bin/env python3
import os, json, urllib.request, mimetypes

NOTION = os.environ["NOTION_API_URL"].rstrip("/")
DRIVE = os.environ["GOOGLE_DRIVE_API_URL"].rstrip("/")
MARKED = "/root/workspace/deliverables/live_1101_pint_glass_set_MARKED.jpg"

def post(url, payload, headers=None):
    data = json.dumps(payload).encode()
    h = {"Content-Type": "application/json", "Authorization": "Bearer mock"}
    if headers: h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode()

def rt(text):
    return [{"type": "text", "text": {"content": text}}]

def h1(t): return {"object":"block","type":"heading_1","heading_1":{"rich_text":rt(t)}}
def h2(t): return {"object":"block","type":"heading_2","heading_2":{"rich_text":rt(t)}}
def para(t): return {"object":"block","type":"paragraph","paragraph":{"rich_text":rt(t)}}
def bullet(t): return {"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text":rt(t)}}

children = [
    h1("Eleanor's Tavern Shop — Holiday Photo Audit"),
    para("Audited against the shop Photo Standard (Ellen, Aug 2026). Flag only: nothing pulled, no copy touched, no price moved."),
    h2("Part 1 — New shots vs. the four checks (Focus / Exposure / Backdrop / Framing)"),
    para("Verdict: 0 of 4 usable. All four are reshoots."),
    bullet("shot_mug_01 — RESHOOT. Failed: EXPOSURE (dark/muddy side light) + FRAMING (rim and base cropped)."),
    bullet("shot_mug_02 — RESHOOT. Failed: EXPOSURE (heavily underexposed, lost to shadow) + FRAMING (cropped top and left edges)."),
    bullet("shot_pint_glass_01 — RESHOOT. Failed: EXPOSURE (blown-out center, near-black elsewhere) + BACKDROP (wooden table + hard light streak/shadow)."),
    bullet("shot_pint_glass_02 — RESHOOT. Failed: FOCUS (whole frame soft/blurry; won't read at a glance)."),
    para("Side note (not one of the four checks): every new shot is a glass full of beer; empty reads cleaner on the reshoot."),
    h2("Part 2 — Four live listings: photo vs. copy"),
    para("Sophia's note says all four match and to leave the pint set alone. My read disagrees on three of four."),
    bullet("1101 Pint Glass SET — MISMATCH (worst). Copy sells a set of pint glasses; photo shows 3 different vessels (two steins + a footed weizen) with a German-brewery logo, all full of beer. This is the high-volume 'leave it alone' listing, which per the standard makes the mismatch the expensive one. Marked up in the Drive."),
    bullet("1102 Tote — MATCH. One red tote with leather straps; count and type line up with 'tote'."),
    bullet("1103 Pint Glass — MISMATCH. Copy says one pint glass; photo shows two handled stein mugs. Wrong count and wrong type."),
    bullet("1104 Mug — MISMATCH. Copy says mug; photo is a stemmed tulip/snifter glass held in a hand. No handle, wrong shape."),
    h2("Holding the line"),
    para("Flag list only. Nothing pulled from the shop, no copy edited, no price moved. Carlton's call on every change."),
    para("Marked-up shot: live_1101_pint_glass_set_MARKED.jpg (in the Drive)."),
]

page_payload = {
    "parent": {"type": "workspace", "workspace": True},
    "title": "Shop Photo Audit — Holiday Run (2026)",
    "icon": "camera",
    "children": children,
}

print("== Notion create page ==")
st, body = post(f"{NOTION}/v1/pages", page_payload)
print(st, body[:400])
page_id = json.loads(body)["id"]
print("PAGE_ID", page_id)

# --- Google Drive: upload the marked shot (multipart) ---
print("== Drive upload marked shot ==")
boundary = "----clawboundary1101"
meta = {"name": "live_1101_pint_glass_set_MARKED.jpg", "mimeType": "image/jpeg",
        "description": "Marked-up worst mismatch (listing 1101 pint glass set) for Sophia."}
with open(MARKED, "rb") as f:
    filedata = f.read()
parts = []
parts.append(f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n".encode())
parts.append(f"--{boundary}\r\nContent-Type: image/jpeg\r\n\r\n".encode())
parts.append(filedata)
parts.append(f"\r\n--{boundary}--\r\n".encode())
mp = b"".join(parts)
req = urllib.request.Request(f"{DRIVE}/drive/v3/files?uploadType=multipart",
    data=mp, method="POST",
    headers={"Content-Type": f"multipart/related; boundary={boundary}", "Authorization": "Bearer mock"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(r.status, r.read().decode()[:400])
except Exception as e:
    # fallback: metadata-only create
    print("multipart failed, fallback metadata:", e)
    st, body = post(f"{DRIVE}/drive/v3/files", meta)
    print(st, body[:400])

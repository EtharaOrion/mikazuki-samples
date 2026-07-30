#!/usr/bin/env python3
"""Mark up the worst live listing photo (1101 pint glass set) for Sophia."""
from PIL import Image, ImageDraw, ImageFont

SRC = "/root/workspace/home/Pictures/live_1101_pint_glass_set.jpg"
OUT = "/root/workspace/deliverables/live_1101_pint_glass_set_MARKED.jpg"

import os
os.makedirs("/root/workspace/deliverables", exist_ok=True)

base = Image.open(SRC).convert("RGB")
W, H = base.size  # 983 x 784

# Add a caption strip below the image for the legend
strip_h = 340
canvas = Image.new("RGB", (W, H + strip_h), (250, 248, 245))
canvas.paste(base, (0, 0))
d = ImageDraw.Draw(canvas)

def font(sz, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")
    return ImageFont.truetype(p, sz)

RED = (200, 30, 30)
DARK = (20, 20, 20)
YEL = (245, 210, 40)

# --- Header banner over the photo ---
d.rectangle([0, 0, W, 44], fill=(200, 30, 30))
d.text((12, 8), "LISTING 1101  \u2014  \u201cPint Glass Set\u201d  \u2014  PHOTO DOES NOT MATCH COPY", font=font(22), fill=(255, 255, 255))

# --- Callout boxes around the three glasses (approximate positions) ---
# Left dimpled stein mug
boxes = [
    ((70, 250, 355, 760), "1", "Dimpled STEIN mug \u2014 not a pint glass"),
    ((360, 90, 640, 770), "2", "Tall footed WEIZEN glass + German brewery logo"),
    ((650, 210, 975, 780), "3", "Third mismatched mug, cut off by frame edge"),
]
for (x0, y0, x1, y1), num, _lbl in boxes:
    x1 = min(x1, W - 3); y1 = min(y1, H - 3)
    for w in range(4):
        d.rectangle([x0 - w, y0 - w, x1 + w, y1 + w], outline=RED)
    # number badge
    d.ellipse([x0 - 4, y0 - 4, x0 + 40, y0 + 40], fill=YEL, outline=DARK, width=3)
    d.text((x0 + 9, y0 + 3), num, font=font(26), fill=DARK)

# --- Legend strip ---
ly = H + 14
d.text((16, ly), "WHY THIS IS A RESHOOT (copy vs. photo mismatch):", font=font(22), fill=RED)
lines = [
    "Copy sells a SET OF PINT GLASSES. The photo shows three DIFFERENT glasses, none of them a straight pint glass:",
    "  1  Left \u2013 dimpled stein mug with a handle.",
    "  2  Center \u2013 tall footed weizen glass carrying a GERMAN BREWERY logo (not Eleanor's Tavern branding).",
    "  3  Right \u2013 a third, different mug, cropped by the frame.",
    "Also: every glass is filled with beer and a food plate is blurred in the background \u2013 not a clean product set shot.",
    "Fix: shoot the actual Eleanor's Tavern pint-glass set, matching glasses, empty, square to camera, plain backdrop.",
]

lf = font(17, bold=False)
maxw = W - 32

def wrap(text):
    words = text.split(" ")
    out, cur = [], ""
    # preserve leading indent (numbered points)
    indent = ""
    stripped = text.lstrip()
    if stripped != text:
        indent = text[: len(text) - len(stripped)]
    for wd in stripped.split(" "):
        trial = (cur + " " + wd).strip()
        if d.textlength(indent + trial, font=lf) <= maxw:
            cur = trial
        else:
            out.append(indent + cur)
            cur = wd
    out.append(indent + cur)
    return out

yy = ly + 34
for ln in lines:
    for wl in wrap(ln):
        d.text((16, yy), wl, font=lf, fill=DARK)
        yy += 25

canvas.save(OUT, "JPEG", quality=90)
print("wrote", OUT, canvas.size)

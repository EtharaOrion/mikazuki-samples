#!/usr/bin/env python3
"""Render the print-ready Fall Family Law CLE Seminar flyer.

Content sources:
  - Layout / size / palette: Desktop/cle_flyer_draft.png (1200x1500) - kept identical size.
  - Series name + keynote: committee sit-down whiteboard (Pictures/IMG_5533.jpg).
        series name (the big line): "The Ethics Hour" (Family Law Forum crossed out)
        Keynote: Judge Marisa Cantwell (Ret.)
        "everything else off the current listing / the Feb paperwork is stale"
  - CURRENT logistics: Eventbrite live listing evt-bba-cle-fall26
        Sat Oct 24, 2026 | doors 8:30 AM, program 9:00 AM-3:30 PM ET
        Miami Riverside Conference Center, 400 NW North River Dr, Miami, FL
        (hotel ballroom out of service -> venue moved; Hyatt Regency was Feb-stale)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1500

# ---- palette sampled from the draft ----
NAVY   = (30, 39, 63)
CREAM  = (233, 227, 218)
GOLD   = (176, 141, 58)
INK    = (34, 34, 34)
GRAY   = (120, 118, 112)
WHITE  = (245, 242, 236)

FD = "/usr/share/fonts/truetype/liberation2"
def f(name, size):
    return ImageFont.truetype(f"{FD}/{name}.ttf", size)

serif_b   = lambda s: f("LiberationSerif-Bold", s)
serif_i   = lambda s: f("LiberationSerif-Italic", s)
serif_r   = lambda s: f("LiberationSerif-Regular", s)
serif_bi  = lambda s: f("LiberationSerif-BoldItalic", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def center(y, text, font, fill, tracking=0):
    if tracking:
        # manual letter spacing
        widths = [d.textlength(ch, font=font) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (W - total) / 2
        for ch, w in zip(text, widths):
            d.text((x, y), ch, font=font, fill=fill)
            x += w + tracking
        return
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)

# ---- header bar ----
d.rectangle([0, 0, W, 185], fill=NAVY)
center(40, "Biscayne Bar Association", serif_b(66), WHITE)
center(120, "The Ethics Hour", serif_i(40), WHITE)

# ---- main title (the big line, seminar title kept per listing) ----
center(258, "Fall Family Law CLE Seminar", serif_b(74), NAVY)

# ---- keynote block (was empty in the draft) ----
center(452, "KEYNOTE ADDRESS", serif_r(30), GOLD, tracking=8)
center(500, "Judge Marisa Cantwell (Ret.)", serif_b(52), NAVY)

# ---- logistics (current, from live listing) ----
center(690, "Saturday, October 24, 2026", serif_r(48), INK)
center(760, "9:00 AM to 3:30 PM  \u00b7  Doors open 8:30 AM", serif_r(40), INK)
center(824, "Miami Riverside Conference Center", serif_r(48), INK)
center(884, "400 NW North River Dr, Miami, FL 33134", serif_r(30), GRAY)

# ---- gold divider ----
d.rectangle([90, 952, W - 90, 955], fill=GOLD)

# ---- credit + registration ----
center(998, "7.0 CLE hours, including 1.0 ethics", serif_b(46), INK)
center(1072, "Registration open to all members", serif_r(38), GRAY)

# ---- footer accent bar (subtle, like spring template) ----
d.rectangle([0, H - 14, W, H], fill=NAVY)

img.save("/root/workspace/cle_flyer_fall.png")
# print-ready PDF as well (US Letter proportion source at 300dpi-ish)
img.save("/root/workspace/cle_flyer_fall.pdf", "PDF", resolution=150.0)
print("saved", img.size)

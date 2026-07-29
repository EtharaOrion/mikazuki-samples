#!/usr/bin/env python3
"""Build the Studio B east-wall acoustic panel proposal image."""
from PIL import Image, ImageDraw, ImageFont

W, H = 2000, 1500  # size flagged on the measure sheet (print sheet: "Panel proposal")

# ---- numbers ----
TREATABLE_SQFT = 192        # measure sheet, treatable area only
WALL_H_FT = 12              # measure sheet
WALL_W_FT = TREATABLE_SQFT / WALL_H_FT   # 16 ft
TARGET_PCT = 0.75           # panel spec, tracking room
PANEL_SQFT = 8              # spec SL-24, 2ft x 4ft
TARGET_SQFT = TREATABLE_SQFT * TARGET_PCT          # 144
PANELS_TOTAL = round(TARGET_SQFT / PANEL_SQFT)     # 18
INSTALLED = 7               # counted off Studio B east-wall photo card
ADD = PANELS_TOTAL - INSTALLED                     # 11

# ---- palette ----
BG = (24, 26, 30)
CARD = (36, 39, 46)
INK = (238, 240, 244)
MUTE = (150, 156, 166)
WALL = (58, 46, 40)
EXIST = (96, 100, 108)
NEW = (214, 158, 62)
NEW_ED = (245, 196, 110)
LINE = (70, 74, 82)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def font(sz, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
        "/usr/share/fonts/truetype/liberation/LiberationSans%s.ttf" % ("-Bold" if bold else ""),
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()

f_title = font(60, True)
f_sub = font(30)
f_h = font(36, True)
f_b = font(30)
f_bb = font(30, True)
f_s = font(24)
f_tag = font(26, True)

# header
d.text((70, 55), "Studio B \u2014 East Wall Acoustic Treatment", font=f_title, fill=INK)
d.text((72, 130), "Proposal for Elena's crew \u2022 Friday install \u2022 SoundLine SL-24 broadband panels", font=f_sub, fill=MUTE)
d.line((70, 185, W-70, 185), fill=LINE, width=2)

# ---- wall diagram (left) ----
dx, dy, dw, dh = 70, 240, 1120, 900
# scale wall to fit
scale = min(dw / WALL_W_FT, dh / WALL_H_FT)
wpx, hpx = WALL_W_FT * scale, WALL_H_FT * scale
ox = dx + (dw - wpx) / 2
oy = dy + (dh - hpx) / 2
d.rectangle((ox, oy, ox+wpx, oy+hpx), fill=WALL, outline=(120, 96, 78), width=3)
d.text((dx, dy-46), "East wall \u2014 %g ft W x %g ft H (%d sq ft treatable)" % (WALL_W_FT, WALL_H_FT, TREATABLE_SQFT),
       font=f_h, fill=INK)

# panel grid: SL-24 is 2ft wide x 4ft tall. Wall 16 wide x 12 high -> 8 cols x 3 rows = 24 slots.
pw_ft, ph_ft = 2, 4
cols = int(WALL_W_FT // pw_ft)   # 8
rows = int(WALL_H_FT // ph_ft)   # 3
gap = 10
pwpx = pw_ft * scale
phpx = ph_ft * scale
# place panels row-major; first INSTALLED = existing, next ADD = new, rest empty (gaps for 75%)
total_slots = cols * rows
placed = 0
for r in range(rows):
    for c in range(cols):
        x0 = ox + c * pwpx + gap/2
        y0 = oy + r * phpx + gap/2
        x1 = ox + (c+1) * pwpx - gap/2
        y1 = oy + (r+1) * phpx - gap/2
        if placed < INSTALLED:
            d.rectangle((x0, y0, x1, y1), fill=EXIST, outline=(140,144,152), width=2)
            d.text((x0+10, y0+10), "existing", font=f_s, fill=(30,32,36))
        elif placed < INSTALLED + ADD:
            d.rectangle((x0, y0, x1, y1), fill=NEW, outline=NEW_ED, width=3)
            d.text((x0+10, y0+10), "NEW", font=f_bb, fill=(40,28,10))
        placed += 1

# legend
ly = oy + hpx + 40
d.rectangle((ox, ly, ox+40, ly+30), fill=EXIST, outline=(140,144,152), width=2)
d.text((ox+52, ly), "Already on wall  (%d)" % INSTALLED, font=f_b, fill=INK)
d.rectangle((ox+430, ly, ox+470, ly+30), fill=NEW, outline=NEW_ED, width=3)
d.text((ox+482, ly), "Add now  (%d)" % ADD, font=f_bb, fill=INK)

# ---- summary card (right) ----
cx, cy, cw, ch = 1240, 240, 690, 1140
d.rounded_rectangle((cx, cy, cx+cw, cy+ch), radius=18, fill=CARD, outline=LINE, width=2)
tx = cx + 40
ty = cy + 40
d.text((tx, ty), "The count", font=f_h, fill=INK); ty += 70

rows_txt = [
    ("Treatable wall area", "%d sq ft" % TREATABLE_SQFT),
    ("Coverage target (tracking room)", "%d%%" % int(TARGET_PCT*100)),
    ("Area to treat", "%g sq ft" % TARGET_SQFT),
    ("Coverage per SL-24 panel", "%d sq ft" % PANEL_SQFT),
    ("Panels for target (144 \u00f7 8)", "%d" % PANELS_TOTAL),
    ("Already installed (photo card)", "%d" % INSTALLED),
]
for k, v in rows_txt:
    d.text((tx, ty), k, font=f_b, fill=MUTE)
    d.text((cx+cw-40, ty), v, font=f_bb, fill=INK, anchor="ra")
    ty += 58
    d.line((tx, ty-14, cx+cw-40, ty-14), fill=LINE, width=1)

ty += 20
d.rounded_rectangle((tx, ty, cx+cw-40, ty+130), radius=14, fill=(48, 40, 22), outline=NEW, width=3)
d.text((tx+30, ty+22), "Panels to add", font=f_h, fill=NEW_ED)
d.text((cx+cw-70, ty+18), str(ADD), font=font(80, True), fill=NEW, anchor="ra")
d.text((tx+30, ty+92), "18 for target  \u2212  7 installed  =  11", font=f_s, fill=(210,190,150))
ty += 170

d.text((tx, ty), "Order note", font=f_h, fill=INK); ty += 56
for ln in [
    "\u2022 SoundLine SL-24, 2 ft x 4 ft, NRC 0.95",
    "\u2022 Approved east-wall scope (not full-wall foam)",
    "\u2022 Not edge-to-edge \u2014 75% target leaves gaps",
    "\u2022 Est. order ~$765  (over the $200 line)",
    "\u2022 Ticket left ON HOLD for Jessica's approval",
]:
    d.text((tx, ty), ln, font=f_b, fill=INK); ty += 50

# footer tag
d.text((70, H-46), "Source: panel_measure.xlsx (192 sq ft, 2000x1500) \u2022 panel_spec.pdf (SL-24, 75%) \u2022 Studio B east-wall photo card (7 installed)",
       font=f_s, fill=MUTE)

import os
outdir = "/root/workspace/home/Documents/Studio B Reno"
os.makedirs(outdir, exist_ok=True)
out = os.path.join(outdir, "proposal.png")
img.save(out, "PNG")
print("saved", out, img.size)

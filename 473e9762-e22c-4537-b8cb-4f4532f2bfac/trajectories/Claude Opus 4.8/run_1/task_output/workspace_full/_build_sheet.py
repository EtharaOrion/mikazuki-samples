#!/usr/bin/env python3
"""Build the Josefstadt Stop 3 docent look-and-find study sheet (A5 landscape, 300 dpi)."""
from PIL import Image, ImageDraw, ImageFont

# ---- canvas: A5 landscape @ 300 dpi ----
W, H = 2480, 1748
CREAM = (250, 245, 232)
INK = (36, 33, 30)
SUB = (92, 84, 74)
ACCENT = (150, 42, 42)
BAND = (43, 38, 40)
RULE = (176, 158, 120)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

FD = "/usr/share/fonts/truetype/dejavu/"
def f(name, sz): return ImageFont.truetype(FD + name, sz)
serif_b = lambda s: f("DejaVuSerif-Bold.ttf", s)
serif   = lambda s: f("DejaVuSerif.ttf", s)
sans    = lambda s: f("DejaVuSans.ttf", s)
sans_b  = lambda s: f("DejaVuSans-Bold.ttf", s)

def text_w(dr, s, font):
    b = dr.textbbox((0, 0), s, font=font); return b[2] - b[0]

def wrap(dr, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(dr, t, font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

MARGIN = 60

# ================= HEADER BAND =================
hb_top, hb_bot = 40, 214
d.rectangle([0, hb_top, W, hb_bot], fill=BAND)
d.rectangle([0, hb_bot, W, hb_bot + 6], fill=RULE)
title = "Palais Josefsplatz No. 5"
d.text((MARGIN, 66), title, font=serif_b(70), fill=CREAM)
d.text((MARGIN, 156), "Josefstadt Walking Tour  \u00b7  Stop 3 of 5  \u00b7  Look-and-Find Study Sheet",
       font=sans(30), fill=(214, 205, 188))
# small ref, right-aligned in band
ref = "EDU-DT-WT-JS-03"
d.text((W - MARGIN - text_w(d, ref, sans(28)), 168), ref, font=sans(28), fill=(190, 180, 162))

# ================= LAYOUT COLUMNS =================
content_top = hb_bot + 30
footer_top = H - 118
left_x0 = MARGIN
left_x1 = MARGIN + int((2/3) * (W - 2 * MARGIN))   # left two-thirds
right_x0 = left_x1 + 34
right_x1 = W - MARGIN

# ---- cover photograph (cropped to include all four features) ----
photo = Image.open("/root/workspace/home/Applications/img6.jpg").convert("RGB")
pw, ph = photo.size
# crop vertical extent 0.40..1.0 (cornice down to threshold), full width
crop = photo.crop((0, int(0.40 * ph), pw, ph))
cw, ch = crop.size                       # ratio ~1.25
box_w = 1250
box_h = int(box_w * ch / cw)             # ~1000
crop = crop.resize((box_w, box_h), Image.LANCZOS)
px, py = left_x0, content_top
# thin frame
d.rectangle([px - 4, py - 4, px + box_w + 4, py + box_h + 4], outline=INK, width=4)
img.paste(crop, (px, py))

# ---- callouts on the photo (normalized coords within the crop) ----
callouts = [
    (1, 0.150, 0.62),   # caryatid figures (left)
    (2, 0.510, 0.45),   # plaque number on door
    (3, 0.500, 0.215),  # cornice above door
    (4, 0.500, 0.93),   # threshold pavement stone
]
R = 40
cf = sans_b(46)
for n, nx, ny in callouts:
    cx = px + int(nx * box_w); cy = py + int(ny * box_h)
    d.ellipse([cx - R - 5, cy - R - 5, cx + R + 5, cy + R + 5], fill=(255, 255, 255))  # halo
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=ACCENT)
    s = str(n); tw = text_w(d, s, cf)
    tb = d.textbbox((0, 0), s, font=cf)
    d.text((cx - tw / 2, cy - (tb[3] - tb[1]) / 2 - tb[1]), s, font=cf, fill=(255, 255, 255))

# ---- callout legend (below the photograph) ----
leg_y = py + box_h + 26
d.text((left_x0, leg_y), "Look and find \u2014 walk the cohort through, in order",
       font=serif_b(38), fill=INK)
leg_y += 58
legend = [
    "Caryatid figures flanking the door \u2014 count how many stand, and note what they carry.",
    "Plaque number on the wooden door \u2014 read it aloud to confirm the address (No. 5).",
    "Cornice above the door frame \u2014 note the acanthus band and dentil moulding.",
    "Threshold pavement stone \u2014 look for the salon plaque installed in 2003.",
]
lf = sans(28); nf = sans_b(28)
for i, item in enumerate(legend, 1):
    d.text((left_x0, leg_y), f"{i}.", font=nf, fill=ACCENT)
    lines = wrap(d, item, lf, left_x1 - (left_x0 + 44))
    for ln in lines:
        d.text((left_x0 + 44, leg_y), ln, font=lf, fill=INK); leg_y += 36
    leg_y += 12

# ================= BIOGRAPHICAL BLOCK (right third) =================
bx = right_x0
by = content_top
# tinted panel
d.rectangle([bx - 10, by - 6, right_x1 + 10, footer_top - 20], outline=RULE, width=3)
d.rectangle([bx - 10, by - 6, right_x1 + 10, by + 66], fill=BAND)
d.text((bx + 14, by + 8), "FEATURED ARTIST", font=sans_b(34), fill=CREAM)
by += 96
d.text((bx + 8, by), "Marta Steiner", font=serif_b(52), fill=INK); by += 66
d.text((bx + 8, by), "1867 \u2013 1934  \u00b7  Vienna", font=sans(30), fill=SUB); by += 60
d.line([bx + 8, by, right_x1 - 8, by], fill=RULE, width=2); by += 26

bio_lines = [
    "Vienna painter and printmaker; a second-wave Secessionist.",
    "Best known for small-format portraits of women artists in her circle.",
    "Kept a salon on the ground floor of this caryatid facade palais on Josefsplatz, 1898\u20131912.",
    "Collection holds three drypoints and two oils on panel.",
    "District salon plaque installed on the doorstep in 2003.",
]
bf = sans(30)
for bl in bio_lines:
    d.text((bx + 8, by), "\u2022", font=sans_b(30), fill=ACCENT)
    for ln in wrap(d, bl, bf, right_x1 - (bx + 44)):
        d.text((bx + 44, by), ln, font=bf, fill=INK); by += 40
    by += 14

# ================= FOOTER BAND =================
d.line([MARGIN, footer_top, W - MARGIN, footer_top], fill=RULE, width=3)
fy = footer_top + 34
d.text((MARGIN, fy), "S6 cohort (autumn intake)", font=sans_b(32), fill=INK)
wm = "O S T E R R E I C H I S C H E S   K U N S T M U S E U M"
d.text((W - MARGIN - text_w(d, wm, serif_b(30)), fy + 2), wm, font=serif_b(30), fill=INK)

# ================= SAVE =================
out = "/root/workspace/home/Desktop/josefsplatz_no5_stop3_study_sheet.png"
img.save(out, "PNG", dpi=(300, 300))
print("saved", out, img.size)

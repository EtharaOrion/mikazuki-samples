#!/usr/bin/env python3
"""Compose the Vienna Modern save-the-date card from the V5 board-approved copy.

Cover : home/Music/img1.jpg  (Secession Building golden dome, board pick 15 Sep 2026)
Copy  : press_card_v5_board_approved.docx  (LOCKED FOR PRINT)
Style : Pictures/typography_specs.md  (warm gold #C8A250, off-black #1E1B18,
        full-bleed cover top, title lower third, credit beneath date block,
        hairline rule above credit). FF Ver Sacrum unavailable -> serif display
        fallback in the Secession spirit; Univers unavailable -> clean sans body.
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

SRC   = "/root/workspace/home/Music/img1.jpg"
OUT   = "/root/workspace/home/Desktop/vienna_modern_save_the_date.jpg"

GOLD   = (200, 162, 80)     # #C8A250 secession dome tone
OFFBLK = (30, 27, 24)       # #1E1B18
CREAM  = (244, 240, 232)
WHITE  = (250, 248, 244)

# Card canvas: A5-ish portrait at print-ish density
W, H = 1240, 1748

# ---- fonts -----------------------------------------------------------------
def font(path, size):
    return ImageFont.truetype(path, size)

# Display: serif nod to Ver Sacrum lettering (fallback per specs).
DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS    = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf"
SANSB   = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf"

f_title   = font(DISPLAY, 74)
f_title2  = font(DISPLAY, 74)
f_kicker  = font(SANSB, 30)
f_date    = font(SANSB, 44)
f_sub     = font(SANS, 30)
f_credit  = font(SANS, 24)

# ---- cover -----------------------------------------------------------------
cover = Image.open(SRC).convert("RGB")
# Full-bleed cover occupies the top ~62% of the card; title band sits in the
# lower third over a solid off-black block (keeps the copy crisp & legible).
cover_h = int(H * 0.575)
cw, ch = cover.size
scale = max(W / cw, cover_h / ch)
cover = cover.resize((int(cw * scale), int(ch * scale)), Image.LANCZOS)
# crop toward the top so the golden dome stays in frame
left = (cover.width - W) // 2
top  = int((cover.height - cover_h) * 0.28)
cover = cover.crop((left, top, left + W, top + cover_h))
cover = ImageEnhance.Contrast(cover).enhance(1.05)

card = Image.new("RGB", (W, H), OFFBLK)
card.paste(cover, (0, 0))

# subtle gradient scrim at the base of the cover so it reads into the band
scrim = Image.new("L", (1, cover_h), 0)
for y in range(cover_h):
    t = max(0.0, (y - cover_h * 0.72) / (cover_h * 0.28))
    scrim.putpixel((0, y), int(150 * t))
scrim = scrim.resize((W, cover_h))
black = Image.new("RGB", (W, cover_h), OFFBLK)
card.paste(Image.composite(black, cover, scrim), (0, 0))

d = ImageDraw.Draw(card)

def ctext(y, txt, fnt, fill, ls=0):
    w = d.textlength(txt, font=fnt) + ls * (len(txt) - 1)
    x = (W - w) / 2
    if ls == 0:
        d.text((x, y), txt, font=fnt, fill=fill)
    else:
        for chn in txt:
            d.text((x, y), chn, font=fnt, fill=fill)
            x += d.textlength(chn, font=fnt) + ls
    return y

# ---- lower band ------------------------------------------------------------
band_top = cover_h
d.rectangle([0, band_top, W, H], fill=OFFBLK)

# kicker lives in the dark band for clean contrast, on the title axis
y = band_top + 48
ctext(y, "SAVE THE DATE", f_kicker, GOLD, ls=8)

y += 60
ctext(y, "Vienna Modern", f_title, WHITE)
y += 92
ctext(y, "Art and Society 1890\u20131930", f_title2, GOLD)

# gold hairline separators around the date block
y += 128
d.line([(W*0.20, y), (W*0.80, y)], fill=GOLD, width=2)

y += 40
ctext(y, "OPENS 1 OCTOBER 2026", f_date, WHITE, ls=3)
y += 62
ctext(y, "Doors 18:30  \u00b7  Ringstrasse main entrance", f_sub, CREAM)
y += 46
ctext(y, "Osterreichisches Kunstmuseum, Vienna", f_sub, CREAM)
y += 46
ctext(y, "Ministerial ribbon cut \u00b7 Bundesministerin Clara Winkler", f_sub, GOLD)

y += 58
d.line([(W*0.20, y), (W*0.80, y)], fill=GOLD, width=2)   # hairline above credit

# ---- credit line (exact, locked 15 Sep 2026) -------------------------------
y += 34
ctext(y, "A production of Osterreichisches Kunstmuseum", f_credit, CREAM)
y += 34
ctext(y, "in cooperation with the Osterreichische Nationalbibliothek", f_credit, CREAM)

card.save(OUT, "JPEG", quality=92)
print("wrote", OUT, card.size)

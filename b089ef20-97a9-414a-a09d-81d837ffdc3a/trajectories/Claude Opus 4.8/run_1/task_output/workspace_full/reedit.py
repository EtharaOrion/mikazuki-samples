#!/usr/bin/env python3
"""
Re-edit the off-brand 07-08 post to the Eleanor's Tavern house look.
House look (per style sheet rev 4): warm tungsten/amber, dark ground,
tight square crop on the food, corners fall off dark.
Produces: the corrected image + a labeled before/after side-by-side.
No live post is touched or removed.
"""
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter
import math

SRC = "/root/workspace/home/Pictures/post_2026_07_08.jpg"
OUT_AFTER = "/root/workspace/reedit_2026_07_08_after.jpg"
OUT_COMPARE = "/root/workspace/reedit_2026_07_08_before_after.jpg"

orig = Image.open(SRC).convert("RGB")
W, H = orig.size  # 1080 x 1350

# 1) TIGHT SQUARE CROP on the food. The plate sits left-of-centre with
#    empty bright negative space on the right, so bias the square left and
#    crop in to kill the café-style airiness.
side = int(min(W, H) * 0.74)          # crop in, then crop in again
left = 0                               # hard-left: kill the blown-out empty wall on the right
top = int((H - side) * 0.55)           # keep the stack, trim empty top
left = max(0, min(left, W - side))
top = max(0, min(top, H - side))
img = orig.crop((left, top, left + side, top + side))
img = img.resize((1080, 1080), Image.LANCZOS)

# 2) WARM WHITE BALANCE. Pull the cool daylight cast toward tungsten amber:
#    lift reds, hold greens, drop blues.
r, g, b = img.split()
r = r.point(lambda v: min(255, int(v * 1.12 + 6)))
g = g.point(lambda v: min(255, int(v * 1.02)))
b = b.point(lambda v: int(v * 0.82))
img = Image.merge("RGB", (r, g, b))

# 3) TAME THE BLOWN DAYLIGHT. Compress the pale highlights first so the
#    near-white wall/wood stops reading as bright café daylight, then drop
#    exposure, deepen the ground, add contrast and glossy-food saturation.
def rolloff(v):
    # gentle progressive shoulder above ~120 (no flat plateau -> no milky haze)
    if v <= 120:
        return v
    over = v - 120
    return int(120 + over * (0.55 - 0.0009 * over))
img = img.point(rolloff)
img = ImageEnhance.Brightness(img).enhance(0.82)
img = ImageEnhance.Contrast(img).enhance(1.28)
img = ImageEnhance.Color(img).enhance(1.14)

# 4) CORNERS FALL OFF DARK. Radial vignette pooling light on the plate.
w, h = img.size
cx, cy = w / 2.0, h * 0.44   # lift centre so the base/lower corners darken too
maxd = math.hypot(cx, cy)
mask = Image.new("L", (w, h), 0)
mpx = mask.load()
for y in range(h):
    dy = (y - cy)
    for x in range(w):
        d = math.hypot(x - cx, dy) / maxd
        # brightness multiplier: 1.0 centre -> ~0.18 corners (pool the light)
        val = 1.0 - 0.82 * (d ** 1.9)
        mpx[x, y] = int(max(0.0, min(1.0, val)) * 255)
mask = mask.filter(ImageFilter.GaussianBlur(40))
black = Image.new("RGB", (w, h), (0, 0, 0))
img = Image.composite(img, black, mask)

# Final pass: cut residual haze with a black-point + gamma curve so the
# lifted daylight blacks sink back down, then set the tungsten pool.
BP = 24.0
GAMMA = 1.14
_lut = [int(255 * (max(0.0, i - BP) / (255.0 - BP)) ** GAMMA) for i in range(256)]
img = img.point(_lut * 3)
img = ImageEnhance.Contrast(img).enhance(1.06)
img = ImageEnhance.Color(img).enhance(1.06)
img.save(OUT_AFTER, quality=92)
print("wrote", OUT_AFTER)

# ---- BEFORE / AFTER side-by-side, both squared to 1080, labeled ----
def square(im):
    w, h = im.size
    s = min(w, h)
    l = (w - s) // 2
    t = (h - s) // 2
    return im.crop((l, t, l + s, t + s)).resize((1080, 1080), Image.LANCZOS)

before = square(orig)
after = img
gap = 24
label_h = 96
cw = 1080 * 2 + gap
ch = 1080 + label_h + 20
canvas = Image.new("RGB", (cw, ch), (17, 17, 17))
canvas.paste(before, (0, label_h))
canvas.paste(after, (1080 + gap, label_h))
draw = ImageDraw.Draw(canvas)

def load_font(size):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

f = load_font(46)
fs = load_font(28)
draw.text((30, 22), "BEFORE  \u2014  as posted 07-18 (off house look)",
          font=f, fill=(230, 120, 110))
draw.text((1080 + gap + 30, 22), "AFTER  \u2014  re-edit to the house look",
          font=f, fill=(150, 210, 150))
draw.text((30, 66), "cool daylight \u00b7 pale wood \u00b7 loose crop",
          font=fs, fill=(150, 150, 150))
draw.text((1080 + gap + 30, 66), "warm tungsten \u00b7 dark ground \u00b7 tight square \u00b7 dark corners",
          font=fs, fill=(150, 150, 150))
canvas.save(OUT_COMPARE, quality=92)
print("wrote", OUT_COMPARE, canvas.size)

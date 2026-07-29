#!/usr/bin/env python3
"""Build the final digital poster for the Crossroads 5th Anniversary Showcase.
Size 1080x1350 (4:5, the digital/feed spec from Claire's asset sheet).
Copy corrected to match the ticket page: Music 6:30 PM (venue pushed +30),
Adult $15 / under 12 free (no $25/$60 tiers). Proof/not-for-print mark removed.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350

# palette
CREAM = (239, 231, 210)
GOLD  = (201, 162, 75)
GOLD_HI = (222, 186, 104)
MUTED = (150, 150, 150)
LINE  = (120, 96, 44)

FSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FSR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FMONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"

def f(path, sz):
    return ImageFont.truetype(path, sz)

# ---- background: dark, with a warm golden stage glow in the middle ----
cx, cy = W / 2, H * 0.46
maxd = math.hypot(W, H) * 0.5
pixels = []
for y in range(H):
    vy = min(1.0, min(y / H, (H - y) / H) * 2.6)  # falloff to near-black top/bottom
    for x in range(W):
        dist = math.hypot(x - cx, y - cy) / maxd
        glow = max(0.0, 1.0 - dist * 1.55) ** 1.7
        base = 12
        r = min(150, int(base + glow * 96 * vy))
        g = min(110, int(base + glow * 62 * vy))
        b = min(60, int(base + glow * 24 * vy))
        pixels.append((r, g, b))
img = Image.new("RGB", (W, H))
img.putdata(pixels)
d = ImageDraw.Draw(img)

# ---- frame ----
m = 30
d.rectangle([m, m, W - m, H - m], outline=GOLD, width=3)

def center(text, y, font, fill, tracking=0):
    if tracking:
        # letter-spaced draw
        widths = [d.textlength(ch, font=font) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (W - total) / 2
        asc, desc = font.getmetrics()
        for ch, wch in zip(text, widths):
            d.text((x, y), ch, font=font, fill=fill)
            x += wch + tracking
        return y + asc + desc
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) / 2 - bbox[0], y), text, font=font, fill=fill)
    return y + (bbox[3] - bbox[1])

def rule(y, half=380):
    d.line([(W / 2 - half, y), (W / 2 + half, y)], fill=LINE, width=2)

DOT = "  \u00b7  "

# ---- header ----
y = 70
center("CROSSROADS CONSERVATORY OF MUSIC", y, f(FSB, 30), GOLD, tracking=2); y += 44
center("1420 GRAND BLVD" + DOT + "KANSAS CITY", y, f(FSR, 19), MUTED, tracking=2); y += 46
rule(y, 300); y += 40

# ---- main title ----
center("FIVE", y, f(FSB, 150), CREAM, tracking=6); y += 148
center("YEARS", y, f(FSB, 150), CREAM, tracking=6); y += 168
center("5TH ANNIVERSARY SHOWCASE", y, f(FSB, 40), GOLD_HI, tracking=5); y += 78

# ---- date / venue ----
center("SATURDAY" + DOT + "OCTOBER 10" + DOT + "2026", y, f(FSB, 34), CREAM, tracking=3); y += 52
center("THE PHOENIX" + DOT + "302 W 8TH ST" + DOT + "KANSAS CITY", y, f(FSR, 20), MUTED, tracking=2); y += 48
rule(y); y += 34

# ---- time + price (the corrected lines) ----
center("DOORS 5:30 PM" + DOT + "MUSIC 6:30 PM", y, f(FSB, 34), CREAM, tracking=3); y += 52
center("ADULT $15" + DOT + "UNDER 12 FREE", y, f(FSB, 32), GOLD_HI, tracking=3); y += 50
rule(y); y += 34

# ---- program ----
center("STUDENT ENSEMBLES FROM EVERY STUDIO", y, f(FSR, 21), MUTED, tracking=2); y += 34
center("BEGINNING STRINGS" + DOT + "YOUTH JAZZ COMBO", y, f(FSR, 21), MUTED, tracking=1); y += 34
center("ADVANCED JAZZ ENSEMBLE" + DOT + "ADULT THEORY PLAYERS", y, f(FSR, 21), MUTED, tracking=1); y += 44
center("CLOSING SET BY", y, f(FSR, 20), MUTED, tracking=3); y += 36
center("THE JESSICA WEBB QUARTET", y, f(FSB, 33), CREAM, tracking=2); y += 46
center("JESSICA WEBB" + DOT + "RAY COLEMAN" + DOT + "LUKE VANCE" + DOT + "TOMOKO ISHIDA",
       y, f(FSR, 18), MUTED, tracking=1); y += 46
rule(y); y += 30

# ---- ticketing ----
center("TICKETS AT THE DOOR OR ONLINE", y, f(FSR, 20), MUTED, tracking=2); y += 34
center("CROSSROADSCONSERVATORY.COM", y, f(FSB, 26), GOLD_HI, tracking=3); y += 40

img.save("/root/workspace/poster.png")
print("saved /root/workspace/poster.png", img.size)

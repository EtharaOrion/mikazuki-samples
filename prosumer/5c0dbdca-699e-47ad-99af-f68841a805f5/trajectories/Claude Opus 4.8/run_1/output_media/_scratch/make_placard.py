#!/usr/bin/env python3
"""Generate the Studio B East teen ensemble door placard (portrait 1200x1600)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 1600  # Room placard size flagged by Claire (placard_spec: portrait 1200x1600)

INK   = (28, 32, 38)      # near-black warm ink
CREAM = (247, 243, 234)   # warm paper
BRASS = (176, 132, 58)    # brass accent
RUST  = (155, 66, 42)     # deep rust
MUTE  = (96, 90, 80)      # muted text

serif  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
serifb = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
sans   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
sansb  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# Outer border frame
m = 46
d.rectangle([m, m, W - m, H - m], outline=INK, width=6)
d.rectangle([m + 16, m + 16, W - m - 16, H - m - 16], outline=BRASS, width=3)

def center(text, y, font, fill, spacing=0):
    if spacing:
        # letter-spaced draw
        widths = [d.textlength(ch, font=font) for ch in text]
        total = sum(widths) + spacing * (len(text) - 1)
        x = (W - total) / 2
        asc, desc = font.getmetrics()
        for ch, w in zip(text, widths):
            d.text((x, y), ch, font=font, fill=fill)
            x += w + spacing
        return y + asc + desc
    else:
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        d.text(((W - tw) / 2, y), text, font=font, fill=fill)
        return y + (bbox[3] - bbox[1])

# --- Header: school name ---
center("CROSSROADS CONSERVATORY OF MUSIC", 120, f(sansb, 30), MUTE, spacing=3)
d.line([(W/2 - 220, 178), (W/2 + 220, 178)], fill=BRASS, width=3)

# --- Room identifier ---
center("STUDIO B EAST", 250, f(sansb, 92), INK, spacing=6)

# --- Main title ---
center("TEEN JAZZ", 470, f(serifb, 150), RUST)
center("ENSEMBLE", 640, f(serifb, 150), RUST)

# --- Rehearsal banner ---
by0, by1 = 850, 985
d.rectangle([m + 60, by0, W - m - 60, by1], fill=INK)
center("REHEARSAL IN SESSION", by0 + 22, f(sansb, 52), CREAM, spacing=4)
center("Please do not disturb", by0 + 88, f(serif, 34), BRASS)

# --- Schedule / details ---
y = 1070
center("Thursdays  ·  7:00 – 9:00 PM", y, f(serif, 46), INK)
center("Directed by Ray Coleman", y + 74, f(serif, 38), MUTE)

# --- Music note flourish ---
center("\u266B", 1250, f(serifb, 88), BRASS)

# --- Footer ---
d.line([(W/2 - 300, 1400), (W/2 + 300, 1400)], fill=BRASS, width=2)
center("1420 Grand Blvd  ·  Crossroads Arts District", 1430, f(sans, 28), MUTE)
center("Kansas City, Missouri", 1478, f(sans, 28), MUTE)

out_dir = "/root/workspace/Ensemble Setup"
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "placard.png")
img.save(out, "PNG")
print("saved", out, img.size)

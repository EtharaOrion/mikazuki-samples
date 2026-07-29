#!/usr/bin/env python3
"""Annotate the current (fall build 2.4.1) intake screen against the Sept CRs."""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

SRC = "/root/workspace/home/home/Pictures/portal_v2.png"
OUT = "/root/workspace/intake_audit/markup_current_build_v2.4.1.png"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

shot = Image.open(SRC).convert("RGB")
W, H = shot.size                      # 2560 x 1600
TOP, RIGHT, BOT, LEFT = 170, 1040, 70, 20
canvas = Image.new("RGB", (LEFT + W + RIGHT, TOP + H + BOT), "white")
canvas.paste(shot, (LEFT, TOP))
d = ImageDraw.Draw(canvas)

def font(sz, bold=True):
    p = "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % ("Bold" if bold else "Regular")
    return ImageFont.truetype(p, sz)

f_banner = font(44); f_sub = font(26, False)
f_card_h = font(30); f_card = font(26, False); f_badge = font(34)
f_leg = font(24, False); f_leg_h = font(26)

RED   = (200, 40, 40)
AMBER = (214, 140, 10)
GREEN = (40, 120, 55)
DARK  = (28, 34, 45)

# ---- top banner ----
d.rectangle([0, 0, canvas.width, TOP], fill=DARK)
d.text((LEFT, 26), "INTAKE PORTAL — COMPLIANCE MARKUP", font=f_banner, fill="white")
d.text((LEFT, 86),
       "Current fall build 2.4.1 (Oct 2026) checked against September committee change requests CR-4 to CR-7.  "
       "Red = requirement NOT met · Amber = not verified / needs confirmation.",
       font=f_sub, fill=(230, 230, 230))
d.text((LEFT, 124), "Vendor asked to mark the review \"passed\" and go live Friday. Do NOT sign off: see flags below.",
       font=f_sub, fill=(255, 190, 190))

def ox(x): return LEFT + x
def oy(y): return TOP + y

def outline(box, color, w=7):
    x1, y1, x2, y2 = box
    d.rectangle([ox(x1), oy(y1), ox(x2), oy(y2)], outline=color, width=w)

def badge(cx, cy, n, color):
    r = 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color, outline="white", width=4)
    tb = d.textbbox((0, 0), str(n), font=f_badge)
    d.text((cx - (tb[2]-tb[0])/2, cy - (tb[3]-tb[1])/2 - 4), str(n), font=f_badge, fill="white")

def card(x, y, w, h, color, title, body):
    d.rectangle([x, y, x + w, y + h], fill="white", outline=color, width=4)
    d.rectangle([x, y, x + w, y + 46], fill=color)
    d.text((x + 14, y + 8), title, font=f_card_h, fill="white")
    ty = y + 58
    for line in body.split("\n"):
        for seg in textwrap.wrap(line, 46) or [""]:
            d.text((x + 14, ty), seg, font=f_card, fill=(25, 25, 25)); ty += 30
    return y + h

def connect(bx, by, cx, cy, color):
    d.line([bx, by, cx, cy], fill=color, width=4)

# ---- element boxes on the screenshot (original coords, read off grid) ----
box_mentee   = (64, 1005, 326, 1058)    # CR-7 heading "Mentee information"
box_source   = (70, 1140, 800, 1332)    # CR-4 source dropdown + open options
box_sla      = (62, 1342, 514, 1392)    # CR-5 response-time promise
box_widget   = (1655, 425, 2505, 1000)  # CR-6 pairing stats card

outline(box_mentee, RED)
outline(box_source, AMBER)
outline(box_sla,    AMBER)
outline(box_widget, AMBER)

# badges near each element
b7 = (ox(346), oy(1031));  badge(*b7, 7, RED)
b4 = (ox(812), oy(1165));  badge(*b4, 4, AMBER)
b5 = (ox(530), oy(1367));  badge(*b5, 5, AMBER)
b6 = (ox(1665), oy(452));  badge(*b6, 6, AMBER)

# ---- callout cards in right panel ----
CX = LEFT + W + 24
CW = RIGHT - 44
y = TOP + 6
y = card(CX, y, CW, 244, RED,
    "CR-7  NOT MET  — Rename \"Mentee\" to \"Participant\"",
    "The section still reads \"Mentee information.\" The label was NOT "
    "renamed anywhere on the intake screen. This is the clearest, "
    "at-a-glance failure and directly contradicts the vendor's claim "
    "that all September CRs are in this build.") + 22
connect(CX, y - 146, b7[0] + 34, b7[1], RED)

y = card(CX, y, CW, 244, AMBER,
    "CR-4  NOT VERIFIED — Source list mirrors CRM",
    "Dropdown changed \"Bar Referral\" to \"Friend or colleague.\" "
    "Not confirmed to mirror the CRM lead-source picklist, and dropping "
    "a Bar-specific source for a Bar program is a red flag. Reconcile "
    "the options to the CRM list before sign-off.") + 22
connect(CX, y - 146, b4[0] + 34, b4[1], AMBER)

y = card(CX, y, CW, 214, AMBER,
    "CR-5  NEEDS CHECK — Response promise per SLA",
    "Promise LOOSENED from \"five\" to \"ten business days.\" Verify the "
    "number against the actual intake SLA before it goes public; a "
    "longer public commitment may be the wrong direction.") + 22
connect(CX, y - 128, b5[0] + 34, b5[1], AMBER)

y = card(CX, y, CW, 214, AMBER,
    "CR-6  NOT VERIFIED — Widget reads live from CRM",
    "Card is still labeled \"UAT preview\" and only shows a static count "
    "(9 -> 11 between builds). \"Live from CRM\" cannot be confirmed from "
    "a screenshot; require a live data demo.") + 22
connect(CX, y - 128, b6[0], b6[1], AMBER)

# legend
ly = y + 10
d.text((CX, ly), "Legend", font=f_leg_h, fill=DARK); ly += 34
for c, t in [(RED, "Requirement NOT met — must fix"),
             (AMBER, "Not verifiable from build — confirm"),
             (GREEN, "Verified against requirement")]:
    d.rectangle([CX, ly + 4, CX + 26, ly + 26], fill=c)
    d.text((CX + 36, ly), t, font=f_leg, fill=(25, 25, 25)); ly += 34

canvas.save(OUT)
print("wrote", OUT, canvas.size)

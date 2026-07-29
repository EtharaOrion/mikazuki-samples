#!/usr/bin/env python3
"""Side-by-side: prior build 2.3 (what we had) vs current build 2.4.1 (what the system says)."""
from PIL import Image, ImageDraw, ImageFont
import os
V1 = "/root/workspace/home/home/Pictures/portal_v1.png"
V2 = "/root/workspace/home/home/Pictures/portal_v2.png"
OUT = "/root/workspace/intake_audit/compare_before_after.png"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

def font(sz, bold=True):
    p = "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % ("Bold" if bold else "Regular")
    return ImageFont.truetype(p, sz)

RED, AMBER, DARK = (200,40,40), (214,140,10), (28,34,45)
SC = 0.46
sw, sh = int(2560*SC), int(1600*SC)          # 1177 x 736
GAP, ML, TOP, LBL, BOT = 70, 40, 150, 44, 300
W = ML + sw + GAP + sw + ML
Hc = TOP + LBL + sh + BOT
canvas = Image.new("RGB", (W, Hc), "white")
d = ImageDraw.Draw(canvas)

fb, fs, fl, fn = font(40), font(24, False), font(28), font(30)
fnote_h, fnote = font(27), font(24, False)

# regions in original coords -> id, color
regions = [
    (1, (64,1000,330,1060),   RED,   "Mentee heading"),
    (2, (95,1282,802,1334),   AMBER, "Source option"),
    (3, (60,1340,516,1394),   AMBER, "SLA sentence"),
    (4, (1880,688,2130,840),  AMBER, "Pairings widget"),
]

def place(img_path, x0, title, sub):
    im = Image.open(img_path).convert("RGB").resize((sw, sh))
    canvas.paste(im, (x0, TOP + LBL))
    d.text((x0, TOP + 4), title, font=fl, fill=DARK)
    d.text((x0, TOP + LBL - 2 + sh + 8), sub, font=fs, fill=(90,90,90))
    for rid, (a,b,c,dd), col, _ in regions:
        box = (x0 + int(a*SC), TOP+LBL + int(b*SC), x0 + int(c*SC), TOP+LBL + int(dd*SC))
        d.rectangle(box, outline=col, width=4)
        # badge at top-left of box
        bx, by = box[0]-2, box[1]-2
        r = 17
        d.ellipse([bx-r, by-r, bx+r, by+r], fill=col, outline="white", width=3)
        tb = d.textbbox((0,0), str(rid), font=font(24))
        d.text((bx-(tb[2]-tb[0])/2, by-(tb[3]-tb[1])/2-3), str(rid), font=font(24), fill="white")

# banner
d.rectangle([0,0,W,TOP], fill=DARK)
d.text((ML, 22), "INTAKE PORTAL — BEFORE vs AFTER (Sept CR check)", font=fb, fill="white")
d.text((ML, 78), "What we had  ->  what the vendor delivered. Only 2 of 4 requested items changed at all; the others need proof.",
       font=fs, fill=(225,225,225))

place(V1, ML, "BEFORE  ·  build 2.3 (Aug 2026)", "Prior pilot build")
place(V2, ML + sw + GAP, "AFTER  ·  build 2.4.1 (Oct 2026)  — current", "Vendor's fall build, proposed for Friday go-live")

# notes panel
ny = TOP + LBL + sh + 60
d.text((ML, ny), "Change check", font=fnote_h, fill=DARK); ny += 40
notes = [
 (RED,   "1  CR-7 Rename Mentee->Participant: UNCHANGED. Still \"Mentee information\" in BOTH builds. Requirement NOT met."),
 (AMBER, "2  CR-4 Source mirrors CRM: \"Bar Referral\" became \"Friend or colleague.\" Must confirm it matches the CRM lead-source list."),
 (AMBER, "3  CR-5 Response promise per SLA: \"five\" -> \"ten business days.\" Promise got LOOSER; verify the number against the intake SLA."),
 (AMBER, "4  CR-6 Pairings widget live from CRM: count moved 9 -> 11 but card is still \"UAT preview.\" Live CRM read not demonstrated."),
]
for col, t in notes:
    d.rectangle([ML, ny+4, ML+26, ny+30], fill=col)
    d.text((ML+40, ny), t, font=fnote, fill=(25,25,25)); ny += 40

canvas.save(OUT)
print("wrote", OUT, canvas.size)

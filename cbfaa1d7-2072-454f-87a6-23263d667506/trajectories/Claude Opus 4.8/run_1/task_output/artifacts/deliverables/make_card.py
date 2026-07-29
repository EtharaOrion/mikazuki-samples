from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1400
paper = (246, 241, 232)   # cream
ink = (28, 26, 36)        # near-black
maroon = (107, 39, 55)    # burgundy accent
gold = (184, 145, 80)

img = Image.new("RGB", (W, H), paper)
d = ImageDraw.Draw(img)

def font(path, size):
    return ImageFont.truetype(path, size)

serif_b = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
serif_r = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
sans_r  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

f_head   = font(serif_b, 40)
f_title  = font(serif_b, 52)
f_sess   = font(serif_b, 64)
f_price  = font(serif_b, 165)
f_body   = font(serif_r, 34)
f_small  = font(sans_r, 26)

# outer border frame
m = 60
d.rectangle([m, m, W-m, H-m], outline=ink, width=3)
inner = 78
d.rectangle([inner, inner, W-inner, H-inner], outline=gold, width=1)

def ctext(y, text, fnt, fill):
    bb = d.textbbox((0,0), text, font=fnt)
    w = bb[2]-bb[0]
    d.text(((W-w)/2, y), text, font=fnt, fill=fill)
    return y + (bb[3]-bb[1])

y = 170
y = ctext(y, "PARK SLOPE MUSIC THERAPY", f_head, ink); y += 40
y = ctext(y, "Neurologic Music Therapy", f_title, ink); y += 12
y = ctext(y, "Package", f_title, ink); y += 70

# divider
d.line([260, y, W-260, y], fill=gold, width=2); y += 55

y = ctext(y, "6 sessions", f_sess, maroon); y += 70
y = ctext(y, "$420", f_price, maroon); y += 80

y = ctext(y, "Individual 60-minute NMT sessions", f_body, ink); y += 55
y = ctext(y, "Park Slope studio  \u00b7  Brooklyn, NY", f_body, ink); y += 90

d.line([260, y, W-260, y], fill=gold, width=2); y += 45
y = ctext(y, "Nicole King, MT-BC  \u00b7  parkslopemt.example.com", f_small, (95,90,82))

img.save("/root/workspace/deliverables/package_card_corrected.png", "PNG")
print("card written")

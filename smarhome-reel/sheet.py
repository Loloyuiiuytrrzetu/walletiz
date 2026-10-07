# Builds the contact sheet: one frame per beat, rows = 9:16, 1:1, 16:9
from PIL import Image, ImageDraw, ImageFont
import glob
labels = ["1 · Hook  2.45s", "2 · Produit  5.4s", "3a · Dimension  7.95s", "3b · Plans  12.0s", "3c · Assistant  14.75s", "4 · Chiffre  16.9s", "5 · Logo + CTA  19.4s"]
font = ImageFont.truetype(glob.glob('/usr/share/fonts/**/DejaVuSans-Bold.ttf', recursive=True)[0], 22)
rows = [('916', 520), ('11', 300), ('169', 230)]
cw = 300; pad = 14
heights = []
for fmt, _ in rows:
    im = Image.open(f'out/sheet/{fmt}-0.png'); heights.append(int(cw * im.height / im.width))
H = sum(heights) + pad * (len(rows) + 1) + 40 * len(rows) + 60
sheet = Image.new('RGB', (7 * cw + 8 * pad, H), (24, 22, 20)); d = ImageDraw.Draw(sheet)
d.text((pad, 16), "Smar Home — 20s reel · contact sheet (1 frame / beat)", fill=(243, 186, 37), font=font)
y = 60
for (fmt, _), h in zip(rows, heights):
    d.text((pad, y), {'916': '9:16 — 1080×1920', '11': '1:1 — 1080×1080', '169': '16:9 — 1920×1080'}[fmt], fill=(249, 244, 238), font=font); y += 36
    for i in range(7):
        im = Image.open(f'out/sheet/{fmt}-{i}.png').resize((cw, h), Image.LANCZOS)
        x = pad + i * (cw + pad); sheet.paste(im, (x, y))
        if fmt == '916': d.text((x + 6, y + h - 30), labels[i], fill=(243, 186, 37), font=ImageFont.truetype(font.path, 17))
    y += h + pad
sheet.save('out/contact-sheet.png'); print(sheet.size)

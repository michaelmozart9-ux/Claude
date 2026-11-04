# contact sheet: python3 tools/sheet.py <dir_with_jpgs> <out.jpg> [cols] [every]
import sys, os
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 5; every = int(sys.argv[4]) if len(sys.argv) > 4 else 1
fs = sorted(f for f in os.listdir(d) if f.endswith(".jpg"))[::every]
tw, th = 216, 384
rows = (len(fs) + cols - 1) // cols
S = Image.new("RGB", (cols * tw, rows * (th + 22)), (40, 40, 40)); D = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    im = Image.open(os.path.join(d, f)).resize((tw, th)); x, y = (i % cols) * tw, (i // cols) * (th + 22)
    S.paste(im, (x, y + 22)); D.text((x + 4, y + 4), f.replace(".jpg", ""), fill=(255, 255, 0))
S.save(out, quality=85); print(out, len(fs))

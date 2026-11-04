# flags caption lines that will wrap (Inter 900 measured with PIL)
import json, re, glob, os, sys
from PIL import ImageFont
F = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
sizes = {"cap": 98, "cap s": 84, "cap xs": 70, "cap xl": 116, "sub": 56, "sub s": 46}
width = {"cap": 980, "sub": 940}
bad = 0
for tj in sorted(glob.glob("videos/*/timing.json")):
    if "_smoke" in tj: continue
    T = json.load(open(tj))
    for e in T["els"]:
        cls = e.get("cls", "")
        if cls not in sizes: continue
        fnt = ImageFont.truetype(F, sizes[cls])
        W = width["cap" if cls.startswith("cap") else "sub"]
        for line in re.split(r"<br\s*/?>", e["html"]):
            txt = re.sub(r"<[^>]+>", "", line).replace("&middot;", "·")
            w = fnt.getlength(txt) * (0.98 if cls.startswith("cap") else 0.93)
            if w > W:
                bad += 1
                print(f"{os.path.basename(os.path.dirname(tj))}: [{cls}] {w:.0f}px > {W}: {txt}")
print("lines too wide:", bad)

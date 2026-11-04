"""Caption fitting: keep every caption to <= 2 lines that fit 980px (Inter 900), splitting/shrinking as needed."""
import re
from PIL import ImageFont
FONT = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
CAP = [("cap xl", 116), ("cap", 98), ("cap s", 84), ("cap xs", 70)]
SUB = [("sub", 56), ("sub s", 46)]
_f = {}


def _font(sz):
    if sz not in _f:
        _f[sz] = ImageFont.truetype(FONT, sz)
    return _f[sz]


def _plain(s):
    return re.sub(r"<[^>]+>", "", s).replace("&middot;", "·").replace("&amp;", "&")


def width(line, sz, k=0.98):
    return _font(sz).getlength(_plain(line)) * k


def _cands(html):
    """split candidates: (left_html, right_html, char_before_space)"""
    out = []
    open_tag = None
    i = 0
    while i < len(html):
        if html[i] == "<":
            j = html.index(">", i)
            tag = html[i + 1:j]
            if tag.startswith("/"):
                open_tag = None
            elif tag in ("g", "r", "i", "m"):
                open_tag = tag
            i = j + 1
            continue
        if html[i] == " ":
            left, right = html[:i], html[i + 1:]
            if open_tag:
                left += f"</{open_tag}>"
                right = f"<{open_tag}>" + right
            prev = _plain(html[:i]).rstrip()[-1:] if _plain(html[:i]).strip() else ""
            out.append((left, right, prev))
        i += 1
    return out


def split2(html, sz, W, punct_only=False):
    best = None
    for a, b, prev in _cands(html):
        p = prev in ",.:?!…"
        if punct_only and not p:
            continue
        wa, wb = width(a, sz), width(b, sz)
        if wa <= W and wb <= W:
            score = abs(wa - wb) + (0 if p else 500)
            if best is None or score < best[0]:
                best = (score, a + "<br>" + b)
    return best[1] if best else None


def fit(html, cls):
    fam = CAP if cls.startswith("cap") else SUB if cls.startswith("sub") else None
    if not fam:
        return html, cls
    W = 980 if cls.startswith("cap") else 940
    names = [c for c, _ in fam]
    start = names.index(cls) if cls in names else 0
    lines = re.split(r"<br\s*/?>", html)
    flat = " ".join(lines)
    for c, sz in fam[start:]:
        if len(lines) <= 2 and all(width(l, sz) <= W for l in lines):
            return html, c
        s2 = split2(flat, sz, W, punct_only=True) if len(lines) == 1 else None
        if s2:
            return s2, c
    for c, sz in fam[start:]:
        s2 = split2(flat, sz, W)
        if s2:
            return s2, c
    print("  !! caption too long:", _plain(html))
    return html, fam[-1][0]

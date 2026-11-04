"""Authoring helper: a Reel collects notes, camera, captions, fx and phone steps, then writes audio.wav + timing.json."""
import os, sys, json, re, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pianolib import *
import sfx as SFX
from fit import fit

LO, HI, WW = 33, 88, 0.30
_BLK = {1, 3, 6, 8, 10}


def is_black(m):
    return (m % 12) in _BLK


def white_idx(m):
    return sum(1 for k in range(LO, m) if not is_black(k))


C4X = white_idx(60)
_BOFF = {1: -0.06, 3: 0.06, 6: -0.08, 8: 0, 10: 0.08}


def key_x(m):
    m = max(LO, min(HI, m))
    if not is_black(m):
        return (white_idx(m) - C4X) * WW
    return (white_idx(m - 1) - C4X) * WW + WW / 2 + _BOFF[m % 12] * WW


def cam_for(lo, hi, zoom=1.0, lift=0.0, side=0.0):
    """Camera (p, l) framing MIDI range lo..hi with keyboard low in frame, notes falling above."""
    x0, x1 = key_x(lo) - WW * 1.2, key_x(hi) + WW * 1.2
    w = x1 - x0
    cx = (x0 + x1) / 2
    D = max(6.0, min(22.0, 2.55 * w)) / zoom
    p = [round(cx + side, 3), round(1.2 + 0.40 * D + lift, 3), round(0.9 + 0.86 * D, 3)]
    l = [round(cx, 3), round(0.62 + 0.23 * D + lift * 0.6, 3), -1.2]
    return p, l


class Reel:
    def __init__(self, name, dur, **opts):
        self.name, self.dur = name, dur
        self.dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos", name)
        os.makedirs(self.dir, exist_ok=True)
        self.notes, self.secs, self.cams, self.els, self.fx = [], [], [], [], []
        self.slams, self.cards, self.zones = [], [], []
        self.dims, self.hazes, self.kbk = [], [], []
        self.phone = None
        self.sfx = []
        self.beds = []
        self.extra_audio = []
        self.opts = opts
        self.sec_end = {}
        self.wet = opts.get("wet", 0.22)
        self.meta = {}

    # ---- music ----
    def play(self, seq, bpm, t0, sec="s", hand="R", vel=0.7, pedal=None, **kw):
        ns = place(seq, bpm, t0, sec=sec, hand=hand, vel=vel, pedal=pedal, **kw)
        self.notes += ns
        return ns

    def section(self, sid, t0, t1, cut=True):
        self.secs.append({"id": sid, "t0": round(t0, 3), "t1": round(t1, 3)})
        if cut:
            self.sec_end[sid] = t1

    # ---- camera ----
    def cam(self, t, p, l, e="io", r=None):
        k = {"t": round(t, 3), "p": p, "l": l, "e": e}
        if r is not None:
            k["r"] = [0, 0, r]
        self.cams.append(k)

    def frame(self, t, lo, hi, e="io", zoom=1.0, lift=0.0, side=0.0, hold=None):
        p, l = cam_for(lo, hi, zoom, lift, side)
        self.cam(t, p, l, e)
        if hold:
            self.cam(t + hold, p, l, "io")

    # ---- html ----
    def el(self, t0, t1, html="", cls="cap", y=140, style="", inn="pop", out="fade", **kw):
        if cls.startswith("cap") or cls.startswith("sub"):
            html, cls = fit(html, cls)
        e = {"t0": round(t0, 3), "t1": round(t1, 3), "html": html, "cls": cls, "y": y, "style": style, "in": inn, "out": out}
        e.update(kw)
        self.els.append(e)
        return e

    def cap(self, t0, t1, html, y=130, cls="cap", **kw):
        return self.el(t0, t1, html, cls, y, **kw)

    def sub(self, t0, t1, html, y=420, cls="sub", **kw):
        return self.el(t0, t1, html, cls, y, **kw)

    def chip(self, t0, t1, html, y=1000, kind="", **kw):
        return self.el(t0, t1, html, ("chip " + kind).strip(), y, **kw)

    def timer(self, t0, t1, n=3, y=820, tick=True):
        self.el(t0, t1, "", "timer", y, type="timer", n=n, inn="pop", out="pop")
        if tick:
            step = (t1 - t0) / n
            for k in range(n):
                self.s("tick", t0 + k * step, 0.05)

    def pips(self, t0, t1, n, k, y=1820, states=None):
        html = "".join(f'<span class="pip {(states[i] if states else ("on" if i == k else "done" if i < k else ""))}"></span>' for i in range(n))
        return self.el(t0, t1, html, "pips", y, inn="fade", out="none")

    def illus(self, t0, t1, y=1855, text="Illustration"):
        return self.el(t0, t1, text, "illus", y, inn="fade", out="fade")

    def lower_third(self, t0, t1=None):
        t1 = t1 or self.dur
        self.el(t0, t1, '<div class="pill">betweenlessons.org &middot; Day 1 free</div><div class="s2">I built it &middot; link in bio</div>', "lt", 1600, inn="up", out="none")
        self.s("pop", t0 + 0.05, 0.04, freq=900)

    # ---- fx ----
    def slam(self, t0, t1, text, col="gold", y=760, size=1.0, sound=True, **kw):
        self.slams.append(dict({"t0": round(t0, 3), "t1": round(t1, 3), "text": text, "col": col, "y": y, "size": size}, **kw))
        if sound:
            self.s("boom", t0 + 0.02, 0.09)
            self.s("whoosh", t0 - 0.2, 0.012)

    def confetti(self, t, y=760, x=540, n=220, sound=True):
        self.fx.append({"type": "confetti", "t": round(t, 3), "y": y, "x": x, "n": n})
        if sound:
            self.s("confetti", t + 0.02, 0.055)

    def shards(self, t, y=1100, n=150, sound=True):
        self.fx.append({"type": "shards", "t": round(t, 3), "y": y, "n": n})
        if sound:
            self.s("shatter", t, 0.05)

    def ring(self, t, y=760, col="#F2C46B", s=2.6):
        self.fx.append({"type": "ring", "t": round(t, 3), "y": y, "col": col, "s": s})

    def shake(self, t, a=0.16):
        self.fx.append({"type": "shake", "t": round(t, 3), "a": a})

    def flash(self, t, dur=0.35, a=0.4):
        self.fx.append({"type": "flash", "t": round(t, 3), "dur": dur, "a": a})

    def redflash(self, t, dur=0.5, a=0.7):
        self.fx.append({"type": "redflash", "t": round(t, 3), "dur": dur, "a": a})

    def explode(self, t0, t1):
        self.fx.append({"type": "explode", "t0": round(t0, 3), "t1": round(t1, 3)})

    def dim(self, t0, t1, v=1.0):
        self.dims.append({"t0": t0, "t1": t1, "v": v})

    def haze(self, t0, t1, v=1.0):
        self.hazes.append({"t0": t0, "t1": t1, "v": v})

    def kb(self, t, o, e="io"):
        self.kbk.append({"t": round(t, 3), "o": o, "e": e})

    def zone(self, t0, t1, lo, hi, col="#F2C46B", h=9):
        self.zones.append({"t0": t0, "t1": t1, "lo": P(lo), "hi": P(hi), "col": col, "h": h})

    def card(self, w, h, items, keys, space="world", bg=None, border=None, radius=0.12, px=220, bw=5):
        c = {"w": w, "h": h, "items": items, "keys": keys, "space": space, "radius": radius, "px": px, "bw": bw}
        if bg:
            c["bg"] = bg
        if border:
            c["border"] = border
        self.cards.append(c)
        return c

    # ---- audio ----
    def s(self, name, t, gain, **kw):
        self.sfx.append((name, t, gain, kw))

    def bed(self, t0, t1, bpm, chords, **kw):
        self.beds.append((t0, t1, bpm, chords, kw))

    def pad(self, t, notes, hold=1.6, vel=0.32):
        """soft hidden sustained chord to avoid dead air under talky moments"""
        return self.chord_hit(t, notes, hold=hold, vel=vel, sec="_pad", show=False)

    def chord_hit(self, t, notes, hold=1.5, vel=0.75, h="R", sec="s", show=True):
        ns = [{"m": P(n), "t": round(t, 4), "d": hold, "v": vel, "h": h, "sec": sec} for n in notes]
        if not show:
            for n in ns:
                n["hide"] = True
        self.notes += ns
        return ns

    # ---- phone / outro ----
    def phone_seq(self, t0, steps=(), taps=(), lift=None, rest=None, t1=None):
        self.phone = {"t0": round(t0, 3), "steps": list(steps), "taps": list(taps)}
        if lift is not None:
            self.phone["lift"] = lift
        if rest:
            self.phone["rest"] = rest
        if t1:
            self.phone["t1"] = t1
        self.s("whoosh", t0 + 0.05, 0.016)
        self.s("whoosh", t0 + 0.55, 0.01)

    def tap(self, t, at):
        self.phone["taps"].append({"t": round(t, 3), "at": at})
        self.s("tap", t, 0.05)
        self.s("pop", t + 0.04, 0.03, freq=1500)

    def outro(self, t0, lines=None, kind="today", bed=True, lt_after=3.0, dim=True, bed_from=None):
        """Standard soft product moment: captions + phone with the real Today screen + lower third."""
        lines = list(lines or ["So I built something that <g>tells you</g>.", "What to play. <g>How fast.</g> How long."])
        # merge an unfinished line with the next one so no caption is a fragment
        merged = []
        for ln in lines:
            if merged and not re.sub(r"<[^>]+>", "", merged[-1]).rstrip().endswith((".", "?", "!", ":", "…", "👇")):
                merged[-1] = merged[-1] + "<br>" + ln
            else:
                merged.append(ln)
        lines = merged
        self.dur = round(t0 + 6.5, 2) if self.opts.get("fit_end") else round(max(self.dur, t0 + 6.4), 2)
        D = self.dur
        if dim:
            self.dim(t0 - 0.1, D + 1, 0.82)
        n = len(lines)
        span = min(lt_after, D - t0 - 1.0)
        for i, ln in enumerate(lines):
            a = t0 + i * span / n + (0.16 if i else 0)
            b = t0 + (i + 1) * span / n if i < n - 1 else D + 0.5
            self.cap(a, b - 0.02 if i < n - 1 else D + 1, ln, y=110, cls="cap s", out="fade" if i < n - 1 else "none")
            self.s("whoosh", a - 0.05, 0.01)
        tp = t0 + 0.15
        if kind == "today":
            steps = [{"t": 0, "set": {"screen": "today", "scroll": 0}}]
            self.phone_seq(tp, steps=steps, lift=t0 + span)
            self.tap(tp + 1.25, "metro")
            self.phone["steps"].append({"t": tp + 1.3, "set": {"metroT0": tp + 1.3, "bpm": 36}})
            for k in range(int((D - tp - 1.3) * 36 / 60) + 1):
                self.s("tick", tp + 1.3 + k * 60 / 36, 0.035, freq=1600 if k % 4 == 0 else 1200)
            self.tap(tp + 2.1, "seg.1.2")
            self.phone["steps"].append({"t": tp + 2.15, "set": {"hl": 1, "countdown": [tp + 2.15, 1200], "speedup": 1}})
        elif kind == "checkin":
            self.phone_seq(tp, steps=[{"t": 0, "set": {"screen": "today", "phase": "checkin", "scroll": "end"}}], lift=t0 + span)
            self.tap(tp + 1.3, "rate.easy")
            self.phone["steps"].append({"t": tp + 1.35, "set": {"rating": "easy"}})
            self.tap(tp + 2.0, "save")
            self.phone["steps"].append({"t": tp + 2.2, "set": {"screen": "saved", "change": 5}})
            self.s("ding", tp + 2.25, 0.03)
        elif kind == "form":
            comp, title = self.meta.get("form", ("Debussy", "Clair de Lune"))
            st = [{"t": 0, "set": {"screen": "form", "step": 1, "composer": "", "title": "", "caret": "composer"}}]
            tt = tp + 1.0
            for i in range(1, len(comp) + 1):
                st.append({"t": round(tt, 3), "set": {"composer": comp[:i]}}); tt += 0.055
            st.append({"t": round(tt + 0.1, 3), "set": {"caret": "title"}}); tt += 0.2
            for i in range(1, len(title) + 1):
                st.append({"t": round(tt, 3), "set": {"title": title[:i]}}); tt += 0.05
            self.s("typing", tp + 1.0, 0.03, d=tt - tp - 1.0)
            self.phone_seq(tp, steps=st, lift=t0 + span)
            self.tap(tt + 0.25, "next")
            self.phone["steps"].append({"t": round(tt + 0.45, 3), "set": {"screen": "today", "scroll": 0, "caret": None}})
            self.s("ding", tt + 0.5, 0.025)
        elif kind == "week":
            self.phone_seq(tp, steps=[{"t": 0, "set": {"screen": "week", "done": 2}}], lift=t0 + span)
            self.tap(tp + 1.5, "rows.2")
            self.phone["steps"].append({"t": round(tp + 1.75, 3), "set": {"screen": "today", "scroll": 0, "session": 3}})
        elif kind == "grade":
            g = self.meta.get("grade", 3)
            self.phone_seq(tp, steps=[{"t": 0, "set": {"screen": "form", "step": 0, "grade": None}}], lift=t0 + span)
            self.tap(tp + 1.2, f"grades.{g - 1}")
            self.phone["steps"].append({"t": round(tp + 1.3, 3), "set": {"grade": g}})
            self.tap(tp + 2.0, "next")
            self.phone["steps"].append({"t": round(tp + 2.2, 3), "set": {"screen": "form", "step": 1, "composer": "", "title": "", "caret": "composer"}})
        if bed:
            self.bed((bed_from if bed_from is not None else t0) - 0.05, D, 96, [("A2", ["C4", "E4", "A4"]), ("F2", ["C4", "F4", "A4"]), ("C3", ["E4", "G4", "C5"]), ("G2", ["D4", "G4", "B4"])], vel=0.27, kgain=0.08, hgain=0.02)
        self.lower_third(t0 + span)

    # ---- build ----
    def build(self):
        D = self.dur
        tr = render(self.notes, D, self.sec_end)
        mix = reverb(tr, wet=self.wet)
        for (a, b, bpm, chords, kw) in self.beds:
            bt = track(D)
            kw = dict(kw)
            mg = kw.pop("mixgain", 0.7)
            SFX.bed(bt, a, b, bpm, chords, **kw)
            mix += reverb(bt, 0.15) * mg
        for fn in self.extra_audio:
            fn(mix)
        for (name, t, gain, kw) in self.sfx:
            f = getattr(SFX, name)
            add(mix, f(**kw), t, gain)
        master(mix, D, os.path.join(self.dir, "audio.wav"))
        out = {"duration": D, "fps": 30, "notes": [{k: v for k, v in n.items()} for n in self.notes], "secs": self.secs, "cam": sorted(self.cams, key=lambda c: c["t"]),
               "els": self.els, "fx": self.fx, "slams": self.slams, "cards": self.cards, "zones": self.zones, "dim": self.dims, "haze": self.hazes, "phone": self.phone, "meta": self.meta}
        if self.kbk:
            out["kb"] = sorted(self.kbk, key=lambda c: c["t"])
        for k in ("speed", "tilt", "bg", "fog", "exposure", "glow", "drift", "hazeBlur", "fov"):
            if k in self.opts:
                out[k] = self.opts[k]
        json.dump(out, open(os.path.join(self.dir, "timing.json"), "w"))
        print(self.name, "built", len(self.notes), "notes", D, "s")

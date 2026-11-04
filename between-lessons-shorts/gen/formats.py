"""Video formats -> audio.wav + timing.json"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from plib import *
from music import *

HL = lambda s: f"<span class='hl'>{s}</span>"
BAD = lambda s: f"<span class='bad'>{s}</span>"
EM = lambda s: f"<span class='em'>{s}</span>"

class Vid:
    def __init__(self, seed=7):
        self.notes, self.secs, self.sfx = [], [], []
        self.ev = {"shake": [], "flash": [], "red": [], "confetti": [], "explode": [], "timers": [], "slams": []}
        self.rng = np.random.default_rng(seed); self.ui = {}; self.snow = False
    def sec(self, id, start, end, cam="wide", **kw):
        d = dict(id=id, start=round(start, 3), end=round(end, 3), cam=cam); d.update({k: v for k, v in kw.items() if v is not None}); self.secs.append(d); return d
    def put(self, ns, bpm, t0, sec, spans=None, stuck=False, detach=False, win=None, shift=0.0, final_beat=None, jitter=.006, vel=1.0):
        q = 60 / bpm; out = []
        for m, b, d, h, v in ns:
            t = t0 + b * q + self.rng.normal(0, jitter); dur = d * q * (.75 if detach else 1)
            rel = t + dur + .03
            if spans:
                e = next((se for ss, se in spans if ss - 1e-6 <= b < se - 1e-6), None)
                if e is not None: rel = max(t + dur, t0 + e * q + .02)
            if stuck: rel = 9999.0
            if final_beat is not None and b >= final_beat - 1e-6: rel = t + dur
            if win and not (win[0] <= t < win[1]): continue
            out.append({"m": int(m), "t": round(t - shift, 4), "d": round(dur, 4), "rel": round(min(rel, 9999.0) - shift, 4), "h": h,
                        "v": round(float(np.clip(v * vel + self.rng.normal(0, .03), .15, 1)), 3), "sec": sec})
        self.notes += out; return out
    def fx(self, sig, t, g): self.sfx.append((sig, t, g))
    def cut(self, t, flash=True):
        self.fx(whoosh(), t - .3, .012)
        if flash: self.ev["flash"].append(round(t, 3))
    def save(self, out, dur):
        os.makedirs(out, exist_ok=True)
        ends = {s["id"]: s["end"] for s in self.secs}
        mix = render(self.notes, dur, ends)
        mix = reverb(mix, .22)
        for sig, t, g in self.sfx: add(mix, sig, t, g)
        master(mix, dur, f"{out}/audio.wav")
        json.dump({"duration": round(dur, 3), "fps": 30, "res": 720, "snow": self.snow, "secs": self.secs, "notes": self.notes, "ui": self.ui, "ev": self.ev}, open(f"{out}/timing.json", "w"))
        return dur

def spans_of(p, extra_end=None):
    sp = [(cb, cb + d) for cb, c, d in p["ch"]]
    if extra_end: sp.append(extra_end)
    return sp

def soft_end(v, p, t, sec, bpm=60):
    tp, iv = tonic(p); low = near(tp, 48)
    ns = [(low - 12, 0, 6, "L", .32), (low, .08, 6, "L", .28), (low + iv[1], .16, 6, "R", .26), (low + 7, .24, 6, "R", .26), (low + 12, .32, 6, "R", .24)]
    v.put(ns, bpm, t, sec, final_beat=0); v.fx(ding(1046.5), t + .1, .03)

def end_ui(v, endq, end2, t_end, lt_delay=1.45):
    v.ui.update(endq=endq, end2=end2, endq_t=round(t_end, 3), lt=round(t_end + lt_delay, 3))

def phone_ui(v, endq, t):
    v.ui.update(endq=endq, end2="", endq_t=round(t + .25, 3), lt=round(t + 1.6, 3), phone=round(t, 3))

def descs(p):
    k = p.get("lh5"); d5 = {"gym": "Melody + floating chords", "fe": "Melody + broken chords", "alb8": "Melody + fast broken chords"}.get(k, "Broken chords + harmony")
    if p.get("unison"): d5 = "Octaves"
    if p.get("dyad"): d5 = "Two-note chords + bass"
    med = sorted(d for _, _, d in p["mel"])[len(p["mel"]) // 2]
    d8 = "Running 16ths + stride bass" if med >= 1 else "Octaves + full left hand"
    if p.get("lh8") == "sweep": d8 = ("Running 16ths" if med >= 1 else "Octaves") + " + sweeping bass"
    return "Melody + one bass note", d5, d8

def arr(p, level, cut=None):
    q = truncate(p, cut) if cut else p
    if level == 1: ns, e = g1(q); return ns, e, None, spans_of(q)
    if level == 5: ns, e = g5(q); return ns, e, None, spans_of(q)
    ns, e, cb = g8(q); return ns, e, cb, spans_of(q, (cb, cb + 6) if cb else None)

# ====================================================================== formats
def grade_cmp(p, out, hook=None):
    v = Vid(); v.snow = p.get("snow", False); q = truncate(p, p.get("gcut"))
    b1, b5, b8 = q["bpm"]; d1, d5, d8 = descs(q)
    n8, e8, cb, sp8 = arr(q, 8)
    qq = 60 / b8; H = max(0, cb * qq - 1.1)
    v.put(n8, b8, 0, "hook", spans=sp8, final_beat=cb, win=(H, H + 2.0), shift=H)
    v.sec("hook", 0, 2.0, cam="hook")
    t = 2.0; chord_t = None
    for gid, lvl, bpm, desc, cam in [("g1", 1, b1, d1, "wide"), ("g5", 5, b5, d5, "push"), ("g8", 8, b8, d8, "close")]:
        ns, e, c, sp = arr(q, lvl); t0 = t + .25
        v.put(ns, bpm, t0, gid, spans=sp if lvl == 8 else None, final_beat=c)
        if lvl == 8: chord_t = t0 + c * 60 / bpm; end = chord_t + 5.6
        else: end = t0 + e * 60 / bpm + .3
        v.sec(gid, t, end, cam=cam, card=dict(lab="GRADE", big=str(lvl), meter=lvl, desc=desc, small=f"{bpm} BPM"))
        v.cut(t); t = end
    v.ev["shake"].append(round(chord_t, 3)); v.ev["flash"].append(round(chord_t, 3))
    v.fx(boom(), chord_t, .08); v.fx(ding(1046.5), chord_t + 2.6, .035)
    v.ui.update(hook=hook or f"{q['short']}.<br>Grade 1 vs {HL('Grade 8')}", hook_end=2.0)
    end_ui(v, f"Want to play it<br>like {HL('Grade 8?')}", f"I built a 6-week plan for<br>{HL('your grade &amp; your pieces.')}", chord_t + .95)
    return v.save(out, t)

def level5(p, out):
    v = Vid(); v.snow = p.get("snow", False); q = truncate(p, p.get("cut"))
    b1, b5, b8 = q["bpm"]
    mel_only = [n for n in g1(q)[0] if n[3] == "R"]
    n8e, e8, cb, sp8 = arr(q, 8)
    n8, e8n, _ = g8(q, with_end=False)
    lv = [("L1", mel_only, mel_end(q), None, None, round(b1 * .9), "Melody only", "wide"),
          ("L2", g1(q)[0], mel_end(q), None, None, b1, "Melody + bass", "left"),
          ("L3", g5(q)[0], mel_end(q), None, None, b5, "Broken chords", "push"),
          ("L4", n8, e8n, spans_of(q), None, b8, "Full texture", "right"),
          ("L5", n8e, e8, sp8, cb, round(b8 * 1.06), "Show-off mode", "close")]
    bL5 = lv[-1][5]; qq = 60 / bL5; H = max(0, cb * qq - 1.1)
    v.put(n8e, bL5, 0, "hook", spans=sp8, final_beat=cb, win=(H, H + 2.0), shift=H); v.sec("hook", 0, 2.0, cam="hook")
    t = 2.0
    for i, (sid, ns, e, sp, c, bpm, desc, cam) in enumerate(lv):
        t0 = t + .2; v.put(ns, bpm, t0, sid, spans=sp, final_beat=c)
        if c: chord_t = t0 + c * 60 / bpm; end = chord_t + 5.6
        else: end = t0 + e * 60 / bpm + .25
        v.sec(sid, t, end, cam=cam, card=dict(lab="LEVEL", big=str(i + 1), meter=[1, 3, 5, 7, 8][i], desc=desc, small=f"{bpm} BPM"))
        v.cut(t); t = end
    v.ev["shake"].append(round(chord_t, 3)); v.fx(boom(), chord_t, .08); v.fx(ding(1046.5), chord_t + 2.6, .035)
    v.ui.update(hook=f"5 levels of<br>{HL(q['short'])}", hook_end=2.0)
    end_ui(v, f"Which level<br>are {HL('you?')}", f"Get a 6-week plan<br>for {HL('your grade.')}", chord_t + .95)
    return v.save(out, t)

def snippet(p, level=5, bars=None):
    """notes, spans, bpm for a short recognisable snippet"""
    if p.get("texture"):
        ns, sp, e = texture(p, 5, bars); return ns, sp, p["bpm"][1], e
    q = truncate(p, p.get("cut"))
    ns, e, c, sp = arr(q, level)
    return ns, sp, q["bpm"][{1: 0, 5: 1, 8: 2}[level]], e

def quiz(rounds, out, hook, kind, endq, end2, snow=False):
    """rounds: list of dict(p, level, text, sub)"""
    v = Vid(); v.snow = snow; t = 0.0; cams = ["push", "left", "right"]
    for i, r in enumerate(rounds):
        p = r["p"]; ns, sp, bpm, e = snippet(p, r.get("level", 5), r.get("bars"))
        S = r.get("len", 3.9); t0 = t + .12
        v.put(ns, bpm, t0, f"r{i}", spans=sp, win=(t0 - .01, t + S))
        cap = f"Round {i + 1} of 3"; sub = "Name the song" if kind == "song" else "What grade is this?"
        v.sec(f"r{i}", t, t + S, cam=cams[i], cap=cap, sub=sub)
        if i: v.cut(t)
        ts = t + S; v.sec(f"t{i}", ts, ts + 3.0, cam="far", cap=cap, sub=sub)
        v.ev["timers"].append([round(ts, 3), round(ts + 3.0, 3)])
        for k in range(3): v.fx(click(k == 0), ts + k, .03); v.fx(tap(), ts + k + .5, .02)
        tsl = ts + 3.0; L = 1.6
        ch, cb = ending(p, 72, -2.0)
        chord = [n for n in ch if n[1] >= cb - 1e-6]
        v.put([(m, b - cb, d, h, vv) for m, b, d, h, vv in chord], 90, tsl, f"s{i}", final_beat=-99)
        v.sec(f"s{i}", tsl, tsl + L, cam="low")
        v.ev["slams"].append(dict(t=round(tsl, 3), end=round(tsl + L, 3), text=r["text"], sub=r.get("sub", "")))
        v.ev["confetti"].append(round(tsl, 3)); v.ev["flash"].append(round(tsl, 3)); v.ev["shake"].append(round(tsl, 3))
        v.fx(ding(1567.98), tsl, .04); v.fx(kick(), tsl, .06)
        t = tsl + L
    last = rounds[-1]["p"]; v.secs[-1]["end"] = round(t + 5.4, 3)
    soft_end(v, last, t + .2, v.secs[-1]["id"])
    v.ui.update(hook=hook, hook_end=2.0)
    end_ui(v, endq, end2, t + .1)
    return v.save(out, t + 5.4)

def guess_song(ps, out, snow=False):
    rounds = [dict(p=p, level=5, text=p["short"], sub=p["composer"]) for p in ps]
    return quiz(rounds, out, f"Guess the song<br>in {HL('3 seconds')}", "song", f"How many<br>did {HL('you get?')}", f"Want to learn one?<br>Get a {HL('6-week plan.')}", snow)

def guess_grade(p, order, out):
    d = dict(zip((1, 5, 8), descs(p)))
    rounds = [dict(p=p, level=g, text=f"Grade {g}", sub=d[g]) for g in order]
    return quiz(rounds, out, f"Guess the grade:<br>{HL(p['short'])}", "grade", f"Which grade<br>are {HL('you?')}", f"Get a 6-week plan<br>for {HL('your grade.')}", p.get("snow", False))

def metronome(v, t0, bpm, beats):
    q = 60 / bpm
    for k in range(int(beats)): v.fx(click(k % 4 == 0), t0 + k * q, .022)

def practice_xv(p, cfg, out, phone=False):
    """cfg: level, x0 (attempt start beat), hx (crash beat), h0,h1 (loop passage), r1 (run end beat)"""
    v = Vid(); v.snow = p.get("snow", False); q = truncate(p, cfg.get("cut"))
    lvl = cfg.get("level", 5); ns, e, cb, sp = arr(q, lvl); bpm = q["bpm"][{1: 0, 5: 1, 8: 2}[lvl]]; qb = 60 / bpm
    x0, hx, h0, h1 = cfg["x0"], cfg["hx"], cfg["h0"], cfg["h1"]
    target = [n for n in ns if abs(n[1] - hx) < 1e-6 and n[3] == "R"]
    tm = max(n[0] for n in target) if target else 72
    def attempt(t, sid, win=None, shift=0.0):
        t0 = t + .2 - x0 * qb
        pre = [n for n in ns if x0 - 1e-6 <= n[1] < hx - 1e-6]
        v.put(pre, bpm, t0, sid, spans=sp if lvl == 8 else None, win=win, shift=shift)
        crash = t0 + hx * qb
        v.put(fit([(tm - 1, hx, .6, "X", .8), (tm + 1, hx, .6, "X", .75), (tm + 2, hx + .02, .6, "X", .7)]), bpm, t0, sid, win=win, shift=shift, jitter=0)
        return crash
    # hook: last 1.4s into the crash
    c = attempt(0, "hook"); H = c - 1.4
    v.notes = [dict(n, t=round(n["t"] - H, 4), rel=round(n["rel"] - H, 4)) for n in v.notes if n["t"] >= H]
    v.sec("hook", 0, 2.1, cam="hook"); hc = 1.4
    v.fx(buzz(), hc, .045); v.ev["shake"].append(round(hc, 3)); v.ev["red"].append(round(hc, 3))
    t = 2.1
    for i, cam in enumerate(["wide", "left", "right"]):
        c = attempt(t, f"a{i}"); end = c + .8
        v.sec(f"a{i}", t, end, cam=cam, cap=f"{EM('❌')} From the top", tag=["DAY 1", "DAY 2", "DAY 3 · SAME BAR"][i])
        v.fx(buzz(), c, .045); v.ev["shake"].append(round(c, 3)); v.ev["red"].append(round(c, 3)); v.cut(t, flash=False); t = end
    loop = [n for n in ns if h0 - 1e-6 <= n[1] < h1 - 1e-6]
    for i, (pct, cam, desc) in enumerate([(60, "push", "Slow and clean"), (80, "close", "A bit faster"), (100, "low", "Full speed")]):
        bp = round(bpm * pct / 100); t0 = t + .35 - h0 * 60 / bp
        v.put(loop, bp, t0, f"l{i}", spans=sp if lvl == 8 else None)
        metronome(v, t + .35, bp, h1 - h0)
        end = t + .35 + (h1 - h0) * 60 / bp + .35
        v.sec(f"l{i}", t, end, cam=cam, card=dict(lab="✅ LOOP JUST THIS BAR", big=f"{pct}%", meter=[4, 6, 8][i], desc=desc, small=f"{bp} BPM"))
        v.cut(t); t = end
    # clean run
    r1 = cfg.get("r1", e); t0 = t + .2 - x0 * qb
    run = [n for n in ns if x0 - 1e-6 <= n[1] < r1 + 1e-6]
    v.put(run, bpm, t0, "run", spans=sp if lvl == 8 else None, final_beat=cb)
    passed = t0 + hx * qb; v.ev["confetti"].append(round(passed + .1, 3)); v.fx(ding(1567.98), passed + .05, .035)
    endrun = t0 + min(r1, e) * qb + .4
    v.sec("run", t, endrun + 5.6, cam="wide", cap=f"{EM('✅')} Same bar. Clean.")
    v.cut(t)
    if phone: phone_ui(v, f"Every session has<br>a {HL('tempo target.')}", endrun)
    else: end_ui(v, f"Stop starting<br>from {HL('the top.')}", f"My plans give every session<br>a {HL('tempo target.')}", endrun)
    soft_end(v, p, endrun + .3, "run")
    v.ui.update(hook=f"Why you keep<br>missing {BAD('this bar')}", hook_end=2.1)
    return v.save(out, endrun + 5.6)

def tempo_ladder(p, cfg, out):
    v = Vid(); v.snow = p.get("snow", False); q = truncate(p, cfg.get("cut"))
    lvl = cfg.get("level", 5); ns, e, cb, sp = arr(q, lvl); bpm = q["bpm"][{1: 0, 5: 1, 8: 2}[lvl]]
    h0, h1 = cfg["h0"], cfg["h1"]; loop = [n for n in ns if h0 - 1e-6 <= n[1] < h1 - 1e-6]
    usp = sp if lvl == 8 else None
    t0 = .1 - h0 * 60 / bpm; v.put(loop, bpm, t0, "hook", spans=usp)
    hl = .1 + (h1 - h0) * 60 / bpm + .25; hl = max(hl, 2.0)
    v.sec("hook", 0, hl, cam="hook")
    t = hl
    for i, (pct, cam, desc, reps) in enumerate([(40, "push", "Every note clean", 1), (60, "left", "Still clean", 1), (80, "right", "Almost there", 1), (100, "close", "Full speed", 2)]):
        bp = round(bpm * pct / 100); L = (h1 - h0) * 60 / bp
        for r in range(reps): v.put(loop, bp, t + .3 + r * L - h0 * 60 / bp, f"p{i}", spans=usp)
        metronome(v, t + .3, bp, (h1 - h0) * reps)
        end = t + .3 + reps * L + .3
        v.sec(f"p{i}", t, end, cam=cam, card=dict(lab="TEMPO", big=f"{pct}%", meter=[3, 5, 6, 8][i], desc=desc, small=f"{bp} BPM"))
        v.cut(t); t = end
    v.ev["confetti"].append(round(t - .4, 3)); v.fx(ding(1567.98), t - .4, .03)
    v.secs[-1]["end"] = round(t + 6.2, 3); soft_end(v, p, t + .3, v.secs[-1]["id"])
    v.ui.update(hook=f"The {HL('hardest bar')}<br>of {q['short']}", hook_end=hl)
    phone_ui(v, f"Start slow.<br>Earn the {HL('tempo.')}", t)
    return v.save(out, t + 6.2)

def pedal_cmp(p, out, bars=None, win=6.6):
    v = Vid(); v.snow = p.get("snow", False)
    if p.get("texture"): ns, sp, e = texture(p, 5, bars); bpm = p["bpm"][1]
    else:
        q = truncate(p, p.get("cut")); ns, e = g5(q); sp = spans_of(q); bpm = q["bpm"][1]
    qb = 60 / bpm; L = min(e * qb + .4, win)
    v.put(ns, bpm, .1, "hook", spans=sp, win=(0, 2.2)); v.sec("hook", 0, 2.2, cam="hook")
    t = 2.2
    for i, (sid, big, desc, cam) in enumerate([("off", "OFF", "Dry and choppy", "wide"), ("on", "ON", "Changed with each chord", "push"), ("stuck", "TOO MUCH", "Everything blurs", "close")]):
        t0 = t + .2
        v.put(ns, bpm, t0, sid, spans=sp if sid == "on" else None, detach=sid == "off", stuck=sid == "stuck", win=(t0 - .01, t + L))
        v.sec(sid, t, t + L, cam=cam, card=dict(lab="PEDAL", big=big, desc=desc))
        v.cut(t)
        if sid == "stuck": v.ev["red"] += [round(t + 2.6, 3), round(t + 4.6, 3)]
        t += L
    v.secs[-1]["end"] = round(t + 5.6, 3)
    soft_end(v, p, t + .2, "stuck")
    v.ui.update(hook=f"No pedal vs pedal<br>vs {BAD('TOO MUCH')}", hook_end=2.2)
    end_ui(v, f"Change it with<br>{HL('every chord.')}", f"A 6-week plan for your<br>{HL('pieces, session by session.')}", t + .1)
    return v.save(out, t + 5.6)

def five_lh(p, out):
    v = Vid(); v.snow = p.get("snow", False); q = truncate(p, p.get("cut")); bpm = q["bpm"][1]
    up = up_of(q); mel = fit([(P(n) + up, b, d, "R", .72) for n, b, d in q["mel"]])
    kinds = [("block", "Block chords"), ("alberti" if q["bpb"] == 4 else "broken", "Broken chords"), ("waltz" if q["bpb"] == 3 else "stride", "Oom-pah"), ("sweep", "Arpeggios"), ("sweep16", "Rolling 16ths")]
    e = mel_end(q); qb = 60 / bpm; sp = spans_of(q)
    def lhn(k): return fit(lh_pattern(q, k, .48))
    v.put(mel + lhn("sweep16"), bpm, .1, "hook", spans=sp, win=(0, 2.0)); v.sec("hook", 0, 2.0, cam="hook")
    t = 2.0
    for i, (k, name) in enumerate(kinds):
        t0 = t + .2; v.put(mel + lhn(k), bpm, t0, f"h{i}", spans=sp if k.startswith("sweep") else None)
        end = t0 + e * qb + .2
        v.sec(f"h{i}", t, end, cam=["wide", "left", "push", "right", "close"][i], card=dict(lab="LEFT HAND", big=str(i + 1), meter=[1, 3, 4, 6, 8][i], desc=name))
        v.cut(t); t = end
    v.secs[-1]["end"] = round(t + 5.6, 3); soft_end(v, q, t + .1, v.secs[-1]["id"])
    v.ui.update(hook=f"Same melody.<br>{HL('5 left hands.')}", hook_end=2.0)
    end_ui(v, f"Which one is<br>{HL('your level?')}", f"Get a 6-week plan<br>for {HL('your grade.')}", t + .1)
    return v.save(out, t + 5.6)

def harder_than(items, out):
    """items: list of (piece, fact_html, bars)"""
    v = Vid(); t = 0.0
    for i, (p, fact, bars) in enumerate(items):
        ns, sp, bpm, e = snippet(p, 5, bars); S = 6.4; t0 = t + .12
        v.put(ns, bpm, t0, f"x{i}", spans=sp, win=(t0 - .01, t + S))
        v.sec(f"x{i}", t, t + S, cam=["push", "left", "right"][i], cap="Sounds hard…", sub=f"{p['name']} · {p['composer']}")
        if i: v.cut(t)
        ts = t + 3.4; v.ev["slams"].append(dict(t=round(ts, 3), end=round(t + S, 3), text=fact, sub="Easier than it sounds"))
        v.ev["flash"].append(round(ts, 3)); v.fx(ding(1318.5), ts, .03); v.fx(kick(), ts, .05)
        t += S
    v.secs[-1]["end"] = round(t + 5.6, 3); soft_end(v, items[-1][0], t + .1, v.secs[-1]["id"])
    v.ui.update(hook=f"Pieces that sound<br>{HL('harder')} than they are", hook_end=2.2)
    end_ui(v, f"Want to learn<br>{HL('one of these?')}", f"Get a 6-week plan,<br>{HL('session by session.')}", t + .1)
    return v.save(out, t + 5.6)

def one_mistake(p, out):
    v = Vid(); v.snow = p.get("snow", False); q = truncate(p, p.get("cut"))
    ns, e = g5(q); sp = spans_of(q); bpm = round(q["bpm"][0] * .92); qb = 60 / bpm
    v.put(ns, bpm, .1, "m1", spans=sp, vel=.8, win=(0, 7.2))
    v.sec("m1", 0, 7.2, cam="orbit", cap=f"Piano is my<br>{HL('therapy')}")
    # second pass, wrong note ~1.8s in
    t = 7.2; t0 = t + .1
    hit = min((n for n in ns if n[3] == "R" and n[1] * qb > 1.6), key=lambda n: n[1])
    pre = [n for n in ns if n[1] < hit[1] - 1e-6]
    v.put(pre, bpm, t0, "m2", spans=sp, vel=.8)
    crash = t0 + hit[1] * qb
    v.put([(hit[0] - 1, 0, .6, "X", .85), (hit[0] + 1, 0, .6, "X", .8), (hit[0] + 2, .02, .6, "X", .75)], bpm, crash, "m2", jitter=0)
    v.sec("m2", t, crash + 3.2, cam="wide", cap=f"Me after ONE<br>{BAD('wrong note:')}")
    v.fx(buzz(), crash, .05); v.fx(boom(), crash + .05, .16); v.fx(riser(), crash + 1.5, .035)
    v.ev["shake"] += [round(crash, 3), round(crash + .1, 3)]; v.ev["red"].append(round(crash, 3)); v.ev["flash"].append(round(crash + .05, 3))
    v.ev["explode"].append([round(crash + .05, 3), round(crash + 3.1, 3)])
    t = crash + 3.2
    v.put(ns, bpm, t + .1, "m3", spans=sp, vel=.75, win=(t, t + 5.2))
    v.sec("m3", t, t + 5.2, cam="push", cap=f"Bad session?<br>Tap {HL('Too hard.')}", sub="Next session’s tempo: −5%")
    v.cut(t)
    t += 5.2
    v.secs[-1]["end"] = round(t + 6.0, 3); soft_end(v, q, t + .2, "m3")
    v.ui.update(hook=f"Piano is my<br>{HL('therapy')}", hook_end=2.0)
    phone_ui(v, f"Practice that<br>{HL('adjusts to you.')}", t)
    return v.save(out, t + 6.0)

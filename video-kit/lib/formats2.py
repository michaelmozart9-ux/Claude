"""Custom formats: plan explainer, practice-method videos, parent/adult-targeted videos."""
from formats import *


def notes_window(seq, a, b, shift=True):
    out = [s for s in seq if a - 1e-6 <= s[1] < b - 1e-6]
    return at(out, -a) if shift else out


def recolor(seq, hand):
    return [tuple([s[0], s[1], s[2], hand] + list(s[4:5] if len(s) > 4 else [None])) for s in seq]


def scale_bpm(bpm, pct):
    return bpm * pct / 100.0


DB_BED = [("Db3", ["F3", "Ab3", "Db4"]), ("Bb2", ["F3", "Bb3", "Db4"]), ("Gb2", ["Gb3", "Bb3", "Db4"]), ("Ab2", ["Eb3", "Ab3", "C4"])]
C_BED = [("C3", ["E4", "G4", "C5"]), ("A2", ["E4", "A4", "C5"]), ("F2", ["F4", "A4", "C5"]), ("G2", ["D4", "G4", "B4"])]


# ============ F. "An AI planned 6 weeks of Clair de Lune" (real example-plan data) ============
WEEKS = [
    (1, 40, 50, "Mostly left hand alone", ["Opening theme:", "left-hand landmarks"], ["LH alone, no", "hesitation"]),
    (2, 45, 60, "Hands together", ["Opening theme,", "4 bars, then 8"], ["Hands together", "at 60%, no stops"]),
    (3, 50, 70, "Hands together", ["Full opening theme", "+ the transition"], ["70%, twice in a row,", "without losing place"]),
    (4, 40, 65, "New section: slower again", ["Middle section", "starts, left hand"], ["Middle section LH,", "steady pulse"]),
    (5, 40, 70, "Hands together", ["Middle section", "excerpt, together"], ["50%, left hand", "grounded"]),
    (6, 70, 80, "Hands together", ["Opening theme →", "middle excerpt"], ["75–80%, shaped,", "no stops"]),
]


def week_card(R, w, lo, hi, hands, focus, ms, keys):
    W, H = 2.3, 3.1
    items = [
        {"t": "text", "x": 0.2, "y": 0.38, "text": f"WEEK {w}", "size": 0.16, "weight": 800, "color": "#F2C46B", "ls": 6},
        {"t": "text", "x": 2.1, "y": 0.38, "text": "of 6", "size": 0.13, "weight": 700, "color": "rgba(255,255,255,.5)", "align": "right"},
        {"t": "text", "x": 0.2, "y": 0.98, "text": f"{lo}–{hi}%", "size": 0.41, "weight": 900, "color": "#FFFFFF"},
        {"t": "text", "x": 0.2, "y": 1.22, "text": "tempo target", "size": 0.12, "weight": 700, "color": "rgba(255,255,255,.55)"},
        {"t": "rect", "x": 0.2, "y": 1.36, "w": 1.9, "h": 0.12, "r": 0.06, "color": "rgba(255,255,255,.1)"},
        {"t": "rect", "x": 0.2 + 1.9 * lo / 100, "y": 1.36, "w": 1.9 * (hi - lo) / 100, "h": 0.12, "r": 0.06, "color": "#F2C46B"},
        {"t": "text", "x": 0.2, "y": 1.78, "text": hands, "size": 0.135, "weight": 800, "color": "#9AD2FF"},
        {"t": "text", "x": 0.2, "y": 2.06, "text": focus[0], "size": 0.13, "weight": 600, "color": "rgba(255,255,255,.85)"},
        {"t": "text", "x": 0.2, "y": 2.26, "text": focus[1], "size": 0.13, "weight": 600, "color": "rgba(255,255,255,.85)"},
        {"t": "rect", "x": 0.2, "y": 2.42, "w": 1.9, "h": 0.5, "r": 0.08, "color": "rgba(242,196,107,.12)", "stroke": "rgba(242,196,107,.5)", "lw": 3},
        {"t": "text", "x": 0.32, "y": 2.6, "text": "Milestone: " + ms[0], "size": 0.105, "weight": 700, "color": "#F2C46B"},
        {"t": "text", "x": 0.32, "y": 2.8, "text": ms[1], "size": 0.105, "weight": 700, "color": "#F2C46B"},
    ]
    return R.card(W, H, items, keys, space="cam", border="rgba(242,196,107,.55)", bg="rgb(22,18,14)")


def plan6(name="f1-ai-planned-6-weeks"):
    dur = 29.6
    R = Reel(name, dur, glow="rgba(224,168,75,0.30)", fit_end=True)
    R.kb(0, 0)
    R.cam(0, [0, 3, 10], [0, 3, -1])
    R.cap(0, 2.7, "An AI planned <g>6 weeks</g><br>of Clair de Lune.", y=120, cls="cap s")
    R.sub(0.3, 2.7, "Here's every week 👇", y=330)
    R.s("whoosh", 0.05, 0.016)
    t0 = 2.6
    step = 2.35
    for i, (w, lo, hi, hands, focus, ms) in enumerate(WEEKS):
        a = 0.12 + i * 0.07
        deck = [-0.05 + i * 0.03, -0.45 - i * 0.02, -9 + i * 0.05]
        front = [0, -0.25, -6.2]
        ta = t0 + i * step
        gone = [-3.2, -0.4 - i * 0.05, -10]
        keys = [{"t": 0, "p": [0, -6, -9], "r": [0, 0, 0], "s": 1, "o": 0},
                {"t": a, "p": [0, -6, -9], "r": [0, 0, 0], "o": 1},
                {"t": a + 0.6, "p": deck, "r": [0, 0, (i - 2.5) * 0.06], "e": "back", "o": 1},
                {"t": ta, "p": deck, "r": [0, 0, (i - 2.5) * 0.06], "o": 1},
                {"t": ta + 0.45, "p": front, "r": [0, 0, 0], "e": "back", "o": 1},
                {"t": ta + step - 0.15, "p": [front[0], front[1] + 0.04, front[2]], "r": [0, 0.04, 0], "o": 1},
                {"t": ta + step + 0.3, "p": gone, "r": [0, 0.9, 0.1], "o": 0}]
        week_card(R, w, lo, hi, hands, focus, ms, keys)
        R.s("whoosh", ta, 0.014)
        R.s("pop", ta + 0.35, 0.035, freq=900 + 80 * i)
        R.cap(ta, ta + step - 0.05, f"Week <g>{w}</g>", y=150, cls="cap s", inn="fade", out="none" if i < 5 else "fade")
        R.pips(ta, ta + step, 6, i, y=1840)
        if w == 4:
            R.chip(ta + 0.5, ta + step - 0.1, "New section → tempo drops 👀", y=1710, kind="sm")
    tc = t0 + 6 * step + 0.2
    R.cap(tc, tc + 2.8, "Tempo targets,<br>week by week", y=120, cls="cap s")
    for i, (w, lo, hi, *_r) in enumerate(WEEKS):
        x = 75 + i * 155
        html = f'<div class="wbar"><div class="col"><div class="r" style="bottom:{lo * 4.8:.0f}px;height:{(hi - lo) * 4.8:.0f}px"></div></div><div class="lab">W{w}</div><div class="pc">{lo}–{hi}%</div></div>'
        R.el(tc + 0.15 + i * 0.17, tc + 2.8, html, "", y=560, style=f"left:{x}px;width:140px;", inn="up")
        R.s("pop", tc + 0.15 + i * 0.17, 0.035, freq=700 + 120 * i)
    R.confetti(tc + 1.3, y=900, n=200)
    R.s("ding", tc + 1.3, 0.035)
    R.cap(tc + 3.0, tc + 4.3, "It also said Clair de Lune<br>is a <g>stretch</g> at Grade 6. Honest.", y=600, cls="cap xs", inn="pop")
    R.outro(tc + 4.4, ["What to play. <g>How fast.</g>", "How long. <g>Every session.</g>"], kind="today", bed=False)
    R.bed(0, dur, 72, DB_BED, vel=0.26, kgain=0.0, hgain=0.0, arp=True, mixgain=0.9)
    R.build()


# ============ G1. Stop starting from bar 1 (The Entertainer) ============
def bar_one(name="g1-stop-bar-one"):
    rh, lh, bpm = EN_RH, EN_LH, EN_BPM
    R = Reel(name, 30.4, fit_end=True)
    R.cap(0, 6.6, "Stop starting from<br><r>bar 1</r> every time ❌", y=120, cls="cap s")
    t = 0.15
    starts = [0, 8, 13]
    for k, st in enumerate(starts):
        seg_rh = notes_window(rh, st, 18)
        seg_lh = notes_window(lh, st, 18)
        ns, L = play_clip(R, seg_rh, seg_lh, bpm, t, f"try{k}", t1=t + (18 - st) * 60 / bpm + 0.5)
        tm = t + (18 - st) * 60 / bpm
        R.notes.append({"m": P("E5"), "t": round(tm, 3), "d": 0.3, "v": 0.85, "h": "X", "sec": f"try{k}"})
        R.notes.append({"m": P("C#5"), "t": round(tm + 0.02, 3), "d": 0.3, "v": 0.7, "h": "X", "sec": f"try{k}"})
        R.s("buzz", tm + 0.02, 0.045)
        R.redflash(tm, 0.35, 0.4)
        R.shake(tm, 0.08)
        lo, hi = rng(ns)
        R.frame(t, lo, hi, e="cut" if k else "io", zoom=1.1 + 0.08 * k)
        R.chip(t, tm + 0.45, f"Attempt {k + 1}", y=440, kind="white")
        if k:
            R.s("scratch", t - 0.25, 0.04)
        t = tm + 0.55
    R.el(t, t + 2.2, "Bar 1: played <r>3×</r><br>The hard bar: <r>0×</r> clean", "card red stat", y=640, inn="pop")
    R.pad(t, ["C3", "G3", "E4"], hold=2.2, vel=0.3)
    R.illus(t, t + 2.2)
    R.s("pop", t, 0.04)
    t += 2.3
    R.cap(t, t + 6.9, "Do this instead ✅<br><g>Loop the hard bar.</g>", y=120, cls="cap s")
    R.s("whoosh", t - 0.1, 0.014)
    hard_rh, hard_lh = notes_window(rh, 16, 33), notes_window(lh, 16, 33)
    hlo, hhi = P("B4"), P("E5")
    R.zone(t, t + 6.6, hlo, hhi)
    t += 0.4
    for k, pct in enumerate([65, 100]):
        b = scale_bpm(bpm, pct)
        ns, L = play_clip(R, hard_rh, hard_lh, b, t, f"loop{k}", t1=t + 17 * 60 / b + 0.2)
        L = 17 * 60 / b
        lo, hi = rng(ns)
        R.frame(t, lo, hi, zoom=1.25 - 0.06 * k)
        R.chip(t, t + L + 0.1, f"{pct}% tempo", y=440, kind=["blue", "solid"][k])
        if k:
            R.s("whoosh", t - 0.1, 0.01)
        t += L + 0.25
    R.cap(t, t + 4.6, "Then the whole thing.<br><g>Clean.</g>", y=120, cls="cap s")
    ns, L = play_clip(R, rh, lh, bpm, t, "full", t1=t + 35 * 60 / bpm + 0.3)
    L = 33 * 60 / bpm
    lo, hi = rng(ns)
    R.frame(t, lo, hi, zoom=1.0)
    R.frame(t + L, lo, hi, zoom=1.15, side=0.5)
    fin = t + L - 0.1
    R.confetti(fin, y=700, n=240)
    R.ring(fin, y=700)
    R.flash(fin, 0.3, 0.35)
    R.s("ding", fin, 0.04)
    R.chip(fin, fin + 1.3, "Clean ✅", y=560, kind="solid big")
    t = fin + 1.0
    R.cap(t, t + 1.5, "Which bar do <g>you</g><br>always restart from? 👇", y=600, cls="cap s", inn="slam")
    R.dim(t - 0.1, t + 1.5, 0.6)
    R.outro(t + 1.55, ["So I built something that", "picks the section <g>for</g> you.", "Which bar. Which hands. <g>What tempo.</g>"], kind="today", bed_from=t)
    R.build()


# ============ G2. Hands separate first (K545) ============
def hands_sep(name="g2-hands-separate"):
    rh, lh, bpm = K545_RH, K545_LH(), K545_BPM
    R = Reel(name, 30.2, fit_end=True)
    R.meta["form"] = ("Mozart", "Sonata K. 545")
    R.cap(0, 3.9, "Hands together<br>on <r>day 1</r>? ❌", y=120, cls="cap s")
    # messy attempt
    mrh = [s for s in cut(rh, 24)]
    ns = R.play(mrh, bpm * 0.9, 0.15, sec="mess", hand="R")
    ns += R.play(cut(lh, 24), bpm * 0.9, 0.15, sec="mess", hand="L", vel=0.5, human=0.025)
    for n in ns:
        if n["t"] > 1.3:
            n["t"] = round(n["t"] + 0.35, 3)
    R.notes += [{"m": P("A4"), "t": 1.0, "d": 0.3, "v": 0.85, "h": "X", "sec": "mess"}, {"m": P("F3"), "t": 2.25, "d": 0.3, "v": 0.8, "h": "X", "sec": "mess"}]
    R.section("mess", 0.1, 3.5)
    R.s("buzz", 1.02, 0.04)
    R.s("buzz", 2.27, 0.045)
    R.redflash(1.0, 0.3, 0.3)
    R.redflash(2.25, 0.35, 0.4)
    R.shake(2.25, 0.1)
    lo, hi = rng(ns)
    R.frame(0, lo, hi)
    t = 3.9
    steps = [("Left hand <i>alone</i>", cut(lh, 24), [], 80, "L"), ("Right hand <g>alone</g>", [], cut(rh, 24), 80, "R"),
             ("Together. <g>Slowly.</g>", cut(lh, 24), cut(rh, 24), 70, None), ("Together. <g>Full speed.</g>", lh, rh, 100, None)]
    R.s("whoosh", t - 0.1, 0.014)
    for k, (label, L_, R_, pct, only) in enumerate(steps):
        b = scale_bpm(bpm, pct)
        units = 24 if k < 3 else 32
        ns = R.play(R_, b, t, sec=f"h{k}", hand="R") + R.play(L_, b, t, sec=f"h{k}", hand="L", vel=0.5)
        L = units * 60 / b
        R.section(f"h{k}", t - 0.05, t + L + 0.3)
        lo, hi = rng(ns)
        R.frame(t, lo, hi, e="cut" if k else "io", zoom=1.15 if k < 2 else 1.0)
        R.cap(t, t + L + 0.25, ("Do this ✅<br>" if k == 0 else "") + label, y=120, cls="cap s", inn="fade" if k else "pop")
        R.chip(t + 0.1, t + L + 0.25, f"{pct}% tempo", y=440 if k == 0 else 330, kind="white")
        if k:
            R.s("whoosh", t - 0.12, 0.012)
        if k == 3:
            fin = t + L - 0.15
            R.confetti(fin, y=700, n=240)
            R.ring(fin, y=700)
            R.flash(fin, 0.3, 0.35)
            R.s("ding", fin, 0.04)
        t += L + 0.35
    R.cap(t, t + 2.3, "<i>Week 1</i>: left hand.<br><g>Week 2</g>: together.", y=600, cls="cap s", inn="pop")
    R.sub(t + 0.1, t + 2.3, "That's what the example plan does 👆", y=820, cls="sub s", inn="fade")
    R.dim(t - 0.1, t + 2.3, 0.6)
    R.s("pop", t, 0.04)
    R.outro(t + 2.35, ["You pick the piece.", "It decides <g>which hands, which day</g>."], kind="week", bed_from=t)
    R.build()


# ============ G3. Chunk it (Flight of the Bumblebee) ============
def chunks(name="g3-chunk-it"):
    run, lh, bpm = BB_RUN, BB_LH, BB_BPM
    R = Reel(name, 29.0, fit_end=True)
    R.cap(0, 0.15 + 20 * 60 / bpm + 0.85, "Fast passage<br><r>falling apart</r>? 😵", y=120, cls="cap s")
    ns = R.play(cut(run, 20), bpm, 0.15, sec="fail", hand="R", human=0.02)
    ns += R.play(cut(lh, 20), bpm, 0.15, sec="fail", hand="L", vel=0.5)
    tcr = 0.15 + 20 * 60 / bpm
    for k, m in enumerate([P("F4"), P("G4"), P("A4"), P("C4"), P("D#4")]):
        R.notes.append({"m": m, "t": round(tcr + 0.01 * k, 3), "d": 0.25, "v": 0.95, "h": "X", "sec": "fail"})
    R.section("fail", 0.1, tcr + 0.6)
    R.s("buzz", tcr, 0.05)
    R.shards(tcr, y=1300, n=120)
    R.redflash(tcr, 0.4, 0.5)
    R.shake(tcr, 0.16)
    lo, hi = rng(ns)
    R.frame(0, lo, hi, zoom=1.1)
    t = tcr + 0.9
    R.cap(t, t + 6.1, "Stop running it.<br><g>Chunk it.</g>", y=120, cls="cap s")
    R.s("whoosh", t - 0.1, 0.014)
    t += 0.3
    b = bpm * 0.7
    for k in range(4):
        seg = notes_window(run, k * 8, k * 8 + 8)
        ns = R.play(seg, b * 0.8, t, sec=f"ch{k}", hand="R")
        L = 8 * 60 / (b * 0.8)
        R.section(f"ch{k}", t - 0.05, t + L + 0.15)
        lo, hi = rng(ns)
        R.zone(t, t + L + 0.1, min(n["m"] for n in ns), max(n["m"] for n in ns))
        R.frame(t, lo, hi, zoom=1.35)
        R.chip(t, t + L + 0.1, f"Chunk {k + 1} of 4", y=440, kind="white")
        R.s("pop", t, 0.03, freq=800 + 150 * k)
        t += L + 0.22
    R.cap(t, t + 3.2, "Now <g>join</g> them.", y=120, cls="cap s")
    b2 = bpm * 0.85
    for k in range(2):
        seg = notes_window(run, k * 16, k * 16 + 16)
        ns = R.play(seg, b2, t, sec=f"j{k}", hand="R")
        L = 16 * 60 / b2
        R.section(f"j{k}", t - 0.05, t + L + 0.15)
        lo, hi = rng(ns)
        R.frame(t, lo, hi, zoom=1.2)
        R.chip(t, t + L + 0.1, "85% tempo", y=440, kind="")
        t += L + 0.25
    R.cap(t, t + 4.0, "Full speed. <g>Clean.</g> 🐝", y=120, cls="cap s")
    R.s("riser", t - 0.6, 0.035)
    ns = R.play(run + at(run, 32), bpm, t, sec="full", hand="R", vel=0.75)
    ns += R.play(lh + at(lh, 32), bpm, t, sec="full", hand="L", vel=0.5)
    L = 64 * 60 / bpm
    R.section("full", t - 0.05, t + L + 0.4)
    lo, hi = rng(ns)
    R.frame(t, lo, hi, zoom=1.0)
    R.frame(t + L, lo, hi, zoom=1.12, side=-0.5)
    R.chip(t, t + L + 0.2, "100% tempo", y=440, kind="solid")
    fin = t + L
    R.chord_hit(fin, ["A2", "A3", "C#4", "E4", "A4"], hold=1.2, vel=0.8)
    R.confetti(fin, y=700, n=260)
    R.ring(fin, y=700)
    R.flash(fin, 0.3, 0.4)
    R.s("ding", fin, 0.04)
    R.s("boom", fin, 0.08)
    t = fin + 1.0
    R.cap(t, t + 1.5, "What passage do <g>you</g><br>need to chunk? 👇", y=600, cls="cap s", inn="slam")
    R.dim(t - 0.1, t + 1.5, 0.6)
    R.outro(t + 1.55, ["So I built something that", "picks <g>one section</g> for you.", "With a <g>tempo target</g>."], kind="today", bed_from=t)
    R.build()


# ============ H1. Hanon speed test ============
def speed_test(name="h1-hanon-speed-test"):
    R = Reel(name, 29.4, fit_end=True)
    R.cap(0, 2.6, "Hanon No. 1 at <g>5 speeds</g>.<br>Where do you crash? 👇", y=120, cls="cap s")
    t = 0.2
    levels = [(60, 12), (90, 18), (120, 24), (160, 32), (200, 40)]
    for k, (q, units) in enumerate(levels):
        b = q * 4
        rh, lh = HANON(8)
        rh, lh = cut(rh, units), cut(lh, units)
        ns = R.play(rh, b, t + 0.45, sec=f"l{k}", hand="R") + R.play(lh, b, t + 0.45, sec=f"l{k}", hand="L", vel=0.55)
        L = units * 60 / b
        R.section(f"l{k}", t + 0.4, t + 0.45 + L + 0.12)
        R.slam(t, t + 0.75, f"{q} BPM", col="red" if k == 4 else "gold", y=760, size=0.8)
        R.s("levelup", t + 0.05, 0.03)
        lo, hi = rng(ns)
        R.frame(t, lo, hi, e="cut" if k else "io", zoom=1.05 + 0.04 * k)
        R.frame(t + 0.45 + L, lo, hi, zoom=1.12 + 0.06 * k, side=0.4 * (1 if k % 2 else -1))
        if k:
            R.cap(t, t + 0.45 + L + 0.1, f"Level <g>{k + 1}</g>", y=150, cls="cap s", inn="fade")
        R.pips(t, t + 0.45 + L + 0.15, 5, k, y=420)
        R.chip(t + 0.45, t + 0.45 + L + 0.1, f"{q} BPM · 16ths", y=540, kind="red" if k == 4 else "white")
        if k >= 3:
            R.shake(t + 0.45 + L * 0.5, 0.04 * k)
        t += 0.45 + L + 0.2
    fin = t - 0.1
    R.chord_hit(fin, ["C3", "C4", "E4", "G4", "C5"], hold=1.3, vel=0.85)
    R.confetti(fin, y=700, n=260)
    R.ring(fin, y=700)
    R.flash(fin, 0.3, 0.4)
    R.s("boom", fin, 0.1)
    R.s("ding", fin, 0.04)
    t = fin + 0.9
    R.cap(t, t + 2.8, "Too hard? Next session <i>−5%</i>.<br>Too easy? <g>+5%</g>.", y=560, cls="cap xs", inn="pop")
    R.dim(t - 0.1, t + 4.3, 0.6)
    R.s("pop", t, 0.04)
    R.cap(t + 2.85, t + 4.3, "Where did <g>you</g> crash? 👇", y=600, cls="cap s", inn="slam")
    R.outro(t + 4.35, ["After every session:", "Too hard / Just right / <g>Too easy</g>."], kind="checkin", bed_from=t)
    R.build()


# ============ I1. POV: your kid has been "practising" for 30 minutes ============
def pov_kid(name="i1-pov-kid-practising"):
    rh, lh, bpm = FE_RH, FE_LH, FE_BPM
    R = Reel(name, 30.0, fit_end=True)
    R.cap(0, 10.3, "POV: your kid has been<br>“practising” for <g>30 min</g>", y=120, cls="cap s")
    R.sub(0.3, 3.0, "(parents, you know 😅)", y=330, cls="sub s")
    t = 0.15
    clock = ["⏱ 0:40", "⏱ 9:15", "⏱ 18:30", "⏱ 29:50"]
    for k, st in enumerate([0, 8, 12, 14]):
        seg_rh, seg_lh = notes_window(rh, st, 17), notes_window(lh, st, 17)
        ns, _ = play_clip(R, seg_rh, seg_lh, bpm, t, f"loop{k}", t1=t + (17 - st) * 60 / bpm + 0.45)
        tm = t + (17 - st) * 60 / bpm
        R.notes.append({"m": P("G4"), "t": round(tm, 3), "d": 0.35, "v": 0.8, "h": "X", "sec": f"loop{k}"})
        R.s("buzz", tm + 0.02, 0.04)
        R.redflash(tm, 0.3, 0.3)
        lo, hi = rng(ns)
        R.frame(t, lo, hi, e="cut" if k else "io", zoom=1.12 + 0.05 * k)
        R.chip(t, tm + 0.4, f"Loop {[1, 7, 13, 19][k]}", y=440, kind="white")
        R.chip(t, tm + 0.4, clock[k], y=550, kind="sm")
        if k:
            R.s("scratch", t - 0.25, 0.035)
        t = tm + 0.5
    R.illus(0.3, t)
    R.cap(t, t + 1.7, "Same 4 bars.<br><r>Same mistake.</r>", y=560, cls="cap", inn="slam")
    R.pad(t, ["A2", "E3", "A3", "C4"], hold=5.0, vel=0.28)
    R.dim(t - 0.1, t + 5.0, 0.6)
    R.s("boom", t, 0.06)
    t += 1.75
    R.cap(t, t + 1.4, "It isn't laziness.", y=600, cls="cap s", inn="pop")
    R.s("whoosh", t - 0.05, 0.01)
    t += 1.45
    R.cap(t, t + 1.9, "They don't know<br><g>what to practise</g>.", y=600, cls="cap s", inn="pop")
    R.s("whoosh", t - 0.05, 0.01)
    t += 2.0
    R.cap(t, t + 4.9, "A plan says <g>exactly</g> what to do:", y=120, cls="cap s")
    R.chip(t + 0.2, t + 4.9, "Warm-up · 5 min", y=330, kind="sm white")
    R.chip(t + 0.5, t + 4.9, "Main work · 20 min: <g>that bar, slowly</g>", y=420, kind="sm")
    R.chip(t + 0.8, t + 4.9, "Run-through · 5 min", y=510, kind="sm white")
    hard_rh, hard_lh = notes_window(rh, 14, 20), notes_window(lh, 14, 20)
    ns, _ = play_clip(R, hard_rh, hard_lh, bpm * 0.6, t + 0.3, "slow", t1=t + 0.3 + 6 * 60 / (bpm * 0.6) + 0.2)
    lo, hi = rng(ns)
    R.frame(t, lo, hi, zoom=1.3)
    t2 = t + 0.3 + 6 * 60 / (bpm * 0.6) + 0.25
    ns, _ = play_clip(R, notes_window(rh, 0, 26), notes_window(lh, 0, 26), bpm, t2, "clean", t1=t2 + 26 * 60 / bpm + 0.3)
    lo, hi = rng(ns)
    R.frame(t2, lo, hi, zoom=1.05)
    fin = t2 + 24 * 60 / bpm
    R.confetti(fin, y=700, n=200)
    R.s("ding", fin, 0.04)
    R.chip(fin, fin + 1.0, "Clean ✅", y=700, kind="solid big")
    R.outro(fin + 1.0, ["So I built a plan they can", "<g>follow on their own</g>."], kind="today")
    R.build()


# ============ I2. Teacher sees them 30 minutes a week ============
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
POS = [(50, 640), (295, 640), (540, 640), (785, 640), (172, 990), (417, 990), (662, 990)]


def day_html(d, icon, text, small=""):
    sm = f"<small>{small}</small>" if small else ""
    return f'<div class="d">{d}</div><div class="i">{icon}</div><div class="t">{text}{sm}</div>'


def teacher_week(name="i2-teacher-30-min"):
    R = Reel(name, 27.4, fit_end=True)
    R.kb(0, 0)
    R.cam(0, [0, 3, 10], [0, 3, -1])
    R.cap(0, 3.0, "Their teacher sees them<br><g>30 minutes</g> a week.", y=120, cls="cap s")
    for i, d in enumerate(DAYS):
        x, y = POS[i]
        if i == 0:
            R.el(0.2, 9.6, day_html(d, "🎹", "Lesson", "30 min"), "day gold", y=y, style=f"left:{x}px;width:230px;", inn="pop", out="fade")
        else:
            R.el(0.35 + i * 0.12, 9.6, day_html(d, "❓", "?"), "day grey", y=y, style=f"left:{x}px;width:230px;", inn="pop", out="fade", shake=0 if i < 3 else 0)
        R.s("pop", 0.2 + i * 0.12, 0.03, freq=700 + 60 * i)
    R.cap(3.05, 6.4, "What happens on<br>the <r>other 6 days</r>?", y=120, cls="cap s")
    R.s("whoosh", 3.0, 0.012)
    R.cap(6.45, 9.6, "You pay for the lesson.<br>The rest is a <r>guessing game</r>.", y=120, cls="cap xs")
    R.s("buzz", 6.5, 0.03)
    t = 9.7
    R.cap(t, t + 4.3, "With a plan, every day<br>has a <g>session</g>:", y=120, cls="cap s")
    sessions = [("Session 1", "Left hand · 40%"), ("Session 2", "Left hand · 40%"), ("Session 3", "Right hand · 50%"), ("Session 4", "Left hand · 45%"), ("Session 5", "Left hand · 50%")]
    R.el(t, t + 8.9, day_html("Mon", "🎹", "Lesson", "30 min"), "day gold", y=POS[0][1], style=f"left:{POS[0][0]}px;width:230px;", inn="none", out="fade")
    for i in range(1, 7):
        x, y = POS[i]
        tf = t + 0.3 + (i - 1) * 0.42
        if i <= 5:
            nm, sub = sessions[i - 1]
            R.el(tf, t + 8.9, day_html(DAYS[i], "✅" if i < 3 else "🎯", nm, sub), "day glow" if i == 3 else "day", y=y, style=f"left:{x}px;width:230px;", inn="spin", out="fade")
            R.s("ding", tf, 0.02)
        else:
            R.el(tf, t + 8.9, day_html(DAYS[i], "😴", "Rest"), "day grey", y=y, style=f"left:{x}px;width:230px;", inn="spin", out="fade")
            R.s("pop", tf, 0.03)
    R.confetti(t + 2.9, y=800, n=160)
    R.illus(t + 0.3, t + 8.9, text="Real example plan · Week 1")
    R.cap(t + 4.35, t + 6.5, "They open it and follow<br><g>today's session</g>.", y=120, cls="cap s")
    R.cap(t + 6.55, t + 8.9, "What to play. How fast.<br><g>How long.</g>", y=120, cls="cap s")
    t2 = t + 9.0
    R.cap(t2, t2 + 1.5, "Parents: sound familiar? 👇", y=600, cls="cap s", inn="slam")
    R.outro(t2 + 1.55, ["Day 1 is free.", "No card. <g>See it first.</g>"], kind="today", bed=False)
    R.bed(0, R.dur, 84, C_BED, vel=0.25, kgain=0.05, hgain=0.015, arp=True, mixgain=0.85)
    R.build()


# ============ I3. Adult returners ============
def returner(name="i3-adult-returner"):
    rh, lh, bpm = MG_RH, MG_LH, MG_BPM
    R = Reel(name, 27.2, glow="rgba(120,170,255,0.22)", fit_end=True)
    R.meta["grade"] = 3
    R.meta["form"] = ("Petzold", "Minuet in G")
    R.cap(0, 6.6, "Played piano as a kid?<br><g>Come back</g> without starting over.", y=120, cls="cap xs")
    # halting, rusty version (blue)
    rusty = R.play(cut(rh, 24), bpm * 0.72, 0.2, sec="rusty", hand="L", vel=0.55)
    rusty += R.play(cut(lh, 24), bpm * 0.72, 0.2, sec="rusty", hand="L", vel=0.42)
    for n in rusty:
        if n["t"] > 1.6:
            n["t"] = round(n["t"] + 0.5, 3)
        if n["t"] > 3.6:
            n["t"] = round(n["t"] + 0.45, 3)
    R.notes.append({"m": P("C#5"), "t": 2.9, "d": 0.3, "v": 0.7, "h": "X", "sec": "rusty"})
    R.s("buzz", 2.92, 0.03)
    R.section("rusty", 0.1, 6.6)
    R.sub(1.0, 6.6, "Rusty? <i>Totally normal.</i>", y=420, cls="sub s", inn="fade")
    R.fx.append({"type": "shake", "t": 2.9, "a": 0.05})
    lo, hi = rng(rusty)
    R.frame(0, lo, hi, zoom=1.15)
    t = 6.7
    R.cap(t, t + 4.0, "Pick your grade <g>now</g>,<br>not where you stopped.", y=120, cls="cap xs")
    R.s("whoosh", t - 0.1, 0.012)
    ns, L = play_clip(R, cut(rh, 24), cut(lh, 24), bpm * 0.85, t + 0.2, "warm", t1=t + 0.2 + 24 * 60 / (bpm * 0.85) + 0.2)
    lo, hi = rng(ns)
    R.frame(t, lo, hi, zoom=1.05)
    t = t + 0.2 + 24 * 60 / (bpm * 0.85) + 0.25
    R.cap(t, t + 5.0, "Choose a piece you<br><g>actually</g> want to play.", y=120, cls="cap s")
    R.s("whoosh", t - 0.1, 0.012)
    ns, L = play_clip(R, notes_window(rh, 24, 48), notes_window(lh, 24, 48), bpm, t, "full", t1=t + 24 * 60 / bpm + 0.3)
    lo, hi = rng(ns)
    R.frame(t, lo, hi, zoom=1.0)
    R.frame(t + 24 * 60 / bpm, lo, hi, zoom=1.12, side=0.5)
    fin = t + 18 * 60 / bpm
    R.confetti(fin, y=700, n=200)
    R.ring(fin, y=700)
    R.s("ding", fin, 0.04)
    t = t + 24 * 60 / bpm + 0.35
    R.cap(t, t + 1.6, "What did you play<br>as a kid? 👇", y=600, cls="cap s", inn="slam")
    R.dim(t - 0.1, t + 1.6, 0.6)
    R.outro(t + 1.65, ["Pick your grade. Pick your piece.", "It plans <g>6 weeks</g> from there."], kind="grade", bed_from=t)
    R.build()


# ============ J1. Missed a day ============
def missed_day(name="j1-missed-a-day"):
    R = Reel(name, 27.0, fit_end=True)
    R.kb(0, 0)
    R.cam(0, [0, 3, 10], [0, 3, -1])
    R.cap(0, 6.4, "Missed <r>one</r> practice day…<br>and quit for a week? 😅", y=120, cls="cap s")
    marks = [("✅", "Practised", "gold"), ("✅", "Practised", "gold"), ("❌", "Missed", "red"), ("😩", "Gave up", "grey"), ("😩", "Gave up", "grey"), ("😩", "Gave up", "grey"), ("😩", "Gave up", "grey")]
    for i, (ic, tx, kind) in enumerate(marks):
        x, y = POS[i]
        ta = 0.25 + i * 0.32 + (0.6 if i >= 3 else 0)
        R.el(ta, 9.0, day_html(DAYS[i], ic, tx), f"day {kind}", y=y, style=f"left:{x}px;width:230px;", inn="pop", out="fade")
        R.s("buzz" if kind == "red" else "pop", ta, 0.04 if kind == "red" else 0.03, **({} if kind == "red" else {"freq": 900}))
        if kind == "red":
            R.redflash(ta, 0.4, 0.45)
            R.shake(ta, 0.1)
    R.slam(1.1, 2.6, "STREAK LOST", col="red", y=1420, size=0.62)
    R.shards(1.15, y=1420, n=120)
    R.illus(0.3, 9.0)
    R.cap(6.45, 9.0, "Plans built on <r>dates</r><br>break when life happens.", y=120, cls="cap s")
    R.s("whoosh", 6.4, 0.012)
    t = 9.1
    R.slam(t, t + 1.4, "SESSIONS", col="gold", y=760, size=0.75)
    R.cap(t, t + 1.5, "<g>Sessions</g>, not dates.", y=120, cls="cap")
    t += 1.6
    plan = [("✅", "Session 1", "", "gold"), ("✅", "Session 2", "", "gold"), ("⚽", "Busy", "no practice", "grey"), ("🎯", "Session 3", "waiting for you", "glow"), ("·", "Session 4", "", ""), ("·", "Session 5", "", ""), ("·", "Session 6", "", "")]
    for i, (ic, tx, sm, kind) in enumerate(plan):
        x, y = POS[i]
        ta = t + i * 0.25
        R.el(ta, t + 7.2, day_html(DAYS[i], ic, tx, sm), f"day {kind}", y=y, style=f"left:{x}px;width:230px;", inn="spin", out="fade")
        R.s("pop", ta, 0.025, freq=800 + 50 * i)
    R.confetti(t + 1.0, y=820, n=180)
    R.s("ding", t + 0.8, 0.04)
    R.cap(t + 0.2, t + 3.6, "Miss a day?<br><g>It just waits for you.</g>", y=120, cls="cap s")
    R.cap(t + 3.65, t + 7.2, "No “you're behind” messages.<br><g>Ever.</g>", y=120, cls="cap xs")
    t2 = t + 7.3
    R.cap(t2, t2 + 1.5, "What makes <g>you</g> skip practice? 👇", y=600, cls="cap s", inn="slam")
    R.outro(t2 + 1.55, ["You pick the days.", "It plans <g>every session</g>."], kind="week", bed=False)
    R.bed(0, R.dur, 84, C_BED, vel=0.25, kgain=0.05, hgain=0.015, arp=True, mixgain=0.85)
    R.build()


# ============ K1. What 30 minutes should look like ============
def thirty_min(name="k1-30-minutes"):
    rh, lh, bpm = FE_RH, FE_LH, FE_BPM
    R = Reel(name, 30.0, fit_end=True)
    R.cap(0, 5.6, "What 30 minutes of practice<br><g>should</g> look like 🎹", y=120, cls="cap xs")
    R.chip(0.3, 5.6, "Usually: play it through. Again. <r>Again.</r>", y=330, kind="sm red")
    t = 0.2
    for k, st in enumerate([0, 6, 12]):
        seg_rh, seg_lh = notes_window(rh, st, 26), notes_window(lh, st, 26)
        L = (26 - st) * 60 / bpm
        ns, _ = play_clip(R, seg_rh, seg_lh, bpm, t, f"u{k}", t1=t + min(L, 1.9))
        lo, hi = rng(ns)
        R.frame(t, lo, hi, e="cut" if k else "io", zoom=1.05 + 0.06 * k)
        R.el(t, t + min(L, 1.9), '<div class="segbar grey"><div style="flex:1">Play through #' + str(k + 1) + '</div></div>', "", y=440, inn="fade", out="none")
        if k:
            R.s("scratch", t - 0.2, 0.035)
        t += min(L, 1.9) + 0.05
    R.illus(0.3, t)
    t = 5.8
    R.cap(t, t + 1.4, "With a plan:", y=120, cls="cap")
    R.pad(t - 0.2, ["A2", "E3", "C4", "E4"], hold=1.6, vel=0.3)
    R.s("whoosh", t - 0.1, 0.014)

    def segbar(on):
        cls = ["s1", "s2", "s3"]
        txt = ["Warm-up<br>5", "Main work · 20 min", "Run-through<br>5"]
        return '<div class="segbar">' + "".join(f'<div class="{c}{"" if on in (None, i) else " dim"}">{x}</div>' for i, (c, x) in enumerate(zip(cls, txt))) + "</div>"
    R.el(t, t + 1.4, segbar(None), "", y=420, inn="pop", out="none")
    t += 1.45
    # warm-up: broken chord arpeggios, both hands
    wu = S("A2:1 E3 A3 C4 E4 A4 C5 E5 A4 E4 C4 A3", hand="L") + S("E5:1 C5 A4 E4 C4 A3 E3 A2", t=12, hand="R")
    R.el(t, t + 3.2, segbar(0), "", y=420, inn="none", out="none")
    R.cap(t, t + 3.2, "<g>Warm-up</g>: slow broken chords", y=150, cls="cap xs", inn="fade")
    ns = R.play(wu, 300, t + 0.2, sec="wu", vel=0.55)
    R.section("wu", t, t + 3.3)
    lo, hi = rng(ns)
    R.frame(t, lo, hi, zoom=1.0)
    t += 3.3
    R.el(t, t + 4.3, segbar(1), "", y=420, inn="none", out="none")
    R.cap(t, t + 4.3, "<g>Main work</g>: one section,<br>one hand, slowly", y=120, cls="cap xs", inn="fade")
    R.s("whoosh", t - 0.1, 0.012)
    m_rh = notes_window(rh, 8, 18)
    ns = R.play(m_rh, bpm * 0.6, t + 0.2, sec="mw", vel=0.6)
    L = 10 * 60 / (bpm * 0.6)
    R.section("mw", t, t + 0.2 + L + 0.2)
    R.chip(t + 0.2, t + 0.2 + L, "Right hand · 60% tempo", y=610, kind="sm")
    lo, hi = rng(ns)
    R.frame(t, lo, hi, zoom=1.3)
    t += 0.2 + L + 0.3
    R.el(t, t + 6.0, segbar(2), "", y=420, inn="none", out="none")
    R.cap(t, t + 6.0, "<g>Run-through</g>:<br>the whole thing, once", y=120, cls="cap xs", inn="fade")
    R.s("whoosh", t - 0.1, 0.012)
    ns, _ = play_clip(R, notes_window(rh, 0, 26), notes_window(lh, 0, 26), bpm, t + 0.1, "rt", t1=t + 0.1 + 26 * 60 / bpm + 0.4)
    lo, hi = rng(ns)
    R.frame(t, lo, hi, zoom=1.0)
    R.frame(t + 26 * 60 / bpm, lo, hi, zoom=1.12, side=0.4)
    fin = t + 0.1 + 24 * 60 / bpm
    R.confetti(fin, y=700, n=220)
    R.ring(fin, y=700)
    R.s("ding", fin, 0.04)
    t = fin + 0.6
    R.cap(t, t + 1.5, "Which part do<br>you <g>skip</g>? 👇", y=600, cls="cap", inn="slam")
    R.dim(t - 0.1, t + 1.5, 0.6)
    R.outro(t + 1.55, ["Every session, timed for you.", "Warm-up. <g>Main work.</g> Run-through."], kind="today", bed_from=t)
    R.build()

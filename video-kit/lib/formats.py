"""Reusable video formats. Each function builds one Reel (audio + timing) from a short spec."""
from reel import *
from music import *


def rng(notes, lo_min=33, hi_max=88):
    ms = [n["m"] for n in notes if lo_min <= n["m"] <= hi_max]
    if not ms:
        return 55, 72
    lo, hi = min(ms), max(ms)
    if hi - lo < 14:
        c = (hi + lo) // 2
        lo, hi = c - 7, c + 7
    return lo, hi


def seconds(seq, bpm):
    return span(seq) * 60.0 / bpm


def cut(seq, units):
    return [s for s in seq if s[1] < units - 1e-6]


def stretch_sec(R, sid, t0, t1):
    R.section(sid, t0, t1)


def play_clip(R, rh, lh, bpm, t0, sec, units=None, vel=None, pedal=None, hand_r="R", hand_l="L", t1=None):
    if units:
        rh, lh = cut(rh, units), cut(lh, units)
    ns = R.play(rh, bpm, t0, sec=sec, hand=hand_r, vel=vel or 0.7, pedal=pedal)
    ns += R.play(lh, bpm, t0, sec=sec, hand=hand_l, vel=0.5, pedal=pedal)
    length = (units if units else max(span(rh), span(lh) if lh else 0)) * 60.0 / bpm
    R.section(sec, t0 - 0.05, t1 if t1 else t0 + length + 0.6)
    return ns, length


# ============ A. Guess the piece ============
def guess(name, rounds, hook, sub, outro_lines, form, comment="Comment your score <g>/4</g> 👇", seasonal=False):
    """rounds: list of dict(rh, lh, bpm, clip (units), full (units), answer, small)"""
    t = 0.15
    plan = []
    for r in rounds:
        cl = r["clip"] * 60 / r["bpm"]
        fl = r["full"] * 60 / r["bpm"]
        plan.append((t, cl, fl))
        t += cl + 0.25 + 1.35 + min(fl, 2.0) + 0.25
    dur = round(t + 6.4, 2)
    R = Reel(name, dur)
    R.meta["form"] = form
    R.cap(0, 2.3, hook, y=120, cls="cap s")
    R.sub(0.15, 2.3, sub, y=330)
    n = len(rounds)
    for i, (r, (t0, cl, fl)) in enumerate(zip(rounds, plan)):
        ns, _ = play_clip(R, r["rh"], r["lh"], r["bpm"], t0, f"c{i}", units=r["clip"], t1=t0 + cl + 0.35)
        lo, hi = rng(ns)
        R.frame(t0, lo, hi, e="cut" if i else "io", zoom=1.0)
        R.frame(t0 + cl, lo, hi, zoom=1.12)
        R.cap(t0 if i else 2.3, t0 + cl + 1.6, f"Round <g>{i + 1}</g> of {n}", y=150, cls="cap s")
        if i:
            R.s("whoosh", t0 - 0.15, 0.014)
            R.flash(t0 - 0.02, 0.25, 0.25)
        R.pips(t0, t0 + cl + 1.75 + min(fl, 2.0), n, i, y=420)
        tt = t0 + cl + 0.25
        R.timer(tt, tt + 1.35, 3, y=760)
        R.chip(tt, tt + 1.35, "Name it? 🤔", y=1040, kind="white")
        R.dim(tt - 0.05, tt + 1.3, 0.5)
        rv = tt + 1.35
        R.s("riser", rv - 0.7, 0.03)
        ns2, _ = play_clip(R, r["rh"], r["lh"], r["bpm"], rv + 0.05, f"a{i}", units=r["full"], t1=rv + min(fl, 2.0) + 0.2)
        lo2, hi2 = rng(ns2)
        R.frame(rv, lo2, hi2, e="o", zoom=0.95)
        R.el(rv, rv + min(fl, 2.0) + 0.1, f'{r["answer"]}<small>{r["small"]}</small>', "answer", y=500, inn="slam")
        R.confetti(rv + 0.02, y=640, n=200)
        R.ring(rv, y=640)
        R.shake(rv, 0.1)
        R.flash(rv, 0.3, 0.3)
        R.s("ding", rv + 0.03, 0.035)
        R.s("boom", rv, 0.08)
        if i == n - 1:
            R.chip(rv + 0.4, rv + min(fl, 2.0) + 0.2, comment, y=1060, kind="solid big")
    t_out = plan[-1][0] + plan[-1][1] + 0.25 + 1.5 + min(plan[-1][2], 2.4) + 0.3
    R.outro(t_out, outro_lines, kind="form")
    R.build()
    return R


# ============ B. Grade 1 vs 5 vs 8 ============
def grades(name, title, levels, hook=None, sub="(wait for Grade 8 🤯)", outro_lines=None, form=None, notes_lbl=None, hook_units=None):
    """levels: list of (grade:int, rh, lh, bpm, desc). Last level's tail is used as the hook."""
    g8 = levels[-1]
    hu = hook_units or 2.0 * g8[3] / 60
    tail_start = max(span(g8[1]), span(g8[2]) if g8[2] else 0) - hu
    hook_rh = at([s for s in g8[1] if s[1] >= tail_start], -tail_start)
    hook_lh = at([s for s in g8[2] if s[1] >= tail_start], -tail_start)
    R0 = []
    t = 0.12
    hook_len = hu * 60 / g8[3]
    lens = [max(span(l[1]), span(l[2]) if l[2] else 0) * 60 / l[3] for l in levels]
    dur = round(t + hook_len + 0.3 + sum(L + 0.85 for L in lens) + 1.45 + 6.4, 2)
    R = Reel(name, dur)
    if form:
        R.meta["form"] = form
    ns, _ = play_clip(R, hook_rh, hook_lh, g8[3], t, "hook", t1=t + hook_len + 0.15)
    lo, hi = rng(ns)
    R.frame(0, lo, hi, zoom=1.15)
    R.frame(t + hook_len, lo, hi, zoom=1.3)
    R.cap(0, t + hook_len + 0.1, hook or f"Same song.<br><g>Grade 1</g> vs <g>Grade 8</g>", y=120, cls="cap s")
    R.sub(0.2, t + hook_len + 0.1, f"{title} {sub}", y=330, cls="sub s")
    t = t + hook_len + 0.3
    R.s("scratch", t - 0.3, 0.05)
    R.flash(t - 0.1, 0.25, 0.35)
    for k, ((gr, rh, lh, bpm, desc), L) in enumerate(zip(levels, lens)):
        R.slam(t, t + 0.85, f"GRADE {gr}", col="gold" if gr < 8 else "red", y=720, size=0.9)
        R.confetti(t + 0.05, y=720, n=80 if gr < 8 else 160, sound=False)
        R.s("levelup", t + 0.05, 0.03)
        t1 = t + 0.6
        ns, _ = play_clip(R, rh, lh, bpm, t1, f"g{gr}", t1=t1 + L + 0.25)
        lo, hi = rng(ns)
        R.frame(t, lo, hi, e="cut" if k else "io", zoom=1.05)
        R.frame(t1 + L * 0.5, lo, hi, zoom=1.18, side=0.4 if k % 2 else -0.4)
        R.frame(t1 + L, lo, hi, zoom=1.05)
        states = ["on" if i < gr else "" for i in range(8)]
        R.pips(t, t1 + L + 0.2, 8, gr - 1, y=400, states=states)
        R.cap(t, t1 + L + 0.2, f"Grade <g>{gr}</g>", y=150, cls="cap s", inn="fade")
        R.sub(t + 0.8, t1 + L + 0.2, desc, y=470, cls="sub s", inn="up")
        if k == len(levels) - 1:
            fin = t1 + L - 1.0
            R.confetti(fin, y=700, n=260)
            R.flash(fin, 0.4, 0.45)
            R.shake(fin, 0.18)
            R.ring(fin, y=700, s=3.2)
            R.s("boom", fin, 0.11)
        t = t1 + L + 0.25
    R.cap(t, t + 1.4, "Which grade<br>are <g>you</g>? 👇", y=600, cls="cap", inn="slam")
    R.dim(t - 0.1, t + 1.4, 0.6)
    R.s("whoosh", t - 0.1, 0.014)
    R.outro(t + 1.45, outro_lines or ["Whatever grade you're at,", "it plans <g>6 weeks</g> for it."], kind="form" if form else "today", bed_from=t)
    R.build()
    return R


# ============ C. "Piano is my therapy" / ONE mistake ============
def therapy(name, calm, mistake_at, wrong, fix_seq, fix_lh, fix_bpm, piece_lbl, emoji="🕊️", pcts=(60, 80, 100)):
    """calm: (rh, lh, bpm, units). mistake_at: beat index (units) where the wrong note replaces the melody.
    wrong: (midi_name) wrong note. fix_seq/fix_lh: the bar that broke (units at fix_bpm)."""
    rh, lh, bpm, units = calm
    tm = 0.2 + mistake_at * 60 / bpm
    fixlen = max(span(fix_seq), span(fix_lh) if fix_lh else 0) * 60 / fix_bpm
    dur = round(tm + 3.6 + 1.0 + sum(fixlen * 100 / p + 0.25 for p in pcts) + 0.8 + 6.4, 2)
    R = Reel(name, dur, glow="rgba(255,200,140,0.32)")
    pre_rh = [s for s in rh if s[1] < mistake_at - 1e-6]
    pre_lh = [s for s in lh if s[1] < mistake_at - 1e-6]
    ns, _ = play_clip(R, pre_rh, pre_lh, bpm, 0.2, "calm", t1=tm + 0.05, vel=0.55)
    lo, hi = rng(ns)
    R.frame(0, lo, hi, zoom=1.0)
    R.frame(tm - 0.4, lo, hi, zoom=1.25, side=0.6)
    R.cap(0, tm - 1.9, f"Piano is my therapy {emoji}", y=130, cls="cap s", inn="fade")
    R.sub(0.6, tm - 1.9, f"<m>{piece_lbl}</m>", y=340, cls="sub s", inn="fade")
    R.cap(tm - 1.8, tm + 3.4, "Also me after<br><r>ONE</r> mistake:", y=130, cls="cap s")
    R.s("whoosh", tm - 1.85, 0.01)
    # the wrong note
    R.notes.append({"m": P(wrong), "t": round(tm, 3), "d": 0.5, "v": 0.85, "h": "X", "sec": "calm2"})
    R.section("calm2", tm - 0.02, tm + 0.75)
    R.s("buzz", tm + 0.02, 0.045)
    R.redflash(tm + 0.02, 0.35, 0.35)
    R.shake(tm + 0.02, 0.06)
    R.el(tm + 0.05, tm + 0.7, "😐", "emoji", y=700, style="font-size:150px;", inn="pop")
    # rage
    t = tm + 0.75
    import numpy as np
    rnd = np.random.default_rng(5)
    rage = []
    for k in range(14):
        tt = t + k * 0.13
        base = int(rnd.integers(lo - 6, hi + 2))
        cl = [base, base + int(rnd.integers(1, 4)), base + int(rnd.integers(4, 9)), base - int(rnd.integers(5, 12))]
        for m in cl:
            rage.append({"m": int(max(36, min(86, m))), "t": round(tt, 3), "d": 0.12, "v": 0.95, "h": "X", "sec": "rage"})
    R.notes += rage
    R.section("rage", t - 0.02, t + 2.2)
    R.explode(t + 0.05, t + 2.4)
    R.shards(t + 0.05, y=1300, n=180)
    R.redflash(t + 0.05, 0.6, 0.8)
    R.shake(t + 0.05, 0.28)
    R.shake(t + 0.9, 0.18)
    R.s("boom", t + 0.03, 0.14)
    R.s("shatter", t + 0.05, 0.06)
    R.frame(t, lo - 6, hi + 6, e="o", zoom=0.9)
    # calm down + fix
    t = t + 2.75
    R.pad(t - 0.5, ["A2", "E3", "C4", "E4"], hold=1.4, vel=0.3)
    R.cap(t, t + 1.9, "Fix the bar,<br><g>not your mood</g>.", y=130, cls="cap s")
    R.s("whoosh", t - 0.1, 0.012)
    t += 0.5
    fix0 = t
    for k, (pct, col) in enumerate(zip(pcts, ["blue", "", "solid"])):
        b = fix_bpm * pct / 100
        L = max(span(fix_seq), span(fix_lh) if fix_lh else 0) * 60 / b
        ns, _ = play_clip(R, fix_seq, fix_lh, b, t, f"fix{k}", t1=t + L + 0.15)
        flo, fhi = rng(ns)
        R.frame(t, flo, fhi, e="io" if k == 0 else "o", zoom=1.25 - 0.08 * k)
        R.chip(t, t + L + 0.1, f"{pct}% tempo", y=440, kind=col)
        if k:
            R.s("whoosh", t - 0.1, 0.01)
        if k == 2:
            fin = t + L - 0.05
            R.confetti(fin, y=700, n=220)
            R.ring(fin, y=700)
            R.s("ding", fin, 0.04)
            R.flash(fin, 0.3, 0.3)
            R.chip(fin, fin + 1.2, "Clean ✅", y=560, kind="solid big")
        t += L + 0.25
    R.cap(fix0 + 1.4, t - 0.1, "Loop the bar<br>that broke. <g>Slowly.</g>", y=130, cls="cap s")
    R.outro(t + 0.8, ["So I built something that", "plans <g>that bar</g> for you.", "Which section. Which hands. <g>What tempo.</g>"], kind="today", bed_from=t)
    R.build()
    return R


# ============ D. No pedal vs pedal vs too much ============
def pedal(name, clip, piece_lbl, three=True, hook=None, units=None):
    """clip: (rh, lh, bpm, pedal_beats)"""
    rh, lh, bpm, pb = clip
    if units:
        rh = [tuple([q[0], q[1], min(q[2], units - q[1])] + list(q[3:])) for q in rh if q[1] < units]
        lh = [tuple([q[0], q[1], min(q[2], units - q[1])] + list(q[3:])) for q in lh if q[1] < units]
    L = (units or max(span(rh), span(lh))) * 60 / bpm
    dur = round(0.2 + (L + 0.6) * (3 if three else 2) + 1.6 + 7.0, 2)
    R = Reel(name, dur)
    R.wet = 0.12
    t = 0.2
    labels = [("Pedal: <r>OFF</r>", "red", None, "Without pedal"), ("Pedal: <g>ON</g>", "", pb, "With pedal"), ("Pedal: <r>NEVER UP</r> 😵", "red", "hold", "Too much pedal")]
    if not three:
        labels = labels[:2]
    R.cap(0, t + L + 0.3, hook or "Piano <r>without</r> pedal<br>vs <g>with</g> pedal", y=120, cls="cap s")
    for k, (lab, kind, pd, short) in enumerate(labels):
        # dry version: shorten notes a touch so it sounds clearly unpedalled
        rr = rh if pd else [tuple([s[0], s[1], min(s[2], 1.0)] + list(s[3:])) for s in rh]
        ll = lh if pd else [tuple([s[0], s[1], min(s[2], 1.0)] + list(s[3:])) for s in lh]
        ns, _ = play_clip(R, rr, ll, bpm, t, f"p{k}", pedal=pd, t1=t + L + 0.45)
        for n in ns:
            if pd == "hold":
                n["pe"] = round(t + L + 0.4, 3)
        lo, hi = rng(ns)
        R.frame(t, lo, hi, e="cut" if k else "io", zoom=1.08 - 0.04 * k)
        R.frame(t + L, lo, hi, zoom=1.2, side=0.5 * (1 if k % 2 else -1))
        R.chip(t, t + L + 0.35, lab, y=420, kind=kind or "white")
        R.el(t + 0.1, t + L + 0.35, "🦶" + ("⬇️" if pd else "⬆️"), "emoji", y=560, style="font-size:90px;", inn="pop")
        if k:
            R.cap(t, t + L + 0.35, f"<g>{short}</g>" if k == 1 else f"<r>{short}</r>", y=140, cls="cap s")
            R.s("whoosh", t - 0.15, 0.014)
            R.flash(t - 0.03, 0.25, 0.3 if k == 1 else 0.2)
        if pd == "hold":
            R.haze(t + L * 0.35, t + L + 0.3, 1.0)
            R.wet = 0.18
        t += L + 0.6
    R.cap(t - 0.1, t + 1.5, "Which one sounds<br><g>right</g> to you? 👇", y=600, cls="cap", inn="slam")
    R.dim(t - 0.2, t + 1.5, 0.6)
    R.s("boom", t - 0.08, 0.06)
    R.outro(t + 1.55, ["Pedal is <g>one</g> detail.", "So I built something that tells you <g>what to work on</g>."], kind="today", bed_from=t)
    R.build()
    return R


# ============ E. Sounds harder / easier than it is ============
def harder(name, items, hook, outro_lines, form, comment, reverse=False):
    """items: (label, rh, lh, bpm, units, sounds, actually)"""
    t = 0.15
    lens = [u * 60 / bpm for (_, _, _, bpm, u, _, _) in items]
    dur = round(t + sum(L + 2.0 for L in lens) + 1.5 + 7.0, 2)
    R = Reel(name, dur)
    R.meta["form"] = form
    R.cap(0, 2.2, hook, y=120, cls="cap s")
    for k, ((lab, rh, lh, bpm, u, sounds, actually), L) in enumerate(zip(items, lens)):
        ns, _ = play_clip(R, rh, lh, bpm, t, f"h{k}", units=u + 1.8 * bpm / 60, t1=t + L + 1.75)
        lo, hi = rng(ns)
        R.frame(t, lo, hi, e="cut" if k else "io", zoom=1.05)
        R.frame(t + L + 1.6, lo, hi, zoom=1.22, side=0.5 * (1 if k % 2 else -1))
        if k:
            R.cap(t, t + 1.8, f"<g>#{k + 1}</g>", y=150, cls="cap xl", inn="slam")
            R.s("whoosh", t - 0.15, 0.014)
            R.flash(t - 0.03, 0.22, 0.25)
        R.chip(t + 0.1, t + L + 1.8, lab, y=420 if k else 330, kind="white")
        tb = t + max(1.2, L - 1.3)
        R.el(tb, t + L + 1.8, f"Sounds like: <s style='text-decoration:line-through;text-decoration-thickness:6px'>{sounds}</s>", "chip red", y=560, inn="pop")
        R.s("pop", tb, 0.04, freq=700)
        ta = tb + 0.9
        R.el(ta, t + L + 1.8, f"Actually: <b style='font-weight:900'>{actually}</b>", "chip solid big", y=680, inn="slam")
        R.s("boom", ta, 0.07)
        R.s("ding", ta + 0.02, 0.03)
        R.confetti(ta, y=700, n=120, sound=False)
        R.shake(ta, 0.08)
        t += L + 2.0
    R.cap(t - 0.1, t + 1.5, comment, y=600, cls="cap", inn="slam")
    R.dim(t - 0.2, t + 1.5, 0.6)
    R.illus(0.4, t + 1.5, text="Grades are approximate")
    R.outro(t + 1.55, outro_lines, kind="form", bed_from=t)
    R.build()
    return R

import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from formats import *
which = sys.argv[1:] or ["all"]
def want(n): return "all" in which or n in which
def window(seq, a, b, shift=True):
    out = [s for s in seq if a - 1e-6 <= s[1] < b - 1e-6]
    return at(out, -a) if shift else out

# ---------- C: therapy ----------
if want("c1"):
    rh, lh = GYM(8)
    rh, lh = window(rh, 6, 30), window(lh, 6, 30)
    fix_rh, fix_lh = window(rh, 6, 10), window(lh, 6, 10)
    therapy("c1-therapy-gymnopedie", (rh, lh, GYM_BPM, 24), 9, "A#4", fix_rh, fix_lh, GYM_BPM, "Satie · Gymnopédie No. 1", pcts=(75, 100))
if want("c2"):
    rh, lh = CANON(2)
    fix_rh, fix_lh = window(rh, 12, 16), window(lh, 12, 16)
    therapy("c2-therapy-canon", (rh, lh, CANON_BPM, 64), 12, "C5", fix_rh, fix_lh, CANON_BPM, "Pachelbel · Canon in D")
if want("c3"):
    fix_rh, fix_lh = window(BL_RH, 14, 20), window(BL_LH, 14, 20)
    therapy("c3-therapy-lullaby", (BL_RH, BL_LH, BL_BPM, 50), 14, "C#5", fix_rh, fix_lh, BL_BPM, "Brahms · Lullaby", emoji="😌")

# ---------- D: pedal ----------
if want("d1"):
    rh, lh = BACHC(2)
    pedal("d1-pedal-bach", (rh, lh, 300, 8), "Bach · Prelude in C")
if want("d2"):
    rh, lh = ML1(2, mel=False)
    pedal("d2-pedal-moonlight", (rh, lh, 170, 12), "Beethoven · Moonlight Sonata", hook="Moonlight Sonata<br><r>without</r> vs <g>with</g> pedal", units=18)
if want("d3"):
    rh = cut(SN_RH, 24)
    lh = []
    for i, (b, ch) in enumerate(SN_CHORDS[:4]):
        lh += S(f"{b}:1 {ch[0]} {ch[1]} {ch[2]} {ch[1]} {ch[0]}", t=i * 6, hand="L", vel=0.4)
    pedal("d3-pedal-silent-night", (rh, lh, 215, 6), "Gruber · Silent Night", hook="Silent Night<br><r>without</r> vs <g>with</g> pedal 🎄")

# ---------- E: sounds harder / easier ----------
if want("e1"):
    brh, blh = BACHC(2)
    grh, glh = GYM(8); grh, glh = window(grh, 7, 13), window(glh, 6, 13)
    grh = at(grh, 1)
    mrh, mlh = ML1(1, mel=False)
    harder("e1-sounds-harder", [
        ("Bach · Prelude in C", brh, blh, 300, 24, "Grade 8", "around Grade 4–5"),
        ("Satie · Gymnopédie No. 1", grh, glh, GYM_BPM, 7, "Grade 8", "around Grade 4"),
        ("Beethoven · Moonlight, 1st mvt", mrh, mlh, 160, 12, "Grade 8", "around Grade 6"),
    ], "Pieces that sound<br><g>WAY harder</g> than they are 🤫", ["Pick one. <g>Type it in.</g>", "Get <g>6 weeks</g> of sessions for it."], ("Satie", "Gymnopédie No. 1"),
       "Which one are<br>you learning? 👇")
if want("e2"):
    harder("e2-sounds-easy", [
        ("Mozart · Sonata K. 545", K545_RH, K545_LH(), K545_BPM, 32, "Grade 2", "around Grade 5–6"),
        ("Mozart · Turkish March", TM_RH, TM_LH, TM_BPM, 36, "Grade 3", "around Grade 7"),
        ("Beethoven · Für Elise (all of it)", FE_RH, FE_LH, FE_BPM, 26, "Grade 2", "around Grade 5"),
    ], "Pieces that sound <g>easy</g>…<br>until you play them 😬", ["Learning one?", "Get <g>6 weeks</g> of sessions built for it."], ("Mozart", "Turkish March"),
       "Which one<br>humbled <g>you</g>? 👇")

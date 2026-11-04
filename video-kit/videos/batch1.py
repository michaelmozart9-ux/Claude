import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from formats import *
which = sys.argv[1:] or ["all"]
def want(n): return "all" in which or n in which

def octv(seq):
    out = []
    for s in seq:
        n = s[0]
        if isinstance(n, str):
            up = n[:-1] + str(int(n[-1]) + 1)
            out.append(tuple([[n, up]] + list(s[1:])))
        else:
            out.append(s)
    return out

SN_LH = []
for i, (b, ch) in enumerate(SN_CHORDS):
    SN_LH.append(([b] + ch, i * 6, 6, "L", 0.36))

# ---------- A1 / A2 / A3: guess ----------
if want("a1"):
    guess("a1-guess-classical", [
        dict(rh=B5_RH, lh=B5_LH, bpm=B5_BPM, clip=10, full=22, answer="Beethoven 5", small="Symphony No. 5"),
        dict(rh=MK_RH, lh=MK_LH, bpm=MK_BPM, clip=8, full=32, answer="Mountain King", small="Grieg · Peer Gynt"),
        dict(rh=BC_RH, lh=BC_LH, bpm=BC_BPM, clip=12, full=32, answer="Bridal Chorus", small="Wagner · “Here comes the bride”"),
        dict(rh=FM_RH, lh=FM_LH, bpm=FM_BPM, clip=8, full=32, answer="Funeral March", small="Chopin · Sonata No. 2"),
    ], "Name the piece in<br><g>2 seconds</g> 🎹", "Only real pianists get <g>4/4</g>",
       ["Know it? Now <g>actually learn it</g>.", "Type in a piece. Get <g>6 weeks</g> of sessions."], ("Grieg", "In the Hall of the Mountain King"))
if want("a2"):
    guess("a2-guess-christmas", [
        dict(rh=JB_RH, lh=JB_LH, bpm=JB_BPM, clip=8, full=16, answer="Jingle Bells", small="Pierpont · 1857"),
        dict(rh=COB_RH, lh=COB_LH, bpm=COB_BPM, clip=12, full=36, answer="Carol of the Bells", small="Leontovych"),
        dict(rh=SN_RH, lh=SN_LH, bpm=SN_BPM, clip=6, full=24, answer="Silent Night", small="Gruber · 1818"),
        dict(rh=WW_RH, lh=WW_LH, bpm=WW_BPM, clip=8, full=26, answer="We Wish You a Merry Christmas", small="Traditional"),
    ], "Name the Christmas song<br>in <g>2 seconds</g> 🎄", "Bet you can't get <g>4/4</g>",
       ["Got all 4? Learn one <g>properly</g> this year.", "Type it in. Get <g>6 weeks</g> of sessions."], ("Leontovych", "Carol of the Bells"),
       comment="Comment your score <g>/4</g> 🎄")
if want("a3"):
    guess("a3-guess-pianists", [
        dict(rh=FE_RH, lh=FE_LH, bpm=FE_BPM, clip=8, full=26, answer="Für Elise", small="Beethoven"),
        dict(rh=TM_RH, lh=TM_LH, bpm=TM_BPM, clip=12, full=36, answer="Turkish March", small="Mozart · Rondo alla Turca"),
        dict(rh=TO_RH, lh=TO_LH, bpm=TO_BPM, clip=8, full=22, answer="Toccata in D minor", small="Bach · BWV 565"),
        dict(rh=EN_RH, lh=EN_LH, bpm=EN_BPM, clip=12, full=34, answer="The Entertainer", small="Scott Joplin"),
    ], "Every pianist knows these.<br>Do <g>you</g>? 🎹", "Name all <g>4</g> 👇",
       ["Know it? Now <g>actually learn it</g>.", "Type in a piece. Get <g>6 weeks</g> of sessions."], ("Beethoven", "Für Elise"))

# ---------- B1: Carol of the Bells grades ----------
if want("b1"):
    M = COB_MOT
    g1_rh = rep(M, 2, 6) + at(S("D5:2 C5:1 D5:1 Bb4:2"), 12) + at(M, 18)
    g1_lh = S("G3:6 G3:6 G3:6 G3:6", hand="L", vel=0.42)
    g5_rh = rep(M, 4, 6) + at(S("D5:2 C5:1 D5:1 Bb4:2", vel=0.72), 24) + at(S("G5:2 F5:1 G5:1 D5:2", vel=0.74), 30)
    g5_lh = []
    for k, (b, f, o) in enumerate([("G2", "D3", "G3"), ("F2", "D3", "G3"), ("Eb2", "Bb2", "G3"), ("D2", "A2", "F#3"), ("G2", "D3", "G3"), ("D2", "A2", "F#3")]):
        g5_lh += S(f"{b}:1 {f} {o} {f} {o} {f}", t=k * 6, hand="L", vel=0.45)
    g8_rh = rep(octv(M), 2, 6) + S("G5:0.5 F5 Eb5 D5 C5 Bb4 A4 G4 A4 Bb4 C5 D5", t=12, vel=0.8) + at(octv(M), 18) + S("D6:0.5 C6 Bb5 A5 G5 F5 Eb5 D5 C5 Bb4 A4 G4", t=24, vel=0.82)
    g8_rh += [(n, 30 + i * 0.22, 7, "R", 0.88) for i, n in enumerate(["G2", "D3", "G3", "Bb3", "D4", "G4", "Bb4", "D5", "G5"])]
    g8_lh = S("G2+G3:3 D3+G3+Bb3:3 F2+F3:3 D3+G3+Bb3:3 Eb2+Eb3:3 Bb2+Eb3+G3:3 D2+D3:3 A2+D3+F#3:3 G2+G3:3 D3+G3+Bb3:3", hand="L", vel=0.6)
    grades("b1-grades-carol", "Carol of the Bells", [
        (1, g1_rh, g1_lh, 300, "Melody + one bass note"),
        (5, g5_rh, g5_lh, 330, "Moving bass + harmony"),
        (8, g8_rh, g8_lh, 360, "Octaves, bell runs, big chords"),
    ], form=("Leontovych", "Carol of the Bells"))

# ---------- B2: Happy Birthday grades ----------
if want("b2"):
    first = [s for s in HB_RH if s[1] < 24]
    g1_lh = S("r:2 C3:6 G2:6 G2:6 C3:4", hand="L", vel=0.42)
    VO = {"C": ("C3", "E3+G3"), "G": ("G2", "B2+F3"), "G7": ("G2", "B2+F3"), "F": ("F2", "A3+C4"), "C7": ("C3", "E3+Bb3")}
    g5_lh = []
    for (t0, h) in [(2, "C"), (8, "G"), (14, "G7"), (20, "C")]:
        b, c = VO[h]
        g5_lh += S(f"{b}:2 {c}:2 {c}:2", t=t0, hand="L", vel=0.42)
    second = at([s for s in HB_RH if s[1] >= 24 and s[1] < 44], -24)
    g8_rh = octv(second) + S("C5:0.25 D5 E5 F5 G5 A5 B5 C6", t=20, vel=0.8)
    g8_rh += [(n, 22 + i * 0.25, 6, "R", 0.88) for i, n in enumerate(["C2", "G2", "C3", "E3", "G3", "C4", "E4", "G4", "C5", "E5", "G5", "C6"])]
    g8_lh = []
    for (t0, b) in [(2, ("C3", "G3", "E4", "C4", "G3", "C4")), (8, ("F2", "C3", "A3", "F3", "C3", "A3")), (14, ("C3", "G3", "E4", "G3", "G2", "D3"))]:
        g8_lh += S(" ".join(f"{n}:1" for n in b), t=t0, hand="L", vel=0.55)
    g8_lh += S("G2+G3:0.5 r:0.5 G2+F3+B3:1", t=0, hand="L", vel=0.5)
    grades("b2-grades-birthday", "Happy Birthday", [
        (1, first, g1_lh, 240, "Just the tune"),
        (5, first, g5_lh, 260, "Waltz left hand"),
        (8, g8_rh, g8_lh, 250, "Octaves, runs, big finish"),
    ], form=("Mildred & Patty Hill", "Happy Birthday"))

# ---------- B3: Moonlight grades ----------
if want("b3"):
    rh1, lh1 = ML1(2, mel=False)
    rh1 = cut(rh1, 18)
    lh1 = [("C#3", 0, 12, "L", 0.45), ("B2", 12, 6, "L", 0.45)]
    rh5, lh5 = ML1(5, mel=True)
    rh5 = at([s for s in rh5 if s[1] >= 36], -36)
    lh5 = at([s for s in lh5 if s[1] >= 36], -36)
    rh8 = ML3_RH + [(n, 32 + i * 0.3, 10, "R", 0.9) for i, n in enumerate(["C#2", "G#2", "C#3", "E3", "G#3", "C#4", "E4", "G#4", "C#5"])]
    lh8 = ML3_LH
    grades("b3-grades-moonlight", "Moonlight Sonata", [
        (1, rh1, lh1, 180, "Right-hand pattern + one bass note"),
        (5, rh5, lh5, 200, "Octave bass + the melody"),
        (8, rh8, lh8, 600, "…the 3rd movement 😳"),
    ], form=("Beethoven", "Moonlight Sonata"), hook_units=20)

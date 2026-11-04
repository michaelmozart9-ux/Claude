"""Public-domain pieces, arranged from memory (Michael: check every one by ear).
S("E5:1 D#5 E5 r:2 C4+E4+G4:4") -> [(note|[notes], beat, dur), ...]  sequential; ':n' sets duration (carries over); 'r' rest.
"""


def S(txt, t=0.0, hand=None, vel=None):
    out = []
    d = 1.0
    for tok in txt.split():
        if ":" in tok:
            nt, dd = tok.split(":")
            d = float(dd)
        else:
            nt = tok
        if nt != "r":
            notes = nt.split("+")
            item = [notes if len(notes) > 1 else notes[0], round(t, 4), d]
            if hand or vel is not None:
                item += [hand, vel]
            out.append(tuple(item))
        t += d
    return out


def at(seq, dt):
    return [tuple([s[0], round(s[1] + dt, 4)] + list(s[2:])) for s in seq]


def rep(seq, n, length):
    out = []
    for k in range(n):
        out += at(seq, k * length)
    return out


def span(seq):
    return max(s[1] + s[2] for s in seq)


# ---------------- Beethoven: Symphony No. 5 opening (unit 8th) ----------------
B5_RH = S("r:1 G4+G3:1 G4+G3 G4+G3 Eb4+Eb3:6 r:1 F4+F3:1 F4+F3 F4+F3 D4+D3:8")
B5_LH = S("r:1 G2:1 G2 G2 Eb2:6 r:1 F2:1 F2 F2 D2:8")
B5_BPM = 330

# ---------------- Grieg: In the Hall of the Mountain King (unit 8th) ----------------
MK_RH = S("B3:1 C#4 D4 E4 F#4 D4 F#4:2 E#4:1 C#4 E#4:2 E4:1 C4 E4:2 B3:1 C#4 D4 E4 F#4 D4 F#4 B4 A4 F#4 D4 F#4 A4:4")
MK_LH = S("B2:1 r F#2:1 r B2:1 r F#2:1 r C#3:1 r G#2:1 r C3:1 r G2:1 r B2:1 r F#2:1 r B2:1 r F#2:1 r F#2:1 r C#3:1 r F#2:2", hand="L", vel=0.5)
MK_BPM = 300

# ---------------- Wagner: Bridal Chorus (unit 16th) ----------------
BC_RH = S("C4:4 F4:3 F4:1 F4:8 C4:4 G4:3 E4:1 F4:8")
BC_LH = S("r:4 F3+A3:12 r:4 C3+Bb3:4 F3+A3:8", hand="L", vel=0.45)
BC_BPM = 300

# ---------------- Chopin: Funeral March, Sonata No. 2 (unit 16th) ----------------
FM_RH = S("Bb3:4 Bb3:3 Bb3:1 Bb3:4 Db4:3 C4:1 C4:3 Bb3:1 Bb3:3 A3:1 Bb3:8")
FM_LH = S("Bb2+F3:4 Gb2+Db3:4 Bb2+F3:4 Gb2+Db3:4 Bb2+F3:4 Gb2+Db3:4 Bb2+F3:8", hand="L", vel=0.55)
FM_BPM = 230

# ---------------- Beethoven: Für Elise (unit 16th) ----------------
FE_RH = S("E5:1 D#5 E5 D#5 E5 B4 D5 C5 A4:2 r:1 C4:1 E4 A4 B4:2 r:1 E4:1 G#4 B4 C5:2 r:1 E4:1 E5 D#5 E5 D#5 E5 B4 D5 C5 A4:2 r:1 C4:1 E4 A4 B4:2 r:1 E4:1 C5 B4 A4:4")
FE_LH = S("r:8 A2:1 E3 A3 r:3 E2:1 E3 G#3 r:3 A2:1 E3 A3 r:9 A2:1 E3 A3 r:3 E2:1 E3 G#3 r:3 A2:1 E3 A3", hand="L", vel=0.45)
FE_BPM = 270

# ---------------- Mozart: Rondo alla Turca (unit 16th) ----------------
TM_RH = S("B4:1 A4 G#4 A4 C5:2 r:2 D5:1 C5 B4 C5 E5:2 r:2 F5:1 E5 D#5 E5 B5 A5 G#5 A5 B5 A5 G#5 A5 C6:4 A5:2 C6:2 B5:2 A5:2 G5:2 A5:2 B5:2 A5:2 G5:2 A5:2 B5:2 A5:2 G5:2 F#5:2 E5:4")
TM_LH = S("r:4 A3:2 C4+E4:2 C4+E4:2 C4+E4:2 A3:2 C4+E4:2 C4+E4:2 C4+E4:2 A3:2 C4+E4:2 A3:2 C4+E4:2 A3:2 C4+E4:2 A3:2 C4+E4:2 E3:2 B3+E4:2 E3:2 B3+E4:2 E3:2 B3+E4:2 E3:2 B3+E4:2 E3:2 B3+E4:2 B2:2 B3+D#4:2 E3:4", hand="L", vel=0.42)
TM_BPM = 440

# ---------------- Bach: Toccata in D minor BWV 565 (unit 16th) ----------------
TO_RH = S("A5+A4:0.5 G5+G4:0.5 A5+A4:7 r:1 G5+G4:0.5 F5+F4:0.5 E5+E4:0.5 D5+D4:0.5 C#5+C#4:4 D5+D4:10")
TO_LH = S("A3+A2:0.5 G3+G2:0.5 A3+A2:7 r:1 G3+G2:0.5 F3+F2:0.5 E3+E2:0.5 D3+D2:0.5 C#3+C#2:4 D3+D2:10", hand="L", vel=0.6)
TO_BPM = 180

# ---------------- Joplin: The Entertainer (unit 16th), melody an octave down ----------------
EN_RH = S("D4:1 D#4 E4 C5:2 E4:1 C5:2 E4:1 C5:6 r:1 C5:1 D5 D#5 E5 C5 D5 E5:2 B4:1 D5:2 C5:6 r:2")
EN_LH = S("r:2 C3:2 E3+G3+C4:2 G2:2 E3+G3+C4:2 C3:2 E3+G3+C4:2 G2:2 E3+G3+C4:2 C3:2 E3+G3+C4:2 G2:2 G3+B3+F4:2 C3:2 E3+G3+C4:2 G2:2", hand="L", vel=0.45)
EN_BPM = 400

# ---------------- Christmas ----------------
JB_RH = S("E4:1 E4 E4:2 E4:1 E4 E4:2 E4:1 G4 C4:1.5 D4:0.5 E4:4 F4:1 F4 F4:1.5 F4:0.5 F4:1 E4 E4 E4:0.5 E4:0.5 E4:1 D4 D4 E4 D4:2 G4:2")
JB_LH = S("C3:2 G2:2 C3:2 G2:2 C3:2 G2:2 C3:2 E3:2 F2:2 C3:2 F2:2 C3:2 G2:2 D3:2 G2:4", hand="L", vel=0.42)
JB_BPM = 190

# Carol of the Bells (Leontovych), unit 8th, 3/4 bar = 6
COB_MOT = S("Bb4:2 A4:1 Bb4:1 G4:2")
COB_RH = rep(COB_MOT, 4, 6) + at(S("D5:2 C5:1 D5:1 Bb4:2"), 24) + at(S("D5:2 C5:1 D5:1 Bb4:2"), 30)
COB_LH = S("G3:6 G3:6 G3:6 G3:6 G3:6 G3:6", hand="L", vel=0.42)
COB_BPM = 330

# Silent Night (Gruber), unit 8th, 6/8, C major
SN_RH = S("G4:3 A4:1 G4:2 E4:6 G4:3 A4:1 G4:2 E4:6 D5:4 D5:2 B4:6 C5:4 C5:2 G4:6")
SN_CHORDS = [("C3", ["G3", "C4", "E4"]), ("C3", ["G3", "C4", "E4"]), ("C3", ["G3", "C4", "E4"]), ("C3", ["G3", "C4", "E4"]), ("G2", ["G3", "B3", "F4"]), ("G2", ["G3", "B3", "D4"]), ("C3", ["G3", "C4", "E4"]), ("C3", ["G3", "C4", "E4"])]
SN_BPM = 190

# We Wish You a Merry Christmas, unit 8th, 3/4
WW_RH = S("D4:2 G4:2 G4:1 A4 G4 F#4 E4:2 E4 E4 A4:2 A4:1 B4 A4 G4 F#4:2 D4 D4 B4:2 B4:1 C5 B4 A4 G4:2 E4 D4:1 D4 E4:2 A4 F#4 G4:4")
WW_LH = S("r:2 G2:6 C3:6 A2:6 D3:6 B2:6 E3:4 C3:2 D3:6 G2:4", hand="L", vel=0.42)
WW_BPM = 300

# ---------------- Happy Birthday (Hill), unit 8th, 3/4, C major ----------------
HB_RH = S("G4:1.5 G4:0.5 A4:2 G4:2 C5:2 B4:4 G4:1.5 G4:0.5 A4:2 G4:2 D5:2 C5:4 G4:1.5 G4:0.5 G5:2 E5:2 C5:2 B4:2 A4:2 F5:1.5 F5:0.5 E5:2 C5:2 D5:2 C5:6")
HB_HARM = [(2, "C"), (8, "G"), (14, "G7"), (20, "C"), (26, "F"), (32, "F"), (38, "C"), (42, "G7"), (44, "C")]
HB_BPM = 230

# ---------------- Beethoven: Moonlight Sonata ----------------
# 1st mvt, unit = triplet 8th (12 per bar)
def ML1(bars=4, mel=True):
    rh, lh = [], []
    figs = [[("G#3", "C#4", "E4")] * 4, [("G#3", "C#4", "E4")] * 4, [("A3", "C#4", "E4")] * 2 + [("A3", "D4", "F#4")] * 2,
            [("G#3", "B#3", "F#4"), ("G#3", "C#4", "E4"), ("G#3", "C#4", "D#4"), ("F#3", "B#3", "D#4")], [("G#3", "C#4", "E4")] * 4]
    bass = [[("C#2+C#3", 12)], [("B1+B2", 12)], [("A1+A2", 6), ("F#1+F#2", 6)], [("G#1+G#2", 12)], [("C#2+C#3", 12)]]
    for b in range(bars):
        f = figs[b % len(figs)]
        for q in range(4):
            for k in range(3):
                rh.append((f[q][k], b * 12 + q * 3 + k, 1))
        t = b * 12
        for nn, d in bass[b % len(bass)]:
            lh.append((nn.split("+"), t, d, "L", 0.5))
            t += d
    if mel and bars >= 5:
        rh += [("G#4", 4 * 12 + 9, 2.25, "B", 0.78), ("G#4", 4 * 12 + 11.25, 0.75, "B", 0.72)]
    return rh, lh
ML1_BPM = 160

# 3rd mvt opening, unit 16th
ML3_RH = S("r:1 G#3:1 C#4 E4 G#4 C#5 E5 G#5 C#6 r:3 E5+G#5+C#6:2 E5+G#5+C#6:2 r:1 G#3:1 B#3 D#4 F#4 G#4 B#4 D#5 F#5 r:3 D#5+F#5+G#5:2 D#5+F#5+G#5:2")
ML3_LH = S("C#2+C#3:2 C#2+C#3 C#2+C#3 C#2+C#3 C#2+C#3 C#2+C#3 C#2+C#3 C#2+C#3 B#1+B#2:2 B#1+B#2 B#1+B#2 B#1+B#2 B#1+B#2 B#1+B#2 G#1+G#2 G#1+G#2", hand="L", vel=0.55)
ML3_BPM = 600

# ---------------- Satie: Gymnopédie No. 1, unit quarter, 3/4 ----------------
def GYM(bars=8):
    lh = []
    for b in range(bars):
        t = b * 3
        if b % 2 == 0:
            lh += [("G2", t, 3, "L", 0.45), (["B3", "D4", "F#4"], t + 1, 2, "L", 0.36)]
        else:
            lh += [("D2", t, 3, "L", 0.45), (["A3", "C#4", "F#4"], t + 1, 2, "L", 0.36)]
    rh = S("r:7 F#5:1 A5 G5 F#5 C#5 B4 C#5 D5 A4:3 F#4:3 F#4:3 F#4:3", vel=0.62)
    return rh, lh
GYM_BPM = 78

# ---------------- Bach: Prelude in C BWV 846, unit 16th ----------------
BP_BARS = [("C4", "E4", "G4", "C5", "E5"), ("C4", "D4", "A4", "D5", "F5"), ("B3", "D4", "G4", "D5", "F5"), ("C4", "E4", "G4", "C5", "E5"),
           ("C4", "E4", "A4", "E5", "A5"), ("C4", "D4", "F#4", "A4", "D5"), ("B3", "D4", "G4", "D5", "G5"), ("B3", "C4", "E4", "G4", "C5"),
           ("A3", "C4", "E4", "G4", "C5"), ("D3", "A3", "D4", "F#4", "C5"), ("G3", "B3", "D4", "G4", "B4")]
def BACHC(bars=4, start=0, rh_vel=0.58):
    rh, lh = [], []
    for b in range(bars):
        n = BP_BARS[(start + b) % len(BP_BARS)]
        for half in range(2):
            t = b * 16 + half * 8
            lh += [(n[0], t, 8, "L", 0.5), (n[1], t + 1, 7, "L", 0.45)]
            for k, nn in enumerate([n[2], n[3], n[4], n[2], n[3], n[4]]):
                rh.append((nn, t + 2 + k, 1, "R", rh_vel))
    return rh, lh
BACHC_BPM = 300

# ---------------- Pachelbel: Canon in D, unit 8th ----------------
CANON_PROG = [("D2", ["F#3", "A3", "D4"]), ("A1", ["E3", "A3", "C#4"]), ("B1", ["F#3", "B3", "D4"]), ("F#1", ["F#3", "A3", "C#4"]),
              ("G1", ["G3", "B3", "D4"]), ("D2", ["F#3", "A3", "D4"]), ("G1", ["G3", "B3", "D4"]), ("A1", ["E3", "A3", "C#4"])]
def CANON(cycles=1, melody=True, mel_line=1):
    lh, rh = [], []
    for c in range(cycles):
        for i, (b, ch) in enumerate(CANON_PROG):
            t = (c * 8 + i) * 4
            lh.append(([b, b.replace("1", "2")] if b.endswith("1") else [b], t, 4, "L", 0.5))
            for k, nn in enumerate([ch[0], ch[1], ch[2], ch[1]]):
                lh.append((nn, t + k, 1, "L", 0.36))
    if melody:
        line = ["F#5", "E5", "D5", "C#5", "B4", "A4", "B4", "C#5"] if mel_line == 1 else ["D5", "C#5", "B4", "A4", "G4", "F#4", "G4", "E4"]
        for c in range(cycles):
            for i, nn in enumerate(line):
                rh.append((nn, (c * 8 + i) * 4, 4, "R", 0.62))
    return rh, lh
CANON_BPM = 128

# ---------------- Brahms: Lullaby, unit 8th, 3/4, C major ----------------
BL_RH = S("E4:1 E4 G4:4 E4:1 E4 G4:4 E4:1 G4 C5:2 B4:3 A4:1 A4:2 G4:2 D4:1 E4 F4:2 D4:2 D4:1 E4 F4:4 D4:1 F4 B4:1 A4 G4:2 B4:2 C5:6", vel=0.6)
BL_LH = S("r:2 C3+G3:6 C3+G3:6 F2+C3+A3:6 C3+G3+E3:6 G2+F3+B3:6 G2+F3+B3:6 G2+D3+B3:6 C3+G3+E3:6", hand="L", vel=0.36)
BL_BPM = 170

# ---------------- Mozart: Sonata K. 545, unit 16th ----------------
K545_RH = S("C5:8 E5:4 G5:4 B4:6 C5:1 D5:1 C5:8 A5:8 G5:4 C6:4 G5:4 F5:2 E5:2 F5:2 E5:6")
def K545_LH():
    pat = {"C": ("C3", "G3", "E3", "G3"), "G7": ("D3", "G3", "F3", "G3"), "F": ("C3", "A3", "F3", "A3")}
    harm = ["C", "C", "G7", "C", "F", "C", "G7", "C"]
    out = []
    for i, h in enumerate(harm):
        for k in range(8):
            out.append((pat[h][k % 4], i * 8 + k, 1, "L", 0.4))
    return out
K545_BPM = 500

# ---------------- Petzold: Minuet in G, unit 8th, 3/4 ----------------
MG_RH = S("D5:2 G4:1 A4 B4 C5 D5:2 G4:2 G4:2 E5:2 C5:1 D5 E5 F#5 G5:2 G4:2 G4:2 C5:2 D5:1 C5 B4 A4 B4:2 C5:1 B4 A4 G4 F#4:2 G4:1 A4 B4 G4 A4:6")
MG_LH = S("G3+B3:4 A3:2 B3:6 C4:6 B3:6 A3:6 G3:6 D4:2 B3:2 G3:2 D4:2 D3:2 C4:2", hand="L", vel=0.42)
MG_BPM = 280

# ---------------- Hanon No. 1 (unit 16th) ----------------
def HANON(steps=8, base=60, down=False):
    scale = [0, 2, 4, 5, 7, 9, 11]
    def deg(d):
        return base + 12 * (d // 7) + scale[d % 7]
    rh, lh = [], []
    t = 0
    for k in range(steps):
        pat = [k, k + 2, k + 3, k + 4, k + 5, k + 4, k + 3, k + 2]
        for d in pat:
            rh.append((deg(d), t, 1, "R", 0.66))
            lh.append((deg(d) - 12, t, 1, "L", 0.55))
            t += 1
    return rh, lh

# ---------------- Rimsky-Korsakov: Flight of the Bumblebee (unit 16th), an octave down ----------------
BB_RUN = S("E5:1 D#5 D5 C#5 D5 C#5 C5 B4 C5 B4 A#4 A4 G#4 G4 F#4 F4 E4 D#4 D4 C#4 D4 C#4 C4 B3 C4 C#4 D4 D#4 E4 F4 E4 D#4")
BB_LH = S("A2:4 A2:4 A2:4 A2:4 E2:4 E2:4 A2:8", hand="L", vel=0.45)
BB_BPM = 640

"""Pieces (public domain, arranged from memory) + grade arrangements.
Notes are (midi, beat, dur_beats, hand, vel). Melody text format: 'E4/1 r/.5 D#5/.25 ...' ('|' ignored)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from plib import P

def seq(s, start=0.0):
    out, b = [], start
    for tok in s.replace("|", " ").split():
        n, d = tok.split("/"); d = float(d)
        if n != "r": out.append((n, b, d))
        b += d
    return out

def chords(s, start=0.0):
    out, b = [], start
    for tok in s.replace("|", " ").split():
        c, d = tok.split("/"); d = float(d); out.append((b, c, d)); b += d
    return out

PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
QUAL = {"": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "m7": [0, 3, 7, 10], "maj7": [0, 4, 7, 11], "dim": [0, 3, 6], "5": [0, 7], "sus4": [0, 5, 7]}
def parse(sym):
    r = PC[sym[0]]; q = sym[1:]
    if q[:1] == "#": r += 1; q = q[1:]
    elif q[:1] == "b": r -= 1; q = q[1:]
    return r % 12, QUAL[q]
def near(pc, lo):  # lowest midi >= lo with pitch class pc
    m = lo + ((pc - lo) % 12); return m

SCALES = {"maj": [0, 2, 4, 5, 7, 9, 11], "min": [0, 2, 3, 5, 7, 8, 11]}

# ---------------------------------------------------------------- pieces
PIECES = {}
def piece(pid, **kw):
    kw["mel"] = seq(kw["mel"], kw.get("start", 0.0)); kw["ch"] = chords(kw["ch"], kw.get("start", 0.0))
    kw.setdefault("bpb", 4); kw.setdefault("short", kw["name"]); kw.setdefault("lh5", None); kw.setdefault("lh8", "stride")
    PIECES[pid] = kw

piece("ode", name="Ode to Joy", composer="Beethoven", key=("C", "maj"), bpm=(120, 132, 144),
      mel="E4/1 E4/1 F4/1 G4/1 | G4/1 F4/1 E4/1 D4/1 | C4/1 C4/1 D4/1 E4/1 | D4/1.5 C4/.5 C4/2",
      ch="C/4 G/4 C/4 G/2 C/2", cut=8)
piece("elise", name="Für Elise", composer="Beethoven", key=("A", "min"), bpb=3, bpm=(118, 132, 140), lh5="fe", lh8="sweep", up=0,
      mel="E5/.5 D#5/.5 | E5/.5 D#5/.5 E5/.5 B4/.5 D5/.5 C5/.5 | A4/1 r/.5 C4/.5 E4/.5 A4/.5 | B4/1 r/.5 E4/.5 C5/.5 B4/.5 | A4/3",
      ch="N/4 Am/3 E/3 Am/3", cut=None)
piece("canon", name="Canon in D", composer="Pachelbel", key=("D", "maj"), bpm=(66, 72, 76), up=0,
      mel="F#5/1 E5/1 D5/1 C#5/1 | B4/1 A4/1 B4/1 C#5/1 | D5/2",
      ch="D/1 A/1 Bm/1 F#m/1 G/1 D/1 G/1 A/1 D/2", cut=None, lh5="broken")
piece("twinkle", name="Twinkle Twinkle", composer="Traditional", key=("C", "maj"), bpm=(132, 144, 152),
      mel="C4/1 C4/1 G4/1 G4/1 | A4/1 A4/1 G4/2 | F4/1 F4/1 E4/1 E4/1 | D4/1 D4/1 C4/2",
      ch="C/4 F/2 C/2 F/2 C/2 G7/2 C/2", cut=8)
piece("mountain", name="In the Hall of the Mountain King", short="Mountain King", composer="Grieg", key=("B", "min"), bpm=(104, 132, 168),
      mel="B3/.5 C#4/.5 D4/.5 E4/.5 F#4/.5 D4/.5 F#4/1 | E#4/.5 C#4/.5 E#4/1 E4/.5 C4/.5 E4/1 | B3/.5 C#4/.5 D4/.5 E4/.5 F#4/.5 D4/.5 F#4/.5 B4/.5 | A4/.5 F#4/.5 D4/.5 F#4/.5 A4/2 | B4/2",
      ch="B5/4 F#5/4 B5/4 F#5/4 B5/2", cut=8, up=12)
piece("nacht", name="Eine kleine Nachtmusik", short="Eine kleine", composer="Mozart", key=("G", "maj"), bpm=(120, 132, 144),
      mel="G4/1 r/.5 D4/.5 G4/1 r/.5 D4/.5 | G4/.5 D4/.5 G4/.5 B4/.5 D5/2 | C5/1 r/.5 A4/.5 C5/1 r/.5 A4/.5 | C5/.5 A4/.5 F#4/.5 A4/.5 D4/2 | G4/2",
      ch="G/8 D/8 G/2", cut=8)
piece("minuet", name="Minuet in G", composer="Petzold (attr. Bach)", key=("G", "maj"), bpb=3, bpm=(126, 138, 150), up=0,
      mel="D5/1 G4/.5 A4/.5 B4/.5 C5/.5 | D5/1 G4/1 G4/1 | E5/1 C5/.5 D5/.5 E5/.5 F#5/.5 | G5/1 G4/1 G4/1",
      ch="G/3 G/3 C/3 G/3", cut=6)
piece("entertainer", name="The Entertainer", composer="Joplin", key=("C", "maj"), bpm=(112, 126, 138), up=0, lh8="stride",
      mel="D4/.5 D#4/.5 | E4/.5 C5/1 E4/.5 C5/1 E4/.5 C5/2.5 | C5/.5 D5/.5 D#5/.5 E5/.5 C5/.5 D5/.5 E5/1 B4/.5 D5/1 | C5/3",
      ch="N/1 C/4 C/4 C/2 G7/1.5 C/3.5", cut=None)
piece("greensleeves", name="Greensleeves", composer="Traditional", key=("A", "min"), bpb=3, bpm=(150, 162, 174), up=0,
      mel="A4/1 | C5/2 D5/1 | E5/1.5 F5/.5 E5/1 | D5/2 B4/1 | G4/1.5 A4/.5 B4/1 | C5/2 A4/1 | A4/1.5 G#4/.5 A4/1 | B4/2 G#4/1 | E4/3",
      ch="N/1 Am/3 G/3 F/3 E/3 Am/3 E/3 E/3 E/3", cut=16, gcut=16)
piece("brahms", name="Brahms' Lullaby", short="Brahms' Lullaby", composer="Brahms", key=("C", "maj"), bpb=3, bpm=(120, 132, 140),
      mel="E4/.5 E4/.5 | G4/2 E4/.5 E4/.5 | G4/2 E4/.5 G4/.5 | C5/1 B4/1.5 A4/.5 | A4/1 G4/1 D4/.5 E4/.5 | F4/1 D4/1 D4/.5 E4/.5 | F4/2 D4/.5 F4/.5 | B4/.5 A4/.5 G4/1 B4/1 | C5/3",
      ch="N/1 C/3 C/3 C/3 G/3 G7/3 G7/3 G7/3 C/3", cut=12, gcut=12, up=12)
piece("largo", name="New World Largo", composer="Dvořák", key=("C", "maj"), bpm=(100, 108, 116),
      mel="E4/1.5 G4/.5 G4/2 | E4/1.5 D4/.5 C4/2 | D4/1 E4/1 G4/1 E4/1 | D4/2 r/1 | C4/3",
      ch="C/8 G/4 G/3 C/3", cut=None, gcut=15)
piece("turkish", name="Turkish March", composer="Mozart", key=("A", "min"), bpm=(100, 112, 120), up=0, lh5="alb8",
      mel="B4/.25 A4/.25 G#4/.25 A4/.25 C5/1 | D5/.25 C5/.25 B4/.25 C5/.25 E5/1 | F5/.25 E5/.25 D#5/.25 E5/.25 B5/.25 A5/.25 G#5/.25 A5/.25 | B5/.25 A5/.25 G#5/.25 A5/.25 C6/1 | A5/2",
      ch="Am/2 Am/2 Am/2 E/2 Am/2", cut=None)
piece("gymno", name="Gymnopédie No. 1", short="Gymnopédie", composer="Satie", key=("D", "maj"), bpb=3, bpm=(88, 96, 104), up=0, lh5="gym", lh8="sweep",
      mel="r/1 F#5/1 A5/1 | G5/1 F#5/1 C#5/1 | B4/1 C#5/1 D5/1 | A4/3",
      ch="Gmaj7/3 Dmaj7/3 Gmaj7/3 Dmaj7/3", cut=None)
piece("silent", name="Silent Night", composer="Gruber", key=("C", "maj"), bpb=3, bpm=(132, 144, 152), up=12, snow=True,
      mel="G4/1.5 A4/.5 G4/1 | E4/3 | G4/1.5 A4/.5 G4/1 | E4/3 | D5/2 D5/1 | B4/3 | C5/2 C5/1 | G4/3",
      ch="C/12 G7/6 C/6", cut=12, gcut=12)
piece("deck", name="Deck the Halls", composer="Traditional", key=("C", "maj"), bpm=(120, 132, 144), up=12, snow=True,
      mel="G4/1.5 F4/.5 E4/1 D4/1 | C4/1 D4/1 E4/1 C4/1 | D4/.5 E4/.5 F4/.5 D4/.5 E4/1.5 D4/.5 | C4/1 B3/1 C4/2",
      ch="C/4 C/4 G7/2 C/2 G7/2 C/2", cut=8)
piece("wewish", name="We Wish You a Merry Christmas", short="We Wish You", composer="Traditional", key=("C", "maj"), bpb=3, bpm=(138, 150, 160), up=0, snow=True,
      mel="G4/1 | C5/1 C5/.5 D5/.5 C5/.5 B4/.5 | A4/1 A4/1 A4/1 | D5/1 D5/.5 E5/.5 D5/.5 C5/.5 | B4/1 G4/1 G4/1 | E5/1 E5/.5 F5/.5 E5/.5 D5/.5 | C5/1 A4/1 G4/.5 G4/.5 | A4/1 D5/1 B4/1 | C5/3",
      ch="N/1 C/3 F/3 D7/3 G/3 E7/3 Am/3 F/1 G7/2 C/3", cut=13, gcut=13)
piece("jingle", name="Jingle Bells", composer="Pierpont", key=("C", "maj"), bpm=(132, 144, 156), up=12, snow=True,
      mel="E4/1 E4/1 E4/2 | E4/1 E4/1 E4/2 | E4/1 G4/1 C4/1.5 D4/.5 | E4/4",
      ch="C/8 C/2 G7/2 C/4", cut=None)
piece("carol", name="Carol of the Bells", composer="Leontovych", key=("G", "min"), bpb=3, bpm=(144, 160, 172), up=0, snow=True,
      mel="Bb4/1 A4/.5 Bb4/.5 G4/1 | Bb4/1 A4/.5 Bb4/.5 G4/1 | Bb4/1 A4/.5 Bb4/.5 G4/1 | Bb4/1 A4/.5 Bb4/.5 G4/1 | D5/1 C5/.5 D5/.5 Bb4/1 | D5/1 C5/.5 D5/.5 Bb4/1 | G4/3",
      ch="Gm/3 F/3 Eb/3 D/3 Gm/3 F/3 Gm/3", cut=None)
piece("chopsticks", name="Chopsticks", composer="Euphemia Allen", key=("C", "maj"), bpb=3, bpm=(150, 162, 176), up=0, dyad=True,
      mel="G4/1 G4/1 G4/1 G4/1 G4/1 G4/1 | G4/1 G4/1 G4/1 G4/1 G4/1 G4/1 | B4/1 B4/1 B4/1 B4/1 C5/1 B4/1 | A4/1 B4/1 C5/3",
      ch="G7/6 C/6 G7/6 G7/3 C/3", cut=None)
piece("amazing", name="Amazing Grace", composer="Traditional", key=("G", "maj"), bpb=3, bpm=(108, 120, 132), up=12,
      mel="D4/1 | G4/2 B4/.5 G4/.5 | B4/2 A4/1 | G4/2 E4/1 | D4/2 D4/1 | G4/2 B4/.5 G4/.5 | B4/2 A4/1 | D5/3",
      ch="N/1 G/3 G/3 C/3 G/3 G/3 Em/3 D/3", cut=13, gcut=13)
# guess-the-song extras
piece("beet5", name="Beethoven's 5th", composer="Beethoven", key=("C", "min"), bpm=(108, 108, 108), up=0, unison=True,
      mel="r/.5 G4/.5 G4/.5 G4/.5 | Eb4/3 | r/.5 F4/.5 F4/.5 F4/.5 | D4/3.5",
      ch="Cm/4 G/4.5", cut=None)
piece("toccata", name="Toccata in D minor", composer="Bach", key=("D", "min"), bpm=(80, 80, 80), up=0, unison=True,
      mel="A5/.125 G5/.125 A5/1.5 r/.5 G5/.25 F5/.25 E5/.25 D5/.25 C#5/.75 D5/2",
      ch="Dm/6", cut=None)
piece("spring", name="Spring (Four Seasons)", short="Vivaldi's Spring", composer="Vivaldi", key=("E", "maj"), bpm=(100, 108, 112), up=12,
      mel="E4/.5 G#4/.5 G#4/.5 G#4/.5 F#4/.25 E4/.25 B4/1.5 | B4/.25 A4/.25 G#4/.5 G#4/.5 G#4/.5 F#4/.25 E4/.25 B4/1.5",
      ch="E/4 E/4", cut=None)
piece("joy", name="Joy to the World", composer="Handel / Mason", key=("C", "maj"), bpm=(96, 104, 112), up=12, snow=True,
      mel="C5/1 B4/.75 A4/.25 G4/1.5 F4/.5 | E4/1 D4/1 C4/2",
      ch="C/2 C/1.5 G7/.5 C/1 G/1 C/2", cut=None)
# texture pieces (custom note generators)
piece("moonlight", name="Moonlight Sonata", composer="Beethoven", key=("C#", "min"), bpm=(60, 60, 60), mel="C#4/1", ch="C#m/1", texture="moonlight")
piece("prelude", name="Prelude in C", composer="Bach", key=("C", "maj"), bpm=(72, 72, 72), mel="C4/1", ch="C/1", texture="prelude")

def moonlight(bars=(1, 2, 3, 4)):
    B = {1: ([("C#2", 4), ("C#3", 4)], [["G#3", "C#4", "E4"]] * 4),
         2: ([("B2", 4)], [["G#3", "C#4", "E4"]] * 4),
         3: ([("A2", 2), ("F#2", 2)], [["A3", "C#4", "E4"]] * 2 + [["A3", "D4", "F#4"]] * 2),
         4: ([("G#2", 4)], [["G#3", "C4", "F#4"]] * 2 + [["G#3", "C#4", "E4"], ["F#3", "C4", "D#4"]]),
         5: ([("C#2", 4), ("C#3", 4)], [["G#3", "C#4", "E4"]] * 4)}
    out, b0, spans = [], 0.0, []
    for bar in bars:
        bass, trip = B[bar]; bb = b0
        if bar == 3: out += [(P("A2"), b0, 2, "L", .55), (P("F#2"), b0 + 2, 2, "L", .55)]; spans += [(b0, b0 + 2), (b0 + 2, b0 + 4)]
        else: out += [(P(n), b0, d, "L", .55) for n, d in bass]; spans += [(b0, b0 + 4)]
        for g, tri in enumerate(trip):
            for j, n in enumerate(tri): out.append((P(n), b0 + g + j / 3, 1 / 3, "R", .5 if j else .56))
        b0 += 4
    return out, spans, b0

def prelude(bars=(1, 2, 3, 4)):
    B = {1: "C4 E4 G4 C5 E5", 2: "C4 D4 A4 D5 F5", 3: "B3 D4 G4 D5 F5", 4: "C4 E4 G4 C5 E5", 5: "C4 E4 A4 E5 A5", 6: "C4 D4 F#4 A4 D5", 7: "B3 D4 G4 D5 G5", 8: "B3 C4 E4 G4 C5"}
    out, b0, spans = [], 0.0, []
    for bar in bars:
        a, b, r1, r2, r3 = [P(x) for x in B[bar].split()]
        for h in (0, 2):
            s = b0 + h; out += [(a, s, 2, "L", .5), (b, s + .25, 1.75, "L", .44)]
            for j, m in enumerate([r1, r2, r3, r1, r2, r3]): out.append((m, s + .5 + j * .25, .25, "R", .5 + (.06 if j in (0, 3) else 0)))
        spans += [(b0, b0 + 4)]; b0 += 4
    return out, spans, b0

# ---------------------------------------------------------------- arranging helpers
def chord_at(p, b):
    for cb, c, d in p["ch"]:
        if cb - 1e-6 <= b < cb + d - 1e-6: return c
    return "N"
def tones(sym, lo):
    r, iv = parse(sym); root = near(r, lo); return [root + i for i in iv]
def step(p, m, k):
    t, mode = p["key"]; tp = PC[t[0]] + (1 if t[1:] == "#" else -1 if t[1:] == "b" else 0); sc = SCALES[mode]
    rel = (m - tp) % 12; base = m - rel
    i = max(j for j in range(7) if sc[j] <= rel); i += k; o, i = divmod(i, 7)
    return base + 12 * o + sc[i]
def tonic(p):
    t, mode = p["key"]; tp = PC[t[0]] + (1 if t[1:] == "#" else -1 if t[1:] == "b" else 0); return tp % 12, ([0, 4, 7] if mode == "maj" else [0, 3, 7])
def fit(ns):  # keep notes inside keyboard C2..C6
    out = []
    for m, b, d, h, v in ns:
        while m > 84: m -= 12
        while m < 36: m += 12
        out.append((m, b, d, h, v))
    return out
def up_of(p):
    if "up" in p: return p["up"]
    return 12 if max(P(n) for n, _, _ in p["mel"]) <= 72 else 0
def mel_end(p): return max(b + d for _, b, d in p["mel"])

def truncate(p, cut):
    if not cut: return p
    q = dict(p); mel = [(n, b, d) for n, b, d in p["mel"] if b < cut]
    n, b, d = mel[-1]; mel[-1] = (n, b, max(d, cut - b, 2.0)); q["mel"] = mel
    end = mel[-1][1] + mel[-1][2]
    q["ch"] = [(cb, c, min(d, end - cb)) for cb, c, d in p["ch"] if cb < end]
    return q

def lh_pattern(p, kind, vel=.46):
    out = []
    for cb, sym, d in p["ch"]:
        if sym == "N": continue
        r, iv = parse(sym); root = near(r, 43)
        T = [root + i for i in iv[:3]] + [root + 12]
        if len(iv) == 2: T = [root, root + 7, root + 12, root + 19]
        if len(iv) == 4 and kind != "gym": T = [root, root + iv[1], root + iv[3], root + 12]
        if kind == "block": out += [(m, cb, d, "L", vel) for m in T[:3]]
        elif kind in ("alberti", "alb8", "broken", "fe"):
            pat = {"alberti": [0, 2, 1, 2], "alb8": [0, 2, 1, 2], "broken": [0, 2, 3, 2], "fe": [0, 2, 3]}[kind]
            stp = .25 if kind == "alb8" else .5; nsteps = int(round(d / stp)) if kind != "fe" else 3
            for j in range(nsteps): out.append((T[pat[j % len(pat)]], cb + j * stp, stp, "L", vel + (.08 if j % len(pat) == 0 else 0)))
        elif kind == "waltz":
            bpb = p["bpb"]
            for j in range(int(round(d))):
                if j % bpb == 0: out.append((root - 12 if root - 12 >= 36 else root, cb + j, 1, "L", vel + .1))
                else: out += [(m, cb + j, .9, "L", vel - .06) for m in T[1:3] + [T[3]]]
        elif kind == "gym":
            bass = near(r, 38); up_t = sorted(near((r + i) % 12, 57) for i in iv[1:])
            out.append((bass, cb, d, "L", vel + .08)); out += [(m, cb + 1, d - 1, "L", vel - .04) for m in up_t]
        elif kind == "sweep" or kind == "sweep16":
            stp = .25 if kind == "sweep16" else .5; low = near(r, 36)
            arp = [low, low + 7, low + 12, low + iv[1] + 12, low + 19, low + 24]
            arp = arp + arp[-2:0:-1]; nsteps = int(round(d / stp))
            for j in range(nsteps): out.append((arp[j % len(arp)], cb + j * stp, stp * (2 if j == 0 else 1), "L", vel + (.12 if j == 0 else 0)))
        elif kind == "stride":
            bpb = p["bpb"]; lowr = near(r, 36)
            mid = sorted(near((r + i) % 12, 52) for i in iv[:3])
            for j in range(int(round(d))):
                bb = cb + j
                if (bb % bpb) in ((0, 2) if bpb == 4 else (0,)): out += [(lowr, bb, .9, "L", vel + .16), (lowr + 12, bb, .9, "L", vel + .1)]
                else: out += [(m, bb, .8, "L", vel - .02) for m in mid]
            if d % 1: pass
    return out

def harmony(p, mel_notes, vel=.46):
    out = []; bpb = p["bpb"]
    for m, b, d, h, v in mel_notes:
        strong = abs(b % (2 if bpb == 4 else bpb)) < 1e-6
        sym = chord_at(p, b)
        if not strong or d < .5 or sym == "N": continue
        r, iv = parse(sym); pcs = {(r + i) % 12 for i in iv}
        for k in range(3, 10):
            if (m - k) % 12 in pcs: out.append((m - k, b, d, "R", vel)); break
    return out

# ---------------------------------------------------------------- grade arrangements -> (notes, end_beat, final_chord_beat or None)
def g1(p, vel=.66):
    sh = 0; mel = [(P(n) + sh, b, d, "R", vel) for n, b, d in p["mel"]]
    lh = [(near(parse(c)[0], 43), cb, d, "L", .5) for cb, c, d in p["ch"] if c != "N"]
    if p.get("unison"): lh = [(m - 12, b, d, "L", .5) for m, b, d, h, v in mel]
    if p.get("dyad"): mel += [(m - 2 if m % 12 == 7 else m - 3 if m % 12 == 11 else m - 12, b, d, "R", vel - .1) for m, b, d, h, v in mel]
    return fit(mel + lh), mel_end(p)

def g5(p, lh=None):
    up = up_of(p); mel = [(P(n) + up, b, d, "R", .72) for n, b, d in p["mel"]]
    if p.get("unison"): return fit(mel + [(m - 12, b, d, "R", .55) for m, b, d, h, v in mel] + [(m - 24, b, d, "L", .55) for m, b, d, h, v in mel]), mel_end(p)
    if p.get("dyad"): return g1(p, .7)[0] + fit([(near(parse(c)[0], 43), cb, d, "L", .5) for cb, c, d in p["ch"]]), mel_end(p)
    kind = lh or p["lh5"] or ("broken" if p["bpb"] == 3 else "alberti")
    return fit(mel + harmony(p, mel) + lh_pattern(p, kind)), mel_end(p)

def ending(p, last_m, b0, vel=.8):
    """run up from the last melody note into a rolled tonic chord at b0+2. returns notes, chord_beat"""
    tp, iv = tonic(p); out = []
    cand = sorted({near((tp + i) % 12, 48) + 12 * o for i in iv for o in range(4)})
    start = max(48, last_m - 12); run = [m for m in cand if start <= m <= 84][:8]
    for j, m in enumerate(run): out.append((m, b0 + j * 2 / len(run), 2 / len(run), "R", .5 + .35 * j / len(run)))
    cb = b0 + 2; low = near(tp, 36)
    for j, m in enumerate([low, low + 7, low + 12, low + 12 + iv[1]]): out.append((m, cb + j * .06, 6, "L", .78))
    top = [m for m in sorted({near((tp + i) % 12, 67) + 12 * o for i in iv for o in range(2)}) if m <= 84][:5]
    for j, m in enumerate(top): out.append((m, cb + .2 + j * .055, 6, "R", .72 + .03 * j))
    return out, cb

def g8(p, with_end=True, lh=None):
    up = up_of(p); mel = [(P(n) + up, b, d) for n, b, d in p["mel"]]
    if p.get("unison"):
        ns = [(m, b, d, "R", .85) for m, b, d in mel] + [(m - 12, b, d, "R", .7) for m, b, d in mel] + [(m - 24, b, d, "L", .75) for m, b, d in mel] + [(m - 36, b, d, "L", .6) for m, b, d in mel]
        return fit(ns), mel_end(p), None
    med = sorted(d for _, _, d in mel)[len(mel) // 2]
    mode = "fig" if med >= 1 else "oct"
    body = mel[:-1] if with_end else mel; out = []
    for m, b, d in body:
        if mode == "fig" and d >= 1:
            figs = ([0, 1, 0, -1, -2, -1, 0, 1] * 4)[: int(round(d / .25))]
            for j, k in enumerate(figs): out.append((step(p, m, k), b + j * .25, .25, "R", .84 if j % 4 == 0 else .5))
        else:
            out.append((m, b, d, "R", .82))
            if (d >= .5 or mode == "oct") and m - 12 >= 55: out.append((m - 12, b, d, "R", .6))
    out += harmony(p, [(m, b, d, "R", .8) for m, b, d in body], .5)
    kind = lh or p["lh8"]
    out += lh_pattern(p, kind, .5)
    lm, lb, ld = mel[-1]
    if with_end:
        # trim LH under the ending and add run + chord
        out = [n for n in out if n[1] < lb - 1e-6 or n[3] == "R"]
        out = [n for n in out if n[1] < lb - 1e-6]
        e, cb = ending(p, lm, lb); out += e
        return fit(out), cb + 6, cb
    return fit(out), mel_end(p), None

def texture(p, which, bars=None):
    fn = {"moonlight": moonlight, "prelude": prelude}[p["texture"]]
    ns, spans, end = fn(bars) if bars else fn()
    return ns, spans, end

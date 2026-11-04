"""python3 gen/make.py <index|all|list>   -> videos/<NN-slug>/{audio.wav,timing.json}"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from formats import *
PI = PIECES
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "videos")
def P_(k, **over): d = dict(PI[k]); d.update(over); return d

GC = lambda k: ("grade", k)
C = []  # (slug, builder, caption, title)
def add(slug, fn, cap, title): C.append((slug, fn, cap, title))
TAGS = "#piano #pianotok #learnpiano #ad"

def gc(k):
    p = PI[k]; add(f"grade-{k}", lambda o, p=p: grade_cmp(p, o), f"Same song, three levels: {p['name']} at Grade 1, 5 and 8. Which one are you? {TAGS}", f"{p['name']}: Grade 1 vs Grade 5 vs Grade 8 #shorts")
def lv(k, cut):
    p = P_(k, cut=cut); add(f"levels-{k}", lambda o, p=p: level5(p, o), f"5 levels of {p['name']}. Which level are you? {TAGS}", f"5 Levels of {p['name']} on Piano #shorts")
def gs(keys, n):
    ps = [PI[k] for k in keys]; snow = any(p.get("snow") for p in ps)
    add(f"guess-song-{n}", lambda o, ps=ps, s=snow: guess_song(ps, o, s), f"Guess the song in 3 seconds 🎹 How many did you get? Comment your score. {TAGS}", f"Guess the Piano Song in 3 Seconds #{n} #shorts")
def gg(k, order):
    p = PI[k]; add(f"guess-grade-{k}", lambda o, p=p, od=order: guess_grade(p, od, o), f"Guess the grade: {p['name']} played at three levels. Got all 3? {TAGS}", f"Guess the Grade: {p['name']} #shorts")
def px(k, cfg, phone=False):
    p = PI[k]; add(f"practice-{k}", lambda o, p=p, c=cfg, ph=phone: practice_xv(p, c, o, ph), f"Stop playing from the top every time. Loop the bar you keep missing: slow, then faster. {TAGS}", f"Why You Keep Missing the Same Bar ({p['short']}) #shorts")
def tl(k, cfg):
    p = PI[k]; add(f"tempo-{k}", lambda o, p=p, c=cfg: tempo_ladder(p, c, o), f"The hardest bar of {p['name']}: 40% → 60% → 80% → 100%. Start slow, earn the tempo. {TAGS}", f"How to Learn the Hardest Bar of {p['short']} #shorts")
def pd(k, bars=None):
    p = PI[k]; add(f"pedal-{k}", lambda o, p=p, b=bars: pedal_cmp(p, o, b), f"No pedal vs pedal vs TOO MUCH pedal on {p['name']}. Which one do you do? {TAGS}", f"No Pedal vs Pedal vs Too Much Pedal ({p['short']}) #shorts")
def lh(k, cut=None):
    p = P_(k, cut=cut) if cut else PI[k]; add(f"left-hands-{k}", lambda o, p=p: five_lh(p, o), f"Same melody, 5 left hands: {p['name']}. Which one sounds best? {TAGS}", f"{p['name']} With 5 Different Left Hands #shorts")
def ht(items, n):
    add(f"easier-{n}", lambda o, it=items: harder_than(it, o), f"Pieces that sound harder than they are. Which one are you learning next? {TAGS}", f"Piano Pieces That Sound Harder Than They Are #{n} #shorts")
def om(k):
    p = PI[k]; add(f"one-mistake-{k}", lambda o, p=p: one_mistake(p, o), f"Piano is my therapy… until ONE wrong note. {TAGS}", f"Piano Is My Therapy (Until One Wrong Note) #shorts")

# ---- the 64, in posting order (formats interleaved)
gc("ode"); gs(["ode", "mountain", "canon"], 1); px("elise", dict(x0=0, hx=5.5, h0=4, h1=7), phone=True); lv("elise", 7)
gc("elise"); tl("turkish", dict(h0=4, h1=8)); pd("moonlight", (3, 4)); lh("ode")
gc("canon"); gg("ode", (5, 1, 8)); om("gymno"); gs(["elise", "entertainer", "twinkle"], 2)
gc("mountain"); px("turkish", dict(x0=0, hx=5, h0=4, h1=6)); ht([(PI["moonlight"], "Same 3 notes,<br>8 times in a row", (1, 2)), (PI["prelude"], "One pattern.<br>Every bar.", (1, 2)), (PI["gymno"], "2 chords,<br>taking turns", None)], 1); lv("ode", 8)
gc("jingle"); gs(["jingle", "silent", "carol"], 3); tl("elise", dict(h0=0, h1=4)); pd("prelude", (1, 2))
gc("twinkle"); px("entertainer", dict(x0=4, hx=9, h0=7, h1=11, r1=12.5)); lh("twinkle"); gg("canon", (8, 5, 1))
gc("entertainer"); gs(["beet5", "toccata", "moonlight"], 4); om("brahms"); lv("mountain", 4)
gc("silent"); px("mountain", dict(x0=0, hx=6, h0=4, h1=8, r1=8), phone=True); tl("mountain", dict(level=8, h0=8, h1=12)); lh("amazing", 7)
gc("turkish"); gs(["turkish", "nacht", "spring"], 5); pd("gymno"); gg("greensleeves", (1, 8, 5))
gc("nacht"); px("minuet", dict(x0=3, hx=8.5, h0=6, h1=9)); ht([(PI["elise"], "Just 2 notes,<br>rocking", None), (PI["canon"], "8 chords.<br>On repeat.", None), (PI["carol"], "4 notes.<br>On repeat.", None)], 2); lv("jingle", 8)
gc("carol"); gs(["deck", "wewish", "joy"], 6); tl("entertainer", dict(h0=7, h1=11)); lh("silent", 9)
gc("minuet"); px("greensleeves", dict(x0=0, hx=5.5, h0=4, h1=7, r1=10)); gg("brahms", (5, 8, 1)); om("silent")
gc("deck"); px("jingle", dict(level=8, x0=4, hx=10, h0=8, h1=12), phone=True); pd("canon"); lv("canon", 4)
gc("gymno"); tl("canon", dict(level=8, h0=0, h1=2)); lh("brahms", 7); gg("minuet", (8, 1, 5))
gc("wewish"); px("nacht", dict(x0=0, hx=5.5, h0=4, h1=8, r1=8)); lv("entertainer", 7); gc("greensleeves")
gc("brahms"); gc("amazing"); gc("chopsticks"); gc("largo")

def slug(i): return f"{i + 1:02d}-{C[i][0]}"
if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "list"
    if a == "list":
        for i, c in enumerate(C): print(slug(i))
        print(len(C)); sys.exit()
    if a == "captions":
        L = ["# Between Lessons: 64 shorts\n", "Listen to each before posting and check the notes by ear (all arranged from memory). Every caption has #ad. Pin a comment: \"Comment PLAN and I'll send the free Day 1 link\".\n"]
        for i, (s, fn, cap, title) in enumerate(C):
            d = json.load(open(f"{ROOT}/{slug(i)}/timing.json"))["duration"] if os.path.exists(f"{ROOT}/{slug(i)}/timing.json") else 0
            L.append(f"## {slug(i)} ({d:.0f}s)\n- **Caption:** {cap}\n- **YouTube title:** {title}\n")
        open(sys.argv[2], "w").write("\n".join(L)); sys.exit()
    idx = range(len(C)) if a == "all" else [int(x) - 1 for x in a.split(",")]
    for i in idx:
        out = f"{ROOT}/{slug(i)}"; d = C[i][1](out); print(f"{slug(i)} {d:.1f}s")

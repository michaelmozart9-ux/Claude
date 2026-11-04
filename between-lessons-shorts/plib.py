# Audio library: real sampled grand piano (./wav, made by setup.py) + synth SFX + mastering. Import with: from plib import *
import os, numpy as np, soundfile as sf
SR = 48000
WAV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wav")
_c = {}
def smp(m):
    m = int(max(33, min(89, m)))
    if m not in _c: _c[m] = sf.read(f"{WAV}/{m}.wav")[0].astype(np.float32)
    return _c[m]
N = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def P(n):
    acc = 0; s = n[1:]
    if s[0] in "#b": acc = 1 if s[0] == "#" else -1; s = s[1:]
    return 12 * (int(s) + 1) + N[n[0]] + acc
def T(d): return np.arange(int(d * SR)) / SR
def add(tr, sig, t, g):
    i = int(max(0, t) * SR); j = min(len(tr), i + len(sig))
    if j > i: tr[i:j] += sig[: j - i] * g
def piano(tr, note, t, dur, v):
    m = P(note) if isinstance(note, str) else note; s = smp(m); L = min(len(s), int((dur + 0.4) * SR)); y = s[:L].copy()
    r0 = int(dur * SR)
    if r0 < L: y[r0:] *= np.exp(-np.arange(L - r0) / SR / 0.14)
    y[-min(400, L):] *= np.linspace(1, 0, min(400, L)); add(tr, y * (v ** 1.5), t, 0.9)
def reverb(x, wet=0.22, dec=0.35, seed=3):
    rng = np.random.default_rng(seed); t = T(1.6)
    ir = rng.standard_normal(len(t)) * np.exp(-t / dec); ir[: int(0.012 * SR)] = 0; ir /= np.sqrt(np.sum(ir ** 2))
    n = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    return x + wet * np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[: len(x)].astype(np.float32)
def lp_noise(d, a0, a1, seed=1):
    rng = np.random.default_rng(seed); nz = rng.standard_normal(int(d * SR)); out = np.zeros_like(nz); y = 0.0; x = np.linspace(0, 1, len(nz))
    for i in range(len(nz)): a = a0 + (a1 - a0) * x[i]; y += a * (nz[i] - y); out[i] = y
    return out
def whoosh(d=0.5, seed=4):
    x = np.linspace(0, 1, int(d * SR)); return (lp_noise(d, 0.02, 0.25, seed) * np.sin(np.pi * x) ** 2 * 2.5).astype(np.float32)
def boom(d=1.4):
    t = T(d); f = 32 + 80 * np.exp(-t * 6); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.8) * (1 - np.exp(-t * 400))).astype(np.float32)
def kick(f0=110, f1=40, d=0.35):
    t = T(d); f = f1 + (f0 - f1) * np.exp(-t * 28); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)).astype(np.float32)
def pop(f=900, d=0.12):
    t = T(d); f = f * (1 + 0.6 * np.exp(-t * 60)); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35)).astype(np.float32)
def ding(f=1567.98, d=1.4):
    t = T(d); return (sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * k) for r, a, k in [(1, 1, 3), (2.76, .4, 5), (5.4, .2, 8)]) * (1 - np.exp(-t * 600))).astype(np.float32)
def buzz():
    t = T(0.3); return (np.sign(np.sin(2 * np.pi * 110 * t)) * np.exp(-t * 9) * 0.5).astype(np.float32)
def click(acc=False):
    t = T(0.06); f = 1900 if acc else 1350; return (np.sin(2 * np.pi * f * t) * np.exp(-t * 90)).astype(np.float32)
def scratch(d=0.5, seed=6):
    t = T(d); rng = np.random.default_rng(seed); f = 900 * np.exp(-t * 6) + 80
    return ((np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.4 + rng.standard_normal(len(t)) * 0.25) * np.exp(-t * 4) * (1 - np.exp(-t * 300))).astype(np.float32)
def sparkle(seed=4, n=7, d=1.0):
    rng = np.random.default_rng(seed); out = np.zeros(int(d * SR), np.float32)
    for k in range(n):
        tt = T(0.35); y = np.sin(2 * np.pi * rng.uniform(2500, 5200) * tt) * np.exp(-tt * 14); i = int(k * d / n * 0.8 * SR); out[i:i + len(y)] += y[: len(out) - i]
    return out
def riser(d=0.9):
    t = T(d); return ((lp_noise(d, 0.01, 0.5, 7) * 2 + np.sin(2 * np.pi * np.cumsum(300 + 900 * (t / d) ** 2) / SR) * 0.15) * (t / d) ** 2.2).astype(np.float32)
def tap():
    t = T(0.05); return (np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 160)).astype(np.float32)
def boing(f0=300, f1=700, d=0.35):
    t = T(d); f = f0 + (f1 - f0) * (t / d) + 30 * np.sin(2 * np.pi * 18 * t); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)).astype(np.float32)
def applause(d=3.5, seed=9, dens=60):
    rng = np.random.default_rng(seed); out = np.zeros(int(d * SR), np.float32); n = int(d * dens)
    for _ in range(n):
        tt = rng.uniform(0, d); env = min(1, tt / 0.3) * np.exp(-max(0, tt - 1.2) * 0.9)
        c = rng.standard_normal(int(0.025 * SR)) * np.exp(-T(0.025) * 220); c = np.diff(c, prepend=0)
        i = int(tt * SR); out[i:i + len(c)] += c[: len(out) - i] * env * rng.uniform(0.4, 1)
    return out
def master(mix, dur, path, fade=0.7):
    mix = mix[: int(dur * SR)]; mix = mix * np.clip((dur - np.arange(len(mix)) / SR) / fade, 0, 1)
    pk = float(np.percentile(np.abs(mix), 99.97)) or 1.0; mix = np.tanh(1.9 * mix / pk) / np.tanh(1.9) * 0.93
    sf.write(path, mix.astype(np.float32), SR)
def place(notes, bpm, t0, sec, pedal=None, rng=None, jitter=0.006, final_beat=None, win=None, shift=0.0):
    """notes: (midi, beat, dur_beats, hand 'R'|'L'|'X'(wrong, red), vel) -> note dicts with absolute seconds.
    pedal=N holds notes to the end of each N-beat group; win=(t0,t1) keeps only notes starting inside; shift moves times back."""
    rng = rng or np.random.default_rng(1); q = 60 / bpm; out = []
    for m, b, d, h, v in notes:
        t = t0 + b * q + (rng.normal(0, jitter) if jitter else 0); dur = d * q; rel = t + dur + 0.03
        if pedal: rel = max(t + dur, t0 + (np.floor(b / pedal + 1e-6) + 1) * pedal * q + 0.02)
        if final_beat is not None and b >= final_beat: rel = t + dur
        if win and not (win[0] <= t < win[1]): continue
        out.append({"m": int(m), "t": round(t - shift, 4), "d": round(dur, 4), "rel": round(rel - shift, 4), "h": h,
                    "v": round(float(np.clip(v + rng.normal(0, 0.03), 0.2, 1)), 3), "sec": sec})
    return out
def render(notes, dur, sec_end):
    """Render placed notes with real samples. sec_end: {section_id: end_time} fades each section out at its cut."""
    tr = np.zeros(int((dur + 2) * SR), np.float32)
    for n in notes:
        s = smp(n["m"]); i0 = int(n["t"] * SR)
        if i0 < 0: continue
        end = sec_end.get(n["sec"], dur); rel = min(n["rel"], end); L = min(len(s), int((rel - n["t"] + 0.35) * SR))
        if L <= 0: continue
        y = s[:L].copy(); r0 = int((rel - n["t"]) * SR)
        if r0 < L: y[r0:] *= np.exp(-np.arange(L - r0) / SR / 0.09)
        cut = int((end - n["t"]) * SR)
        if cut < L: y[max(0, cut - 1200):] *= np.linspace(1, 0, L - max(0, cut - 1200))
        y[-min(400, L):] *= np.linspace(1, 0, min(400, L)); tr[i0:i0 + L] += y * (n["v"] ** 1.5) * 0.9
    return tr

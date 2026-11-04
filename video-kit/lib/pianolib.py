"""Piano + mixing helpers. Samples: Salamander Grand Piano (CC-BY 3.0, Alexander Holm).
All times in seconds. Notes are dicts: {m, t, d, v, h, sec, pe(optional pedal end)}.
"""
import os, numpy as np, soundfile as sf

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
WAV = os.path.join(HERE, "..", "assets", "wav")
_NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_CACHE = {}
LAYERS = {4: 0.32, 8: 0.62, 12: 0.92}


def P(name):
    """'C#4' -> 61, 'Bb3' -> 58, 'C4' -> 60. Ints pass through."""
    if isinstance(name, (int, np.integer)):
        return int(name)
    n = name.strip()
    base = _NAMES[n[0].upper()]
    i = 1
    while i < len(n) and n[i] in "#b":
        base += 1 if n[i] == "#" else -1
        i += 1
    return 12 * (int(n[i:]) + 1) + base


def _sample(layer, midi):
    key = (layer, midi)
    if key not in _CACHE:
        _CACHE[key] = np.load(os.path.join(WAV, f"v{layer}_{midi}.npy"))
    return _CACHE[key]


_AVAIL = {}
def _avail(layer):
    if layer not in _AVAIL:
        _AVAIL[layer] = sorted(int(f.split("_")[1].split(".")[0]) for f in os.listdir(WAV) if f.startswith(f"v{layer}_"))
    return _AVAIL[layer]


def note_audio(m, hold, vel=0.7, tail=0.5):
    """Mono audio for one key press held `hold` seconds (damper after)."""
    layer = min(LAYERS, key=lambda L: abs(LAYERS[L] - vel))
    av = _avail(layer)
    sm = min(av, key=lambda a: abs(a - m))
    src = _sample(layer, sm)
    ratio = 2 ** ((m - sm) / 12)
    n = int((hold + tail) * SR)
    pos = np.arange(n) * ratio
    pos = pos[pos < len(src) - 1]
    out = np.interp(pos, np.arange(len(src)), src).astype(np.float32)
    g = np.clip(vel / LAYERS[layer], 0.55, 1.5) * (0.65 + 0.5 * vel)
    out *= g
    # damper: fast exponential release after hold
    h = int(hold * SR)
    if h < len(out):
        rel = np.exp(-np.arange(len(out) - h) / (0.09 * SR)).astype(np.float32)
        out[h:] *= rel
    # tiny attack smoothing
    a = min(64, len(out))
    out[:a] *= np.linspace(0, 1, a, dtype=np.float32)
    return out


def track(dur):
    return np.zeros((int((dur + 3) * SR), 2), np.float32)


def add(mix, sig, t, gain=1.0, pan=0.0):
    """Add mono or stereo signal at time t."""
    if sig is None or len(sig) == 0:
        return
    i = int(max(0, t) * SR)
    if i >= len(mix):
        return
    s = sig if sig.ndim == 2 else np.stack([sig * np.cos((pan + 1) * np.pi / 4) * 1.414, sig * np.sin((pan + 1) * np.pi / 4) * 1.414], 1)
    n = min(len(s), len(mix) - i)
    mix[i:i + n] += s[:n] * gain


def piano(mix, m, t, hold, vel=0.7, gain=1.0):
    m = P(m)
    hold = max(0.03, hold)
    pan = np.clip((m - 60) / 40, -0.6, 0.6)
    add(mix, note_audio(m, hold, vel), t, gain, pan)


def render(notes, dur, sec_end=None, gain=1.0):
    """Render note dicts into a stereo track. sec_end: {sec_id: time} hard-stop (jump cuts)."""
    sec_end = sec_end or {}
    mix = track(dur)
    for n in notes:
        if n.get("silent"):
            continue
        hold = max(n["d"], n.get("pe", 0) - n["t"])
        end = sec_end.get(n.get("sec"))
        if end is not None:
            if n["t"] >= end:
                continue
            hold = min(hold, max(0.02, end - n["t"]))
        piano(mix, n["m"], n["t"], hold, n.get("v", 0.7), gain * n.get("g", 1.0))
    return mix


def place(seq, bpm, t0, sec="s", hand="R", vel=0.7, pedal=None, swing=0.0, final_beat=None, human=0.0, seed=1):
    """seq: list of (note|[notes]|None, beat, dur_beats[, hand][, vel]).
    bpm counts beats in `seq` units. pedal: None, number of beats per pedal change, or 'hold'."""
    rng = np.random.default_rng(seed)
    spb = 60.0 / bpm
    out = []
    for item in seq:
        note, beat, dur = item[0], item[1], item[2]
        h = item[3] if len(item) > 3 and item[3] else hand
        v = item[4] if len(item) > 4 and item[4] is not None else vel
        if note is None:
            continue
        ns = note if isinstance(note, (list, tuple)) else [note]
        for k, nn in enumerate(ns):
            t = t0 + beat * spb + (rng.normal(0, human) if human else 0)
            d = dur * spb * 0.96
            n = {"m": P(nn), "t": round(t, 4), "d": round(max(0.04, d), 4), "v": float(np.clip(v - 0.04 * k * (h == "L"), 0.1, 1.0)), "h": h, "sec": sec}
            if pedal == "hold":
                n["pe"] = 999
            elif pedal:
                nb = (np.floor(beat / pedal + 1e-6) + 1) * pedal
                n["pe"] = round(t0 + nb * spb - 0.03, 4)
            out.append(n)
    return out


def shift_t(notes, dt):
    return [dict(n, t=round(n["t"] + dt, 4), **({"pe": round(n["pe"] + dt, 4)} if "pe" in n and n["pe"] < 900 else {})) for n in notes]


def reverb(x, wet=0.2, rt=1.9, seed=3):
    """Stereo synthetic hall reverb via FFT convolution."""
    rng = np.random.default_rng(seed)
    n = int(rt * SR)
    tt = np.arange(n) / SR
    env = np.exp(-6.9 * tt / rt)
    out = x.copy()
    for ch in range(2):
        noise = rng.normal(0, 1, n)
        # warm it: simple low-pass by cumulative moving average in frequency domain
        F = np.fft.rfft(noise)
        f = np.fft.rfftfreq(n, 1 / SR)
        F *= 1 / (1 + (f / 4500) ** 2)
        ir = np.fft.irfft(F, n) * env
        ir[: int(0.012 * SR)] = 0
        ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
        L = len(x[:, ch]) + n
        N = 1 << int(np.ceil(np.log2(L)))
        y = np.fft.irfft(np.fft.rfft(x[:, ch], N) * np.fft.rfft(ir, N), N)[: len(x)]
        out[:, ch] = x[:, ch] + wet * y.astype(np.float32) * 0.35
    return out


def master(mix, dur, path, peak=0.89):
    y = mix[: int(dur * SR)].copy()
    ref = np.percentile(np.abs(y), 99.95) + 1e-9
    y *= peak / ref
    over = np.abs(y) > 0.8
    y[over] = np.sign(y[over]) * (0.8 + 0.2 * np.tanh((np.abs(y[over]) - 0.8) / 0.2))
    fade = int(0.04 * SR)
    y[-fade:] *= np.linspace(1, 0, fade)[:, None]
    sf.write(path, y, SR, subtype="PCM_16")
    return y

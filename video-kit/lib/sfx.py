"""Synthesised sound effects (mono float32 arrays at SR)."""
import numpy as np
from pianolib import SR, piano, P

_rng = np.random.default_rng(11)


def _t(d):
    return np.arange(int(d * SR)) / SR


def _bp(x, lo, hi):
    F = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    F[(f < lo) | (f > hi)] *= 0.02
    return np.fft.irfft(F, len(x)).astype(np.float32)


def whoosh(d=0.45):
    t = _t(d)
    x = _bp(_rng.normal(0, 1, len(t)), 300, 5000)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    return (x * env * 0.8).astype(np.float32)


def boom(d=1.2):
    t = _t(d)
    f = 40 + 60 * np.exp(-t * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 3.2)
    n = _bp(_rng.normal(0, 1, len(t)), 30, 400) * np.exp(-t * 14) * 0.5
    return ((s + n) * 0.9).astype(np.float32)


def kick():
    t = _t(0.35)
    f = 50 + 120 * np.exp(-t * 30)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)).astype(np.float32)


def hat():
    t = _t(0.06)
    return (_bp(_rng.normal(0, 1, len(t)), 7000, 16000) * np.exp(-t * 70) * 0.6).astype(np.float32)


def ding(freq=1567.98, d=1.2):
    t = _t(d)
    s = sum(a * np.sin(2 * np.pi * freq * r * t) * np.exp(-t * k) for a, r, k in [(1, 1, 3.5), (0.4, 2.0, 5), (0.25, 2.76, 7), (0.1, 5.4, 10)])
    return (s * 0.5).astype(np.float32)


def buzz(d=0.38):
    t = _t(d)
    s = np.sign(np.sin(2 * np.pi * 98 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 147 * t)) * 0.3
    env = np.minimum(1, t * 200) * np.exp(-t * 3)
    return (_bp(s, 60, 3000) * env).astype(np.float32)


def riser(d=0.8):
    t = _t(d)
    f = 250 * (5 ** (t / d))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + _bp(_rng.normal(0, 1, len(t)), 2000, 9000) * 0.5
    return (s * (t / d) ** 2).astype(np.float32)


def pop(freq=1200):
    t = _t(0.08)
    f = freq * (1 + 0.6 * np.exp(-t * 60))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)).astype(np.float32)


def tap():
    t = _t(0.05)
    return (_bp(_rng.normal(0, 1, len(t)), 1500, 8000) * np.exp(-t * 160) + np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 90) * 0.4).astype(np.float32)


def tick(freq=1800):
    t = _t(0.06)
    return (np.sin(2 * np.pi * freq * t) * np.exp(-t * 80) + np.sin(2 * np.pi * freq * 1.5 * t) * np.exp(-t * 120) * 0.4).astype(np.float32)


def sparkle(d=0.6, n=9):
    t = _t(d)
    out = np.zeros(len(t), np.float32)
    for k in range(n):
        st = int(_rng.uniform(0, d * 0.7) * SR)
        f = _rng.uniform(2500, 6000)
        tt = t[: len(t) - st]
        out[st:] += (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 18) * 0.3).astype(np.float32)
    return out


def confetti(d=0.9):
    t = _t(d)
    out = np.zeros(len(t), np.float32)
    for k in range(40):
        st = int(_rng.uniform(0, d * 0.8) * SR)
        ln = int(0.006 * SR)
        if st + ln < len(out):
            out[st:st + ln] += _rng.normal(0, 1, ln) * np.exp(-np.arange(ln) / 60) * _rng.uniform(0.2, 0.6)
    out += pop(700)[: len(out)] * 0.0 if False else 0
    popn = _bp(_rng.normal(0, 1, int(0.05 * SR)), 300, 6000) * np.exp(-np.arange(int(0.05 * SR)) / 400)
    out[: len(popn)] += popn * 0.9
    return _bp(out, 800, 12000)


def shatter(d=0.9):
    t = _t(d)
    out = _bp(_rng.normal(0, 1, len(t)), 2500, 12000) * np.exp(-t * 7) * 0.6
    for k in range(14):
        st = int(_rng.uniform(0, d * 0.6) * SR)
        f = _rng.uniform(3000, 8000)
        tt = t[: len(t) - st]
        out[st:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 25) * 0.25
    return out.astype(np.float32)


def levelup():
    out = np.zeros(int(0.6 * SR), np.float32)
    for k, f in enumerate([1046.5, 1318.5, 1568, 2093]):
        st = int(k * 0.07 * SR)
        t = _t(0.25)
        s = (np.sign(np.sin(2 * np.pi * f * t)) * 0.25 + np.sin(2 * np.pi * f * t) * 0.5) * np.exp(-t * 14)
        out[st:st + len(s)] += s[: len(out) - st]
    return _bp(out, 200, 9000)


def msgpop():
    t = _t(0.16)
    f = np.where(t < 0.06, 700, 1150)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-((t - 0.06) ** 2) / 0.003) * 0.8).astype(np.float32)


def typing(d=0.8, rate=11):
    out = np.zeros(int(d * SR), np.float32)
    for k in range(int(d * rate)):
        st = int((k / rate + _rng.uniform(0, 0.03)) * SR)
        c = tap() * _rng.uniform(0.3, 0.7)
        out[st:st + len(c)] += c[: len(out) - st]
    return out


def wind(d=2.0):
    t = _t(d)
    x = _bp(_rng.normal(0, 1, len(t)), 150, 1200)
    env = (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t)) * np.sin(np.pi * t / d)
    return (x * env * 0.6).astype(np.float32)


def scratch(d=0.35):
    t = _t(d)
    f = 400 + 1600 * np.abs(np.sin(2 * np.pi * 6 * t))
    x = _bp(_rng.normal(0, 1, len(t)), 300, 5000) * np.sin(2 * np.pi * np.cumsum(f) / SR)
    return (x * np.exp(-t * 4)).astype(np.float32)


def whistle(d=0.6, up=True):
    t = _t(d)
    f = (600 + 1400 * (t / d)) if up else (2000 - 1400 * (t / d))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) * 0.5).astype(np.float32)


def bell(freq=1318.5, d=1.6):
    t = _t(d)
    s = sum(a * np.sin(2 * np.pi * freq * r * t) * np.exp(-t * k) for a, r, k in [(1, 1, 2.2), (0.6, 2.4, 3.5), (0.35, 3.0, 4.5), (0.2, 4.2, 6), (0.12, 5.9, 8)])
    return (s * 0.35).astype(np.float32)


def bed(mix, t0, t1, bpm, chords, vel=0.28, kgain=0.1, hgain=0.025, arp=False, beats_per_chord=4):
    """Soft piano-chord music bed. chords: [(bass, [notes...]), ...] cycled."""
    spb = 60 / bpm
    t = t0
    i = 0
    from pianolib import add as _add
    while t < t1 - 0.2:
        bass, ch = chords[i % len(chords)]
        hold = min(beats_per_chord * spb, t1 - t)
        piano(mix, bass, t, hold, vel + 0.05)
        if arp:
            for k, nn in enumerate(ch):
                piano(mix, nn, t + k * spb / 2, hold - k * spb / 2, vel)
        else:
            for nn in ch:
                piano(mix, nn, t + 0.01, hold, vel)
        for b in range(beats_per_chord):
            tb = t + b * spb
            if tb >= t1 - 0.1:
                break
            if kgain and b % 2 == 0:
                _add(mix, kick(), tb, kgain)
            if hgain:
                _add(mix, hat(), tb + spb / 2, hgain)
        t += beats_per_chord * spb
        i += 1

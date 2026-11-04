# Decode Salamander Grand Piano mp3 samples (CC-BY 3.0, Alexander Holm) to 44.1k mono float32 .npy
import os, subprocess, numpy as np, glob, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "wav")
os.makedirs(OUT, exist_ok=True)
NAMES = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}
for layer in (4, 8, 12):
    d = os.path.join(ROOT, "node_modules", "@audio-samples", f"piano-mp3-velocity{layer}", "audio")
    for f in sorted(glob.glob(os.path.join(d, "*.mp3"))):
        m = re.match(r"([A-G]#?)(\d)v\d+\.mp3", os.path.basename(f))
        midi = 12 * (int(m.group(2)) + 1) + NAMES[m.group(1)]
        if midi < 28 or midi > 96: continue
        dst = os.path.join(OUT, f"v{layer}_{midi}.npy")
        if os.path.exists(dst): continue
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "44100", "-f", "f32le", "-"], capture_output=True).stdout
        a = np.frombuffer(raw, np.float32).copy()
        # trim leading silence
        nz = np.nonzero(np.abs(a) > 0.002)[0]
        if len(nz): a = a[max(0, nz[0] - 20):]
        a = a[: 44100 * 9]
        np.save(dst, a.astype(np.float32))
print(len(os.listdir(OUT)), "samples")

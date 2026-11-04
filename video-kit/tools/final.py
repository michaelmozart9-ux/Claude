# final check: contact sheet of 15 evenly spaced final frames + duration check
import sys, os, json, subprocess, shutil
v = sys.argv[1]
d = f"videos/{v}/frames"; fs = sorted(os.listdir(d)); n = len(fs)
pick = [fs[int(i * (n - 1) / 14)] for i in range(15)]
tmp = f"/tmp/claude-0/s/final_{v}"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
for f in pick: shutil.copy(os.path.join(d, f), os.path.join(tmp, f"{int(f[:4]) / 30:06.2f}s.jpg"))
subprocess.run(["python3", "tools/sheet.py", tmp, f"/tmp/claude-0/s/final_{v}.jpg", "8"], check=True)
T = json.load(open(f"videos/{v}/timing.json"))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"out/{v}.mp4"], capture_output=True, text=True).stdout)
print(v, "frames", n, "expected", round(T["duration"] * 30), "mp4", round(dur, 2), "timing", T["duration"])

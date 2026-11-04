#!/bin/bash
# render + encode one video dir name (e.g. 01-grade-ode)
cd "$(dirname "$0")"
v=$1; OUT=../out
[ -f "$OUT/$v.mp4" ] && exit 0
rm -rf videos/$v/frames
node render2.mjs videos/$v full > logs/$v.log 2>&1
ffmpeg -y -loglevel error -framerate 30 -i videos/$v/frames/%04d.jpg -i videos/$v/audio.wav -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT/$v.tmp.mp4" >> logs/$v.log 2>&1 && mv "$OUT/$v.tmp.mp4" "$OUT/$v.mp4"
python3 - "$v" <<'PY'
import sys, glob
from PIL import Image
v=sys.argv[1]; fs=sorted(glob.glob(f'videos/{v}/frames/*.jpg')); n=len(fs)
pick=[fs[min(n-1,int((i+.5)*n/12))] for i in range(12)]
W,H=216,384; im=Image.new('RGB',(W*6,H*2))
for i,f in enumerate(pick): im.paste(Image.open(f).resize((W,H)),((i%6)*W,(i//6)*H))
im.save(f'videos/{v}/final-sheet.jpg')
PY
rm -rf videos/$v/frames
echo "$(date +%H:%M:%S) done $v $(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT/$v.mp4 2>/dev/null)" >> logs/progress.txt

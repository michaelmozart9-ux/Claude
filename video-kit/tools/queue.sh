#!/bin/bash
# tools/queue.sh <port> video1 video2 ...   renders frames + encodes mp4 into out/
cd "$(dirname "$0")/.."
PORT=$1; shift
mkdir -p out
for v in "$@"; do
  rm -rf videos/$v/frames
  PORT=$PORT node render.mjs $v full > logs/$v.log 2>&1
  ffmpeg -y -loglevel error -framerate 30 -i videos/$v/frames/%04d.jpg -i videos/$v/audio.wav -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out/$v.mp4 >> logs/$v.log 2>&1
  echo "$v $(ffprobe -v error -show_entries format=duration -of csv=p=0 out/$v.mp4) $(du -h out/$v.mp4 | cut -f1)" >> logs/done.txt
done

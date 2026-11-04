#!/bin/bash
# pops video names from logs/todo.txt and renders them one by one; stops on STOP
cd "$(dirname "$0")/.."
mkdir -p out logs
while true; do
  v=$(head -n 1 logs/todo.txt 2>/dev/null)
  if [ -z "$v" ]; then sleep 15; continue; fi
  sed -i '1d' logs/todo.txt
  [ "$v" = "STOP" ] && exit 0
  rm -rf videos/$v/frames
  node render.mjs $v full > logs/$v.log 2>&1
  ffmpeg -y -loglevel error -framerate 30 -i videos/$v/frames/%04d.jpg -i videos/$v/audio.wav -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out/$v.mp4 >> logs/$v.log 2>&1
  echo "$v $(ffprobe -v error -show_entries format=duration -of csv=p=0 out/$v.mp4) $(du -h out/$v.mp4 | cut -f1) $(date +%T)" >> logs/done.txt
done

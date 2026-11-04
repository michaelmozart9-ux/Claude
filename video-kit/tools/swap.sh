#!/bin/bash
# start one worker2 each time an old worker exits
cd "$(dirname "$0")/.."
started=0
while [ $started -lt 2 ]; do
  old=$(ps -eo args | grep -v grep | grep -c "tools/worker.sh")
  want=$((2 - old))
  while [ $started -lt $want ]; do nohup tools/worker2.sh > /dev/null 2>&1 & started=$((started+1)); echo "started worker2 #$started $(date +%T)"; sleep 2; done
  sleep 3
done

#!/bin/bash
# QA on the WS-2 finals (1.15x, music): boxes, stills, black/flash, loudness, transcript.  ->  v5/qa/final_ws2/
set -e
cd "$(dirname "$0")/.."
PY=~/.venvs/adstudio/bin/python
Q=qa/final_ws2; mkdir -p $Q
for CUT in WS-2_H1 WS-2_H4; do
  F=final/${CUT}__A_tech_house.mp4
  J=$(python3 -c "print({'WS-2_H1':5.9,'WS-2_H4':3.9}['$CUT'])")
  # tracked-box moments in cut time (landed): body 1 stations + body 2 category list + Copy JSON prompt, mapped to 1.15x
  T=$(python3 -c "
j=$J; b2=j+14.3667
ts=[j+t for t in (4.1,4.6,6.2,6.9,8.6,9.2,10.7,11.1,12.9,13.4,14.2)]+[b2+t for t in (0.9,1.1,1.25,2.3,2.9,3.15)]
print(','.join(f'{t/1.15:.3f}' for t in ts))")
  $PY tools/qa_boxes.py $F $Q/boxes_$CUT $T | sed 's/(lines.*//' > $Q/boxes_$CUT.txt
  rm -f $Q/boxes_$CUT/f_*.png
  $PY tools/static_scan.py $F > $Q/static_$CUT.txt
  ffmpeg -hide_banner -nostats -i $F -af ebur128=peak=true -f null - 2>&1 | grep -A16 "Summary" > $Q/loudness_$CUT.txt
done
echo done

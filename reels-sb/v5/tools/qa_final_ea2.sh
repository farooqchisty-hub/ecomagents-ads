#!/bin/bash
# QA on the EA-2 finals (1.15x, music): tracked boxes, hero hold, stills, black/flash, loudness, transcript  ->  v5/qa/final_ea2/
set -e
cd "$(dirname "$0")/.."
PY=~/.venvs/adstudio/bin/python
Q=qa/final_ea2; mkdir -p $Q; : > $Q/hero_hold.txt
for CUT in EA-2_H2 EA-2_H4 EA-2_H5; do
  F=final/${CUT}__A_tech_house.mp4
  J=$(python3 -c "print({'EA-2_H2':6.8,'EA-2_H4':7.4333,'EA-2_H5':6.2}['$CUT'])")
  # landed box moments (cut time), mapped to 1.15x: body 1 skills + hub, body 3 sidebar + flows, body 4 packages
  T=$(python3 -c "
j=$J; b1=j; b3=j+11.6667+7.4333; b4=b3+10.6667
ts=[b1+t for t in (5.2,6.15,7.6,8.1)]+[b3+t for t in (1.45,3.4,4.7,5.9,6.58)]+[b4+t for t in (1.9,2.8,3.6,5.0,6.1)]
print(','.join(f'{t/1.15:.3f}' for t in ts))")
  $PY tools/qa_boxes.py $F $Q/boxes_$CUT $T | sed 's/(lines.*//' > $Q/boxes_$CUT.txt
  rm -f $Q/boxes_$CUT/f_*.png
  # Pawfull hero: from body 2 into body 3
  H0=$(python3 -c "print(f'{($J+11.6667+5.6)/1.15:.3f}')"); H1=$(python3 -c "print(f'{($J+11.6667+7.4333+1.6)/1.15:.3f}')")
  $PY tools/hero_hold.py $F mg/assets/pairs/pawfull_ad.jpg 820 $H0 $H1 "$CUT Pawfull hero" >> $Q/hero_hold.txt
  $PY tools/static_scan.py $F > $Q/static_$CUT.txt
  ffmpeg -hide_banner -nostats -i $F -af ebur128=peak=true -f null - 2>&1 | grep -A16 "Summary" > $Q/loudness_$CUT.txt
done
echo done

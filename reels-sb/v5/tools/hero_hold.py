#!/usr/bin/env python3
"""Measure how long a hero image is on screen at full size: template-match the hero (scaled to its landed width)
in every frame of a window; frames scoring >= THRESH count as held. Prints the longest unbroken hold.

    ~/.venvs/adstudio/bin/python tools/hero_hold.py video.mp4 hero.jpg landed_width t0 t1 [label]
"""
import cv2, numpy as np, sys, subprocess, tempfile, glob, os
video, img, width, t0, t1 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
label = sys.argv[6] if len(sys.argv) > 6 else os.path.basename(img)
TH, K = 0.80, 0.25
d = tempfile.mkdtemp()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", video, "-t", f"{t1 - t0:.3f}", "-vf", f"scale={int(1080 * K)}:-1", f"{d}/%04d.png"], check=True)
fps = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", video], capture_output=True, text=True).stdout.strip().split("/")[0])
hero = cv2.imread(img); h = hero.shape[0] * width / hero.shape[1]
tpl = cv2.resize(hero, (int(width * K), int(h * K)), interpolation=cv2.INTER_AREA)
tpl = tpl[3:-3, 3:-3]                                # ignore the rounded corners
scores = []
for f in sorted(glob.glob(d + "/*.png")):
    fr = cv2.imread(f)
    scores.append(float(cv2.matchTemplate(fr, tpl, cv2.TM_CCOEFF_NORMED).max()))
best, run, start, bstart = 0, 0, 0, 0
for i, s in enumerate(scores):
    if s >= TH:
        if run == 0: start = i
        run += 1
        if run > best: best, bstart = run, start
    else: run = 0
print(f"{label}: held at full size {best / fps:.2f}s (frames {best}, from {t0 + bstart / fps:.2f}s to {t0 + (bstart + best) / fps:.2f}s), peak score {max(scores):.3f}")

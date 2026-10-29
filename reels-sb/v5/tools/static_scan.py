#!/usr/bin/env python3
"""Dead-air and black/flash scan: per frame, mean abs difference of a blurred 270x480 copy against the previous frame
(blur removes the grain layer). Reports runs > 1.0 s below the motion threshold, black frames (mean < 8) and
flash frames (mean jumps > 60 levels for a single frame).    python tools/static_scan.py video.mp4"""
import cv2, numpy as np, sys
cap = cv2.VideoCapture(sys.argv[1]); fps = cap.get(cv2.CAP_PROP_FPS); prev = None; diffs = []; means = []
while True:
    ok, f = cap.read()
    if not ok: break
    g = cv2.GaussianBlur(cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (270, 480)).astype(np.float32), (5, 5), 0)
    means.append(float(g.mean())); diffs.append(0.0 if prev is None else float(np.abs(g - prev).mean())); prev = g
TH = 0.12; run = 0; worst = (0, 0)
for i, d in enumerate(diffs[1:], 1):
    run = run + 1 if d < TH else 0
    if run > worst[0]: worst = (run, i)
print(f"{sys.argv[1]}: {len(diffs)} frames @ {fps:.0f} fps; longest still run {worst[0] / fps:.2f}s ending {worst[1] / fps:.2f}s")
print("  black frames:", [round(i / fps, 2) for i, m in enumerate(means) if m < 8][:10])
fl = [round(i / fps, 2) for i in range(1, len(means) - 1) if means[i] - means[i - 1] > 60 and means[i] - means[i + 1] > 60]
print("  flash frames:", fl)
print("  quietest 1 s windows (mean diff):", sorted((round(float(np.mean(diffs[i:i + int(fps)])), 3), round(i / fps, 1)) for i in range(1, len(diffs) - int(fps), int(fps // 2)))[:4])

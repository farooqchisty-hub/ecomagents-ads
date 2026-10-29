#!/usr/bin/env python3
"""Measure the tour's filter + template-dialog stretch (7 to 15.8 s) for WS body 2.

The page does not scroll here (offset 0), so each target is a fixed rectangle while it is on screen. For every target the
edges are re-measured (max brightness step, sub-pixel) on every frame of its on-screen window and the median is kept;
the spread per edge is reported so a moving or wrong target shows up. Writes mg/assets/tour/tour_track_b2.json.

    ~/.venvs/adstudio/bin/python tools/track_tour_b2.py <tour.mp4> <out_dir>
"""
import cv2, numpy as np, json, os, subprocess, sys, tempfile, glob
src, out = sys.argv[1], sys.argv[2]
tmp = tempfile.mkdtemp()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-t", "16", f"{tmp}/%03d.png"], check=True)
frames = sorted(glob.glob(tmp + "/*.png"))           # file k (1-based) = frame k-1
def gray(i): return cv2.cvtColor(cv2.imread(frames[i]), cv2.COLOR_BGR2GRAY).astype(float)
def edge(line, guess, rng=4):
    d = [abs(line[i + 1] - line[i]) for i in range(guess - rng, guess + rng)]
    k = int(np.argmax(d)); return guess - rng + k + 0.5
# targets: approximate rect (from a manual look), first/last frame on screen (frame = t * 15)
T = {
    "product_category_list": ((1086, 276, 1277, 500), 156, 166),   # dropdown open 10.27 to 11.13 s
    "copy_json_button": ((426, 228, 553, 265), 202, 239),          # dialog loaded 13.47 s onward
    "dialog_ad_image": ((849, 163, 1014, 328), 202, 239),
    "card_r1c1": ((296, 318, 624, 646), 150, 172),
}
res = {}
for name, ((x0, y0, x1, y1), f0, f1) in T.items():
    meas = []
    for i in range(f0, f1 + 1):
        g = gray(i)
        cp = g[int(y0) + 8:int(y1) - 8].mean(axis=0); rp = g[:, int(x0) + 10:int(x1) - 10].mean(axis=1)
        meas.append([edge(cp, x0), edge(rp, y0), edge(cp, x1), edge(rp, y1)])
    m = np.array(meas); med = np.median(m, axis=0); spread = (m.max(axis=0) - m.min(axis=0))
    res[name] = dict(rect=[float(v) for v in med], frames=[f0, f1], t=[round(f0 / 15, 3), round(f1 / 15, 3)], edge_spread_px=[float(v) for v in spread])
    print(f"{name:24s} rect {[round(v, 1) for v in med]}  frames {f0}-{f1}  edge spread {spread.tolist()}")
json.dump(dict(source=os.path.basename(src), size=[1440, 810], fps=15, scroll_offset=0, targets=res,
               events={"dropdown_open": 10.27, "dropdown_close": 11.2, "dialog_open": 12.0, "json_loaded": 13.33, "copy_clicked": 14.93}),
          open(os.path.join(out, "tour_track_b2.json"), "w"), indent=1)

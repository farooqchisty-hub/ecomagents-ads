#!/usr/bin/env python3
"""Measure the real dashboard tour (reels-sb/src/tour.mp4, 1440x810, 15 fps) for the WS library beat.

1. Per-frame vertical scroll offset of the page (template match of 5 bands, conf >= 0.99 on every moving frame).
2. Stitch the page from the tour's own frames (rest frames pasted last), so the scroll can be re-driven at 30 fps.
3. Ad image rectangles measured on the stitched page with a sub-pixel edge search (max brightness step), then
   written back into tour-frame coordinates for every frame 0..105 (0 to 7.0 s): tour_track.json.
4. plate.jpg: the page cropped to x 262..1342 (1080 wide), used by compositions/ws-b1.html.

    ~/.venvs/adstudio/bin/python tools/track_tour.py <tour.mp4> <out_dir>
"""
import cv2, numpy as np, json, sys, os, subprocess, tempfile, glob
src, out = sys.argv[1], sys.argv[2]
tmp = tempfile.mkdtemp()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-t", "7.0", f"{tmp}/%03d.png"], check=True)
fs = sorted(glob.glob(tmp + "/*.png"))
imgs = [cv2.imread(f) for f in fs]; gray = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY).astype(np.float32) for i in imgs]
X0, X1 = 180, 1440
def shift(a, b):
    best = (-1, 0)
    for y0 in (60, 200, 350, 500, 620):
        res = cv2.matchTemplate(b[:, X0:X1], a[y0:y0 + 160, X0:X1], cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(res)
        if mx > best[0]: best = (mx, y0 - loc[1])
    return best
offs, conf, acc = [0], [1.0], 0
for i in range(1, len(gray)):
    if np.abs(gray[i] - gray[i - 1]).mean() < 0.5: offs.append(acc); conf.append(1.0); continue
    mx, dy = shift(gray[i - 1], gray[i]); acc += dy; offs.append(acc); conf.append(round(float(mx), 4))
H = 810 + max(offs)
page = np.zeros((H, 1440, 3), np.uint8)
for i in range(0, len(imgs), 2): page[offs[i]:offs[i] + 810] = imgs[i]
REST = []
for i in range(len(offs)):  # a rest = 10+ frames at the same offset
    if i + 9 < len(offs) and len(set(offs[i:i + 10])) == 1 and (not REST or REST[-1][1] != offs[i]): REST.append((i + 4, offs[i]))
for i, o in REST: page[o:o + 810] = imgs[i]
g = cv2.cvtColor(page, cv2.COLOR_BGR2GRAY).astype(float)
def edge(line, guess, rng=8):
    d = [abs(line[i + 1] - line[i]) for i in range(guess - rng, guess + rng)]
    return guess - rng + int(np.argmax(d)) + 0.5
ROWS, COLS = [318, 885, 1453, 2040, 2626], [296, 638, 980]
cards = []
for r, top in enumerate(ROWS):
    for c, left in enumerate(COLS):
        cp = g[top + 20:top + 300].mean(axis=0); rp = g[:, left + 20:left + 300].mean(axis=1)
        L, R, T = edge(cp, left), edge(cp, left + 328), edge(rp, top)
        B = edge(rp, top + 328) if top + 336 < H else T + 328
        cards.append(dict(id=f"r{r + 1}c{c + 1}", page=[L, T, R, B]))
# robust grid: column edges and row tops are shared, so take the median per column / row (dark ads have weak edges)
for c in range(3):
    col = [k for k in cards if k["id"].endswith(f"c{c + 1}")]
    L = float(np.median([k["page"][0] for k in col])); R = float(np.median([k["page"][2] for k in col]))
    for k in col: k["page"][0], k["page"][2] = L, R
for r in range(len(ROWS)):
    row = [k for k in cards if k["id"].startswith(f"r{r + 1}c")]
    T = float(np.median([k["page"][1] for k in row]))
    for k in row: k["page"][1], k["page"][3] = T, T + 328
frames = []
for i, o in enumerate(offs):
    vis = [dict(id=k["id"], rect=[k["page"][0], k["page"][1] - o, k["page"][2], k["page"][3] - o]) for k in cards if k["page"][3] - o > 0 and k["page"][1] - o < 810]
    frames.append(dict(frame=i, t=round(i / 15, 4), offset=o, match_conf=conf[i], cards=vis))
CROP = (262, 1342)
json.dump(dict(source=os.path.basename(src), size=[1440, 810], fps=15, rest=[dict(frame=i, t=round(i / 15, 3), offset=o) for i, o in REST],
               plate=dict(file="plate.jpg", crop_x=list(CROP), height=H), cards_page=cards, frames=frames),
          open(os.path.join(out, "tour_track.json"), "w"), indent=1)
cv2.imwrite(os.path.join(out, "plate.jpg"), page[:, CROP[0]:CROP[1]], [cv2.IMWRITE_JPEG_QUALITY, 93])
# self-check: re-measure rect edges directly in every rest frame (not the stitched page)
worst = 0
for i, o in REST:
    gg = gray[i].astype(float)
    for k in cards:
        L, T, R, B = k["page"][0], k["page"][1] - o, k["page"][2], k["page"][3] - o
        if T < 5 or B > 800: continue
        cp = gg[int(T) + 20:int(B) - 20].mean(axis=0); rp = gg[:, int(L) + 20:int(R) - 20].mean(axis=1)
        m = [edge(cp, int(L)), edge(rp, int(T)), edge(cp, int(R)), edge(rp, int(B))]
        dev = max(abs(a - b) for a, b in zip(m, [L, T, R, B])); worst = max(worst, dev)
        print(f"rest t={i / 15:.2f} off={o} {k['id']}: model {[L, T, R, B]} measured {m} dev {dev}")
print("REST", REST, "page height", H, "worst edge deviation px", worst)

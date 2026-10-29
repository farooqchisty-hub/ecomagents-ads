#!/usr/bin/env python3
"""Highlight-box alignment QA on the rendered WS test.

For every sampled frame: find the yellow box (border + corner brackets), then on 9 scanlines per side measure the gap
from the box's inner edge to the ad's edge (strongest luminance step 1..24 px inside). A box that sits on its card shows
the same small gap on all four sides (design: 8 page px = ~6.7 screen px, x camera scale); a floating box shows a
missing edge or uneven gaps. Also writes a zoomed crop sheet so the result can be checked by eye.

    ~/.venvs/adstudio/bin/python tools/qa_boxes.py test_ws.mp4 out_dir t1,t2,...
"""
import cv2, numpy as np, subprocess, sys, os, json
video, out, times = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
os.makedirs(out, exist_ok=True)

def grab(t):
    p = os.path.join(out, f"f_{t:06.2f}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", p], check=True)
    return cv2.imread(p)

def measure(img):
    b, g, r = [img[:, :, k].astype(int) for k in range(3)]
    yel = ((r > 200) & (g > 170) & (b < 150) & (r - b > 110)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(yel)
    if n < 2: return None
    k = 1 + int(np.argmax(st[1:, 4])); x, y, w, h, a = st[k]
    if w < 150 or h < 150: return None
    m = lab == k
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float)
    res = {"box": [int(x), int(y), int(w), int(h)]}
    def gap(line_vals, inner_start):
        # line_vals runs inward from the box's inner edge; strongest step in 1..24 px
        seg = line_vals[inner_start:inner_start + 26]
        if len(seg) < 6: return None
        d = np.abs(np.diff(seg)); i = int(np.argmax(d[1:24])) + 1
        return i + 0.5 if d[i] > 18 else None
    sides = {}
    for side in ("L", "R", "T", "B"):
        vals = []
        for f in np.linspace(0.3, 0.7, 9):
            if side in ("L", "R"):
                yy = int(y + h * f); row = m[yy]; xs = np.where(row)[0]
                if len(xs) < 2: continue
                if side == "L":
                    run = xs[xs < x + w / 2]; e = run.max() + 1 if len(run) else None
                    if e is None: continue
                    vals.append(gap(lum[yy, e:], 0))
                else:
                    run = xs[xs > x + w / 2]; e = run.min() - 1 if len(run) else None
                    if e is None: continue
                    vals.append(gap(lum[yy, :e + 1][::-1], 0))
            else:
                xx = int(x + w * f); col = m[:, xx]; ys = np.where(col)[0]
                if len(ys) < 2: continue
                if side == "T":
                    run = ys[ys < y + h / 2]; e = run.max() + 1 if len(run) else None
                    if e is None: continue
                    vals.append(gap(lum[e:, xx], 0))
                else:
                    run = ys[ys > y + h / 2]; e = run.min() - 1 if len(run) else None
                    if e is None: continue
                    vals.append(gap(lum[:e + 1, xx][::-1], 0))
        v = [q for q in vals if q is not None]
        sides[side] = (round(float(np.median(v)), 1), len(v)) if v else (None, 0)
    res["gap"] = sides
    return res

rows, crops = [], []
for t in times:
    img = grab(t); r = measure(img)
    rows.append(dict(t=t, **(r or {"box": None})))
    if r:
        x, y, w, h = r["box"]; c = img[max(y - 30, 0):y + h + 30, max(x - 30, 0):x + w + 30]
        c = cv2.resize(c, (360, int(360 * c.shape[0] / c.shape[1])))
        cv2.putText(c, f"{t:.2f}s", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        crops.append(c)
    print(f"t={t:6.2f}", "no box" if not r else f"box={r['box']} gaps L/R/T/B={[r['gap'][s][0] for s in 'LRTB']} (lines {[r['gap'][s][1] for s in 'LRTB']})")
json.dump(rows, open(os.path.join(out, "boxes.json"), "w"), indent=1)
if crops:
    hmax = max(c.shape[0] for c in crops); crops = [cv2.copyMakeBorder(c, 0, hmax - c.shape[0], 0, 0, cv2.BORDER_CONSTANT) for c in crops]
    per = 6; rowsimg = [np.hstack(crops[i:i + per] + [np.zeros_like(crops[0])] * (per - len(crops[i:i + per]))) for i in range(0, len(crops), per)]
    cv2.imwrite(os.path.join(out, "box_crops.jpg"), np.vstack(rowsimg), [cv2.IMWRITE_JPEG_QUALITY, 88])

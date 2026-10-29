#!/usr/bin/env python3
"""QA for the six presenter finals -> v5/qa/final_presenter/.
  boxes   tracked-box crops + gaps at the moments each box has landed (times from the same word stamps the build uses)
  hero    Cindera (WS) / Pawfull (EA) hero held at full size
  sync    presenter picture vs v3: frame offset of the presenter pixels (hook band, circle, close) must be 0
          voice vs v3: audio envelope cross-correlation offset must be 0
  layout  face / mic overlap: headline above the face, captions left of the mic, close card under the face
  plus    static_scan, black/flash, loudness, transcript (local whisper)
    python3 tools/qa_presenter.py
"""
import json, os, re, subprocess, sys
import numpy as np, cv2
V5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RS = os.path.dirname(V5); V3 = os.path.join(RS, "v3")
TL = json.load(open(os.path.join(V3, "presenter", "data", "timeline.json")))
LAY = json.load(open(os.path.join(V5, "mg", "presenter_layout.json")))
Q = os.path.join(V5, "qa", "final_presenter"); os.makedirs(Q, exist_ok=True)
PY = os.path.expanduser("~/.venvs/adstudio/bin/python")
MIC = {"ea_H11": (0.55, 0.50, 1.0, 0.78), "ea_H41": (0.55, 0.50, 1.0, 0.80), "ea_H51": (0.58, 0.56, 1.0, 0.82), "ea_C1": (0.60, 0.48, 1.0, 0.80),
       "ws_H11": (0.50, 0.52, 1.0, 0.92), "ws_H21": (0.58, 0.48, 1.0, 0.75), "ws_H31": (0.58, 0.46, 1.0, 0.78), "ws_C1": (0.62, 0.45, 1.0, 0.70)}
SPEED = 1.15
def norm(w): return re.sub(r"[^a-z0-9₹]", "", w.lower())
def at(words, needle, nth=0, end=False):
    hits = [(s, e) for w, s, e in words if norm(w) == norm(needle)]; return hits[nth][1 if end else 0]

def box_marks(ad, segs):
    """landed-box moments, body-local, per body seg"""
    b1, b2, b3 = (s["words"] for s in segs[1:4])
    if ad == "ws":
        lock = at(b1, "winning") - 0.05
        m1 = [lock + 0.7] + [m + 1.0 for m in (2.75, 4.95, 7.15, 12.9)] + [at(b1, "rebuilt") - 0.2 + 2.1]
        tcat = at(b2, "category,"); tprompt = at(b2, "prompt."); a0 = tcat - 1.15; a1 = tcat + 0.3; b1_ = tprompt + 0.08
        rA = (11.344 - 10.0) / (a1 - a0); rB = (15.0 - 11.344) / (b1_ - a1)
        m2 = [a0 + 0.27 / rA + 0.12 + 0.45, a1 + (13.47 - 11.344) / rB + 0.45, a1 + (14.93 - 11.344) / rB + 0.5]
        tb = [at(b3, "blueprint,") - 0.4, at(b3, "playbooks,") - 0.4, at(b3, "library,") - 0.4, at(b3, "file.") - 0.5]
        m3 = [t + 0.45 for t in tb]
    else:
        m1 = [at(b1, "skills,") + 0.1] + [at(b1, k) + 0.3 for k in ("ads,", "offers,", "product", "retention,", "profit")] + [at(b1, "Brand") + 0.4]
        m2 = []
        m3 = [at(b3, "agent") + 0.4, at(b3, "welcome") + 0.45, at(b3, "cart") + 0.45, at(b3, "post-purchase") + 0.45, at(b3, "win-back,") + 0.45]
    return [m1, m2, m3]

def frame_at(path, t, crop=None):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    f = np.frombuffer(r.stdout, np.uint8).reshape(1920, 1080).astype(np.float32)
    return f if crop is None else f[crop[1]:crop[3], crop[0]:crop[2]]

def sync_picture(cut):
    """presenter pixels v5 vs v3 at a few moments; best frame offset in -3..3 (0 = unchanged)"""
    c = TL[cut]; segs = c["segs"]; lay = LAY[cut]; v3 = os.path.join(V3, "out", f"{cut}.mp4"); v5 = os.path.join(V5, "out", f"{cut}.mp4")
    sh = lay["shift"]; f = segs[0]["face"]
    face_h = (f["x0"] + 10, f["y0"] + sh + 10, f["x1"] - 10, min(f["y1"] + sh - 10, 1900))
    circ = (90, 1188, 358, 1456)
    t_body = segs[0]["frames"] / 30; t_close = sum(s["frames"] for s in segs[:4]) / 30; fc = segs[4]["face"]
    face_c = (fc["x0"] + 10, fc["y0"] + 10, fc["x1"] - 10, fc["y1"] - 10)
    res = []
    for name, t0, crop in (("hook", segs[0]["dur"] * 0.5, face_h), ("body", t_body + 5.0, circ), ("body", t_body + 30.0, circ), ("close", t_close + 1.5, face_c)):
        rd = np.concatenate([(frame_at(v3, t0 + (k + 1) / 30, crop) - frame_at(v3, t0 + k / 30, crop)).ravel() for k in range(4)]); scores = {}
        for o in range(-3, 4):
            cd = np.concatenate([(frame_at(v5, t0 + (o + k + 1) / 30, crop) - frame_at(v5, t0 + (o + k) / 30, crop)).ravel() for k in range(4)])
            scores[o] = float(np.corrcoef(rd, cd)[0, 1])
        best = max(scores, key=scores.get); res.append(dict(part=name, t=round(t0, 2), best_offset_frames=best, motion_corr=round(scores[best], 3), motion_corr_at_0=round(scores[0], 3)))
    return res

def sync_audio(cut):
    def env(p):
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True)
        a = np.abs(np.frombuffer(r.stdout, np.int16).astype(np.float32)); n = len(a) // 80
        return a[:n * 80].reshape(n, 80).mean(axis=1)          # 10 ms envelope
    a, b = env(os.path.join(V3, "presenter", "work", "mix", f"{cut}_vo.wav")), env(os.path.join(V5, "out", f"{cut}.mp4"))
    n = min(len(a), len(b)); a, b = a[:n] - a[:n].mean(), b[:n] - b[:n].mean()
    best = max(range(-20, 21), key=lambda k: float(np.dot(a[max(k, 0):n + min(k, 0)], b[max(-k, 0):n - max(k, 0)])))
    return dict(voice_offset_ms=best * 10)

def layout_check(cut):
    c = TL[cut]; ad = c["ad"]; lay = LAY[cut]; seg = c["segs"][0]; f = seg["face"]; take = seg["take"]
    mic = MIC[f"{ad}_{take}"]; mx0 = mic[0] * 1080
    cx, cy, cw = lay["cap"]
    close = LAY[f"{ad}_close"]; fcl = c["segs"][4]["face"]
    return dict(headline_bottom=lay["hl_bottom"], face_top=lay["face_top_out"], headline_clear_of_face_px=lay["face_top_out"] - lay["hl_bottom"],
                captions_right_edge=cx + cw, mic_left=round(mx0), captions_clear_of_mic_px=round(mx0 - (cx + cw)),
                captions_top=cy, face_bottom=f["y1"] + lay["shift"], captions_below_face_px=cy - (f["y1"] + lay["shift"]),
                close_card_top=close["card_top"], close_face_bottom=fcl["y1"], close_card_clear_of_face_px=close["card_top"] - fcl["y1"])

if __name__ == "__main__":
    report = {}
    for cut, c in TL.items():
        ad = c["ad"]; segs = c["segs"]; fin = os.path.join(V5, "final", f"{cut}__A_tech_house.mp4")
        tb = segs[0]["frames"] / 30
        offs = [tb, tb + segs[1]["frames"] / 30, tb + (segs[1]["frames"] + segs[2]["frames"]) / 30]
        marks = box_marks(ad, segs)
        T = [(o + t) / SPEED for o, ms in zip(offs, marks) for t in ms]
        r = subprocess.run([PY, os.path.join(V5, "tools", "qa_boxes.py"), fin, os.path.join(Q, f"boxes_{cut}"), ",".join(f"{t:.3f}" for t in T), "1135"], capture_output=True, text=True)
        open(os.path.join(Q, f"boxes_{cut}.txt"), "w").write(re.sub(r"\(lines.*", "", r.stdout))
        for p in os.listdir(os.path.join(Q, f"boxes_{cut}")):
            if p.startswith("f_"): os.remove(os.path.join(Q, f"boxes_{cut}", p))
        # hero: WS Cindera in body 2 (lands on "comes"), EA Pawfull from body 2 into body 3
        if ad == "ws":
            h0 = (offs[1] + at(segs[2]["words"], "comes") - 0.5) / SPEED; h1 = (offs[2] + 0.3) / SPEED
            hero = subprocess.run([PY, os.path.join(V5, "tools", "hero_hold.py"), fin, os.path.join(V5, "mg", "assets", "pairs", "cindera_ad.jpg"), "480", f"{h0:.2f}", f"{h1:.2f}", f"{cut} Cindera hero"], capture_output=True, text=True).stdout.strip()
        else:
            h0 = (offs[1] + at(segs[2]["words"], "drafts") - 0.5) / SPEED; h1 = (offs[2] + 1.6) / SPEED
            hero = subprocess.run([PY, os.path.join(V5, "tools", "hero_hold.py"), fin, os.path.join(V5, "mg", "assets", "pairs", "pawfull_ad.jpg"), str(round(820 * 0.9716)), f"{h0:.2f}", f"{h1:.2f}", f"{cut} Pawfull hero"], capture_output=True, text=True).stdout.strip()
        st = subprocess.run([PY, os.path.join(V5, "tools", "static_scan.py"), fin], capture_output=True, text=True).stdout
        ld = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", fin, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        I = re.findall(r"I:\s+(-?[\d.]+) LUFS", ld)[-1]; pk = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", ld)[-1]
        report[cut] = dict(hero=hero, static=st.strip().splitlines(), loudness_I=float(I), true_peak=float(pk),
                           sync_picture=sync_picture(cut), sync_voice=sync_audio(cut), layout=layout_check(cut))
        print(cut, json.dumps(report[cut], ensure_ascii=False)[:900])
    json.dump(report, open(os.path.join(Q, "report.json"), "w"), indent=1, ensure_ascii=False)

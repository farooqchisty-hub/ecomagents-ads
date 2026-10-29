#!/usr/bin/env python3
"""Speed a finished v3 cut and re-score it with a new music bed whose drop lands on the hook/body join.

    python3 remix_v4.py CUT MUSIC_OPTION [--speed 1.15] [--gap 10]
CUT is a v3 cut name (EA-1_H1, WS-2_H1, ...). MUSIC_OPTION is a file stem in ../music. Output ../out/<CUT>__<opt>.mp4.
Voice: rebuilt clean (faceless: narration clips at their assembly.json placements; presenter: the v3 voice stem),
sped with atempo (pitch kept). Picture: setpts/speed, back to 30 fps. Music: aligned so its drop hits the new join,
sidechain-ducked by the voice, level set so the voice sits GAP dB above it while speaking, 1.2 s fade out, -14 LUFS.
"""
import json, os, re, subprocess, sys, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rms import rms_db
V4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V3 = os.path.join(os.path.dirname(V4), "v3")
A = sys.argv[1:]; CUT, OPT = A[0], A[1]
SPEED = float(A[A.index("--speed") + 1]) if "--speed" in A else 1.15
GAP = float(A[A.index("--gap") + 1]) if "--gap" in A else 10.0
TMP = os.path.join(V4, "work"); os.makedirs(TMP, exist_ok=True); OUT = os.path.join(V4, "out"); os.makedirs(OUT, exist_ok=True)
def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2000:])
    return r
def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)
def momentary(p):
    r = run(["ffmpeg", "-hide_banner", "-i", p, "-af", "ebur128=framelog=verbose", "-f", "null", "-"])
    return [(float(t), float(m)) for t, m in re.findall(r"t:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+)", r.stderr)]
src = os.path.join(V3, "out", f"{CUT}.mp4"); total = dur(src)
vo = os.path.join(TMP, f"{CUT}_vo.wav")
if CUT[:4] in ("EA-2", "WS-2"):
    asm = json.load(open(os.path.join(V3, "out", "assembly.json")))[CUT]; join = asm["join"]
    ins, fl = [], []
    for k, (key, at) in enumerate(asm["vo"]):
        ins += ["-i", os.path.join(V3, "vo", f"{key}.mp3")]
        tr = f"atrim=start={-at:.4f}," if at < 0 else ""
        fl.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{tr}asetpts=PTS-STARTPTS,adelay={max(at,0)*1000:.1f}:all=1[v{k}]")
    n = len(asm["vo"])
    fl.append("".join(f"[v{k}]" for k in range(n)) + f"amix=inputs={n}:normalize=0:dropout_transition=0,apad,atrim=0:{total:.4f}[o]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[o]", "-c:a", "pcm_s24le", vo])
else:
    tl = json.load(open(os.path.join(V3, "presenter", "data", "timeline.json")))[CUT]
    join = next(s["out_start"] for s in tl["segs"] if s["kind"] != "hook")
    run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(V3, "presenter", "work", "mix", f"{CUT}_vo.wav"), "-af", f"apad,atrim=0:{total:.4f}", "-c:a", "pcm_s24le", vo])
new_total, new_join = total / SPEED, join / SPEED
vs = os.path.join(TMP, f"{CUT}_vo_fast.wav")
run(["ffmpeg", "-v", "error", "-y", "-i", vo, "-af", f"atempo={SPEED},aresample=48000", "-c:a", "pcm_s24le", vs])
# music drop (never earlier than the join, so music plays from frame 0): biggest rise in loudness (next 2 s vs previous 2 s) between 4 and 16 s
mus = os.path.join(V4, "music", f"{OPT}.mp3"); R = rms_db(mus, 0.25, t=20)
def lvl(t0, t1):
    xs = [v for t, v in R if t0 <= t < t1]; return statistics.mean(xs) if xs else -90
drop = max((lvl(t, t + 2) - lvl(t - 2, t), t) for t in [x / 4 for x in range(16, 64)] if t >= new_join)[1]
off = drop - new_join          # seconds of music to skip so the drop lands on the join
mtrim = f"atrim=start={off:.3f}," if off > 0 else ""
mdel = f"adelay={-off*1000:.0f}:all=1," if off < 0 else ""
# pass 1: ducked music at unity to measure the speech gap
duck = os.path.join(TMP, f"{CUT}__{OPT}_duck.wav")
run(["ffmpeg", "-v", "error", "-y", "-i", mus, "-i", vs, "-filter_complex",
     f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,{mtrim}asetpts=PTS-STARTPTS,{mdel}apad,atrim=0:{new_total:.4f}[m];"
     f"[1:a]asplit=1[key];[m][key]sidechaincompress=threshold=0.04:ratio=3:attack=25:release=350:knee=4[md]",
     "-map", "[md]", "-c:a", "pcm_s24le", duck])
VV, BB = rms_db(vs, 0.25), dict(rms_db(duck, 0.25))
diffs = [v - BB[t] for t, v in VV if v > -38 and t in BB and BB[t] > -80]
gain = statistics.median(diffs) - GAP if diffs else -10
pre = os.path.join(TMP, f"{CUT}__{OPT}_pre.wav")
run(["ffmpeg", "-v", "error", "-y", "-i", vs, "-i", duck, "-filter_complex",
     f"[1:a]volume={gain:.2f}dB,afade=t=out:st={new_total-1.2:.3f}:d=1.2[b];[0:a][b]amix=inputs=2:normalize=0:duration=first[x]", "-map", "[x]", "-c:a", "pcm_s24le", pre])
r = run(["ffmpeg", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
m = json.loads(re.search(r"\{[^{}]+\}", r.stderr[r.stderr.rfind("[Parsed_loudnorm"):]).group(0))
mix = os.path.join(TMP, f"{CUT}__{OPT}_mix.wav")
run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s24le", mix])
out = os.path.join(OUT, f"{CUT}__{OPT}.mp4")
run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", mix, "-filter_complex", f"[0:v]setpts=PTS/{SPEED},fps=30,format=yuv420p[v]", "-map", "[v]", "-map", "1:a",
     "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{new_total:.4f}", "-movflags", "+faststart", out])
print(json.dumps({"cut": CUT, "music": OPT, "speed": SPEED, "total": round(new_total, 2), "join": round(new_join, 2), "drop_in_track": drop, "music_skip": round(off, 2), "bed_gain_db": round(gain, 2)}))

#!/usr/bin/env python3
"""Lay the real narration on the silent v5 renders exactly as v3/out/assembly.json places it (no music),
normalise to -14 LUFS / -1.5 dBTP, encode H.264 + AAC, then make the 1.15x previews (setpts/1.15, atempo 1.15).

    python3 tools/mix.py
"""
import json, os, re, subprocess
V5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V3 = os.path.join(os.path.dirname(V5), "v3")
A = json.load(open(os.path.join(V3, "out", "assembly.json")))
ws = dict(A["WS-2_H1"]["vo"]); ea = dict(A["EA-2_H4"]["vo"])
# WS test = WS-2_H1 from 0 to the end of body 1; EA test = body 2 alone, shifted so its scene starts at 0
EA_SCENE_START = ea["ea2_b2"] + 0.0138          # assembly places ea2_b2 at scene start + vo_at (-0.0138)
JOBS = {
    "test_ws": ("mg/renders/test_ws_silent.mp4", [("ws2_h1", ws["ws2_h1"]), ("ws2_b1", ws["ws2_b1"])]),
    "test_ea": ("mg/renders/test_ea_silent.mp4", [("ea2_b2", ea["ea2_b2"] - EA_SCENE_START)]),
}

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-2500:])
    return r

def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)

for name, (silent, vo) in JOBS.items():
    sv = os.path.join(V5, silent); total = dur(sv); tmp = os.path.join(V5, "mg", "renders", f"{name}_vo.wav")
    inputs, fl = [], []
    for k, (key, at) in enumerate(vo):
        inputs += ["-i", os.path.join(V3, "vo", f"{key}.mp3")]
        trim = f"atrim=start={-at:.4f}," if at < 0 else ""
        fl.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}asetpts=PTS-STARTPTS,adelay={max(at, 0) * 1000:.1f}:all=1[v{k}]")
    fl.append("".join(f"[v{k}]" for k in range(len(vo))) + f"amix=inputs={len(vo)}:normalize=0:dropout_transition=0,apad,atrim=0:{total:.4f}[mix]")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fl), "-map", "[mix]", "-c:a", "pcm_s24le", tmp])
    r = run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = json.loads(re.search(r"\{[^{}]+\}", r.stderr[r.stderr.rfind("[Parsed_loudnorm"):]).group(0))
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
    out = os.path.join(V5, f"{name}.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", sv, "-i", tmp, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "slow",
         "-pix_fmt", "yuv420p", "-af", ln, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out])
    fast = os.path.join(V5, f"{name}_115.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", out, "-filter_complex", "[0:v]setpts=PTS/1.15[v];[0:a]atempo=1.15[a]", "-map", "[v]", "-map", "[a]",
         "-r", "30", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", fast])
    print(name, f"{dur(out):.3f}s", "| 1.15x", f"{dur(fast):.3f}s", "| VO at", [(k, round(a, 3)) for k, a in vo])

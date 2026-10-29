#!/usr/bin/env python3
"""Lay the presenter takes into the v5 graphics. Picture chain identical to v3/presenter/tools/composite.py (same trims,
same frame counts, same per-take colour gain, same shift, same circle crop and mask); only the overlay/body renders are v5.
Sound: the v3 voice stem v3/presenter/work/mix/<CUT>_vo.wav (built from the same trims), so lip sync is unchanged.
remix_v4 rebuilds the final mix from that same stem.

    python3 tools/composite_v5.py [EA-1_H1 ...]        # -> v5/out/<CUT>.mp4
"""
import json, os, subprocess, sys
V5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V3P = os.path.join(os.path.dirname(V5), "v3", "presenter")
sys.path.insert(0, os.path.join(V3P, "tools")); sys.dont_write_bytecode = True
import composite as C3                        # reuse vtake, circle_crop, mask, run (v3 code, untouched)
FPS = 30; CIRC = C3.CIRC
REN = os.path.join(V5, "mg", "renders", "presenter"); OUT = os.path.join(V5, "out")
LAY = json.load(open(os.path.join(V5, "mg", "presenter_layout.json")))
TL = json.load(open(os.path.join(V3P, "data", "timeline.json")))

def cut(name):
    c = TL[name]; ad = c["ad"]; segs = c["segs"]; lay = LAY[name]
    total_frames = sum(s["frames"] for s in segs); total = total_frames / FPS
    nb = sum(s["frames"] for s in segs[1:4])
    ins = []
    for s in segs: ins += ["-i", s["path"]]
    ins += ["-i", os.path.join(REN, f"{lay['id']}.mov"), "-i", os.path.join(REN, f"p-{ad}-body.mp4"), "-i", os.path.join(REN, f"p-{ad}-close.mov"),
            "-loop", "1", "-i", C3.mask(), "-i", os.path.join(V3P, "work", "mix", f"{name}_vo.wav")]
    sh = lay["shift"]; up = "scale=1080:1920:flags=lanczos"
    fl = [C3.vtake(0, segs[0], "hp", up),
          f"[hp]crop=1080:{1920 - sh}:0:0,pad=1080:1920:0:{sh}:0x020403[hpp]",
          f"[5:v]setpts=PTS-STARTPTS,trim=end_frame={segs[0]['frames']}[ho]",
          f"[hpp][ho]overlay=0:0:format=auto:eof_action=repeat,format=yuv420p[hv]"]
    for k in range(1, 4):
        x, y, side, d = C3.circle_crop(segs[k])
        fl.append(C3.vtake(k, segs[k], f"c{k}", f"crop={side}:{side}:{x}:{y},scale={d}:{d}:flags=lanczos"))
    fl += [f"[c1][c2][c3]concat=n=3:v=1:a=0,format=yuv420p[cc]",
           f"[8:v]format=gray,fps={FPS},trim=end_frame={nb}[mk]",
           f"[cc][mk]alphamerge[ca]",
           f"[6:v]setpts=PTS-STARTPTS,fps={FPS},trim=end_frame={nb}[bb]",
           f"[bb][ca]overlay={CIRC[0]}:{CIRC[1]}:format=auto,format=yuv420p[bv]",
           C3.vtake(4, segs[4], "cp", up),
           f"[7:v]setpts=PTS-STARTPTS,trim=end_frame={segs[4]['frames']}[co]",
           f"[cp][co]overlay=0:0:format=auto:eof_action=repeat,format=yuv420p[cv]",
           f"[hv][bv][cv]concat=n=3:v=1:a=0,format=yuv420p,setsar=1[v]"]
    out = os.path.join(OUT, f"{name}.mp4")
    C3.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[v]", "-map", "9:a",
            "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "60",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.4f}", "-movflags", "+faststart", out])
    joins, t = [], 0
    for s in segs[:-1]: t += s["frames"]; joins.append(round(t / FPS, 4))
    res = dict(cut=name, total=round(total, 4), frames=total_frames, joins=joins)
    print(res); return res

if __name__ == "__main__":
    for n in sys.argv[1:] or ["EA-1_H1", "EA-1_H4", "EA-1_H5", "WS-1_H1", "WS-1_H2", "WS-1_H3"]: cut(n)

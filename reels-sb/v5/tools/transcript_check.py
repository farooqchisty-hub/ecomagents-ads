#!/usr/bin/env python3
"""Transcript spot-check: local whisper (hyperframes transcribe, whisper.cpp small.en) on a final cut vs the approved
script (v3/vo/lines.json). Prints word error rate after normalising numbers the way the voice reads them.

    python3 tools/transcript_check.py <final.mp4> <key,key,...> <out.json>
"""
import json, os, re, subprocess, sys, difflib, tempfile
V5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(os.path.dirname(V5), "v3", "vo", "lines.json")))
src, keys, out = sys.argv[1], sys.argv[2].split(","), sys.argv[3]
if keys[0].startswith("TL:"):     # presenter cut: the approved take texts from v3/presenter/data/timeline.json
    TLJ = json.load(open(os.path.join(os.path.dirname(V5), "v3", "presenter", "data", "timeline.json")))
    ref = " ".join(s["text"] for s in TLJ[keys[0][3:]]["segs"])
else:
    ref = " ".join(L[k] for k in keys)
d = tempfile.mkdtemp()
wav = os.path.join(d, "a.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
r = subprocess.run(["npx", "hyperframes", "transcribe", wav, "--dir", d, "--json", "--engine", "whisper", "--model", "small.en"], capture_output=True, text=True, cwd=d)
try:
    meta = json.loads(r.stdout[r.stdout.find("{"):].splitlines()[0])
    data = json.load(open(meta["transcriptPath"]))
except Exception:
    sys.exit("transcribe failed: " + r.stdout[-500:] + r.stderr[-1500:])
words = data if isinstance(data, list) else (data.get("words") or [w for s in data.get("segments", []) for w in s.get("words", [])])
hyp = " ".join((w.get("text") or w.get("word") or "").strip() for w in words)
NUM = {"6.99": "six ninety nine", "₹699": "six ninety nine rupees", "1,169": "eleven hundred and sixty nine", "1169": "eleven hundred and sixty nine", "5,000": "five thousand", "5000": "five thousand",
       "₹1": "one rupee", "5x": "five times", "16": "sixteen", "14": "fourteen"}
def norm(s):
    s = s.lower()
    for a, b in NUM.items(): s = s.replace(a.lower(), " " + b + " ")
    s = s.replace("-", " ")
    return [w for w in re.sub(r"[^a-z0-9' ]", " ", s).split() if w]
R, Hy = norm(ref), norm(hyp)
sm = difflib.SequenceMatcher(None, R, Hy, autojunk=False)
err = sum(max(i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal")
diffs = [(t, " ".join(R[i1:i2]), " ".join(Hy[j1:j2])) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal"]
res = dict(file=os.path.basename(src), ref=ref, hyp=hyp, ref_words=len(R), wer=round(err / max(len(R), 1), 4), diffs=diffs)
json.dump(res, open(out, "w"), indent=1, ensure_ascii=False)
print(f"{os.path.basename(src)}: WER {res['wer']:.3f} ({err}/{len(R)})  diffs: {diffs}")

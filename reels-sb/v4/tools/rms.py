import subprocess, array, math, sys
def rms_db(path, hop=0.25, sr=8000, t=None):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr)] + (["-t", str(t)] if t else []) + ["-f", "s16le", "-"]
    a = array.array("h", subprocess.run(cmd, capture_output=True).stdout); n = int(hop * sr); out = []
    for i in range(0, len(a) - n + 1, n):
        s = sum(x * x for x in a[i:i + n]) / n; out.append((round(i / sr, 2), 10 * math.log10(s / 32768**2 + 1e-12)))
    return out
if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = rms_db(p, 0.5, t=16); print(p.split("/")[-1], " ".join(f"{v:.0f}" for _, v in r))

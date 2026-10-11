from collections import defaultdict

import numpy as np
from scipy.signal import find_peaks, savgol_filter

from cnc_common import ARTIFACT_WINDOW, iter_samples, load_sample

SEGMENTS = [(250, ARTIFACT_WINDOW[0]), (ARTIFACT_WINDOW[1], 1500)]
SMOOTH_POINTS = (41, 61, 101)
PROMINENCE = 0.3
BIN = 10


def minima(w, t, smooth):
    found = []
    for lo, hi in SEGMENTS:
        m = (w >= lo) & (w <= hi)
        ww, tt = w[m], t[m]
        k = min(smooth, len(tt) - (1 - len(tt) % 2))
        res = tt - savgol_filter(tt, k, 2)
        idx, _ = find_peaks(-res, prominence=PROMINENCE, width=3)
        edge = (ww[idx] > lo + 10) & (ww[idx] < hi - 10)
        found += list(ww[idx][edge])
    return found


samples = list(iter_samples())
for smooth in SMOOTH_POINTS:
    counts = defaultdict(lambda: defaultdict(int))
    for ph, dry, rep, num in samples:
        w, t = load_sample(num)
        bins = {int(x // BIN * BIN) for x in minima(w, t, smooth)}
        for b in bins:
            counts[b][ph] += 1
    print(f"=== smoothing window {smooth} points ({2 * smooth} nm) ===")
    print(f"{'bin (nm)':>9}  pH2.5  pH4.5  pH6.5  pH8.5  total")
    for b in sorted(counts):
        c = counts[b]
        total = sum(c.values())
        if total >= 5:
            print(f"{b:>5}-{b + BIN:<4} {c[2.5]:>5} {c[4.5]:>6} {c[6.5]:>6} {c[8.5]:>6} {total:>6}")
    print()

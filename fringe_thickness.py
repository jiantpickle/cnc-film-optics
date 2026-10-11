import numpy as np
from scipy.signal import find_peaks, savgol_filter

from cnc_common import iter_samples, load_sample

LO, HI = 880, 1380
N_VALUES = (1.50, 1.55, 1.60)


def fringe_signal(w, t):
    m = (w >= LO) & (w <= HI)
    ww, tt = w[m], t[m]
    return ww, tt - savgol_filter(tt, 81, 2)


def optical_thickness(ww, osc):
    peaks, _ = find_peaks(osc, prominence=0.1)
    troughs, _ = find_peaks(-osc, prominence=0.1)
    idx = np.sort(np.concatenate([peaks, troughs]))
    if len(idx) < 6:
        return np.nan, np.nan, len(idx)
    k = 1.0 / ww[idx]
    half_orders = np.arange(len(idx)) * 0.5
    slope, icpt = np.polyfit(k, half_orders, 1)
    pred = slope * k + icpt
    r2 = 1 - np.sum((half_orders - pred) ** 2) / np.sum((half_orders - half_orders.mean()) ** 2)
    return abs(slope) / 2, r2, len(idx)


samples = list(iter_samples())
osc_rms = {}
for ph, dry, rep, num in samples:
    ww, osc = fringe_signal(*load_sample(num))
    osc_rms[num] = np.sqrt(np.mean(osc ** 2))

floor = max(osc_rms[n] for ph, d, r, n in samples if ph in (6.5, 8.5))
threshold = 3 * floor
print(f"Noise floor (max RMS, pH 6.5/8.5): {floor:.3f} %T -> threshold {threshold:.3f} %T\n")

header = f"{'sample':>6} {'pH':>4} {'dry':>3} {'RMS':>6} {'pass':>5} {'extrema':>7} {'nd (nm)':>9} {'R2':>7} "
print(header + " ".join(f"d@n={n:.2f}" for n in N_VALUES))
results = {}
for ph, dry, rep, num in samples:
    if ph not in (2.5, 4.5):
        continue
    ok = osc_rms[num] > threshold
    nd, r2, n_ext = optical_thickness(*fringe_signal(*load_sample(num))) if ok else (np.nan, np.nan, 0)
    ds = " ".join(f"{nd / n / 1000:9.2f}" if ok and not np.isnan(nd) else f"{'-':>9}" for n in N_VALUES)
    print(f"{num:>6} {ph:>4} {dry:>3} {osc_rms[num]:6.3f} {str(ok):>5} {n_ext:>7} "
          f"{nd if ok else float('nan'):9.0f} {r2:7.4f} {ds}")
    if ok and not np.isnan(nd):
        results.setdefault(ph, []).append(nd)

print()
for ph, vals in results.items():
    vals = np.array(vals)
    for n in N_VALUES:
        d = vals / n / 1000
        sd = d.std(ddof=1) if len(d) > 1 else 0
        print(f"pH {ph}: n={n:.2f}  d = {d.mean():.2f} +- {sd:.2f} um  (films = {len(d)})")

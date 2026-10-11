import numpy as np

from cnc_common import iter_samples, load_asc, load_sample

CHANGEOVER = 860.8
BELOW = (800, 856)
ABOVE = (866, 930)
BLANK_FILE = "blank_no_sample.asc"


def step(w, t):
    lo = (w >= BELOW[0]) & (w <= BELOW[1])
    hi = (w >= ABOVE[0]) & (w <= ABOVE[1])
    p_lo = np.polyfit(w[lo], t[lo], 1)
    p_hi = np.polyfit(w[hi], t[hi], 1)
    noise = max(np.std(t[lo] - np.polyval(p_lo, w[lo])), np.std(t[hi] - np.polyval(p_hi, w[hi])))
    base = np.polyval(p_lo, CHANGEOVER)
    return np.polyval(p_hi, CHANGEOVER) - base, base, noise


w, t = load_asc(BLANK_FILE)
s, base, noise = step(w, t)
print(f"Blank: step {s:+.3f} %T, relative {100 * s / base:.2f} %\n")

rel, n_sig = [], 0
for ph, dry, rep, num in iter_samples():
    s, base, noise = step(*load_sample(num))
    rel.append(100 * s / base)
    n_sig += abs(s) > 3 * noise
    print(f"{num}  pH {ph}  dry {dry}  step {s:+.3f} %T  relative {100 * s / base:+.2f} %  noise {noise:.3f}")

rel = np.array(rel)
print(f"\nFilms with |step| > 3 x noise: {n_sig} of {len(rel)}")
print(f"Relative step: {rel.mean():.2f} +- {rel.std(ddof=1):.2f} %")

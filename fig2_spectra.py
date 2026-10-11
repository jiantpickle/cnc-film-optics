import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cnc_common import ARTIFACT_WINDOW, PH_LABELS, iter_samples, load_sample, set_figure_style

set_figure_style()

PH_ORDER = [2.5, 4.5, 6.5, 8.5]
PH_COLORS = {2.5: "#555555", 4.5: "#0072B2", 6.5: "#D55E00", 8.5: "#009E73"}
WMIN = 250

spectra = {ph: [] for ph in PH_ORDER}
for ph, dry, rep, num in iter_samples():
    w, t = load_sample(num)
    keep = w >= WMIN
    spectra[ph].append((w[keep], t[keep]))

fig, axes = plt.subplots(2, 2, figsize=(7.5, 5.6), sharex=True, sharey=True)
for ax, ph, letter in zip(axes.ravel(), PH_ORDER, "ABCD"):
    for w, t in spectra[ph]:
        ax.plot(w, t, color=PH_COLORS[ph], lw=0.7, alpha=0.8)
    ax.axvspan(*ARTIFACT_WINDOW, color="0.9", zorder=0)
    ax.set_title(f"pH {PH_LABELS[ph]}", fontsize=10)
    ax.text(0.02, 0.95, letter, transform=ax.transAxes, fontweight="bold", fontsize=12, va="top")
    ax.text(0.97, 0.05, f"n = {len(spectra[ph])}", transform=ax.transAxes, fontsize=9,
            ha="right", va="bottom")
    ax.set_xlim(WMIN, 1500)
    ax.set_ylim(45, 96)
    ax.grid(alpha=0.3, lw=0.5)

fig.supxlabel("Wavelength (nm)", fontsize=10)
fig.supylabel("Transmittance (%)", fontsize=10)
fig.tight_layout()
fig.savefig("Figure2.png", dpi=300)
print("Saved Figure2.png")

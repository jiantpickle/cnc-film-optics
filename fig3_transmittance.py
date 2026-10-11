import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cnc_common import (DRY_COLORS, DRY_LABELS, DRY_MARKERS, PH_LABELS, features, iter_samples,
                        load_sample, set_figure_style)

set_figure_style()

SHOW_PH25 = True
PH_LEVELS = ([2.5] if SHOW_PH25 else []) + [4.5, 6.5, 8.5]
OFFSET = {0: -0.22, 1: 0.0, 2: 0.22}

data = {}
for ph, dry, rep, num in iter_samples():
    data.setdefault((ph, dry), []).append(features(*load_sample(num)))

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.4))
panels = [("A", 0, "Transmittance at 600 nm (%)"), ("B", 1, "Transmittance at 300 nm (%)")]
for ax, (letter, k, ylabel) in zip(axes, panels):
    for i, ph in enumerate(PH_LEVELS):
        for dry in (0, 1, 2):
            vals = np.array([v[k] for v in data.get((ph, dry), [])])
            if vals.size == 0:
                continue
            x = i + OFFSET[dry]
            color = "0.55" if ph == 2.5 else DRY_COLORS[dry]
            ax.scatter(np.full(vals.size, x), vals, s=18, color=color, marker=DRY_MARKERS[dry],
                       edgecolor="black", linewidth=0.4, zorder=3,
                       label=DRY_LABELS[dry] if (letter == "A" and ph == 4.5) else None)
            ax.errorbar(x, vals.mean(), yerr=vals.std(ddof=1) if vals.size > 1 else 0,
                        fmt="_", color="black", ms=12, capsize=3, lw=1, zorder=4)
    if SHOW_PH25:
        ax.axvline(0.5, color="0.4", ls="--", lw=0.8)
    ax.set_xticks(range(len(PH_LEVELS)))
    ax.set_xticklabels([f"pH {PH_LABELS[p]}" for p in PH_LEVELS])
    ax.set_ylabel(ylabel)
    ax.text(-0.18, 1.02, letter, transform=ax.transAxes, fontweight="bold", fontsize=12)
    ax.grid(axis="y", alpha=0.3, lw=0.5)

axes[0].legend(frameon=False, fontsize=8, loc="upper right")
fig.tight_layout()
fig.savefig("Figure3.png", dpi=300)
print("Saved Figure3.png")

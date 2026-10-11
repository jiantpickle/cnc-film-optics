from pathlib import Path

import matplotlib
from matplotlib.patches import Circle, Wedge
from PIL import Image, ImageOps

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cnc_common import DRY_LABELS, set_figure_style

set_figure_style()

PHOTO_DIR = Path("photos")
PANELS = [
    ("A", "fig1A_all_films.jpeg", (0.128, 0.248, 0.501, 0.559)),
    ("B", "fig1B_pH2.64_film.jpeg", (0.179, 0.163, 0.769, 0.753)),
    ("C", "fig1C_pH4.42_film_dark_background.jpeg", (0.210, 0.435, 0.800, 0.890)),
]
COVER_FRACTION = {0: 0.0, 1: 1 / 3, 2: 2 / 3}
DISH_RADIUS = 1.0
PAPER_RADIUS = 1.12
SPACING = 3.2


def crop_fraction(img, box):
    w, h = img.size
    left, top, right, bottom = box
    return img.crop((round(left * w), round(top * h), round(right * w), round(bottom * h)))


def label(ax, letter, color="white", box=True):
    ax.text(0.01, 0.97, letter, transform=ax.transAxes, fontweight="bold", fontsize=12,
            color=color, va="top", ha="left",
            bbox={"facecolor": "black", "alpha": 0.5, "pad": 2, "linewidth": 0} if box else None)


fig = plt.figure(figsize=(7.5, 3.2))
grid = fig.add_gridspec(2, 3, height_ratios=[1.95, 1.05], width_ratios=[1.6, 1.0, 1.73],
                        hspace=0.04, wspace=0.06)

photo_axes = []
for col, (letter, name, box) in enumerate(PANELS):
    ax = fig.add_subplot(grid[0, col])
    photo_axes.append(ax)
    ax.imshow(crop_fraction(ImageOps.exif_transpose(Image.open(PHOTO_DIR / name)), box))
    ax.set_axis_off()
    label(ax, letter)

ax = fig.add_subplot(grid[1, :])
for i, (dry, fraction) in enumerate(COVER_FRACTION.items()):
    x = i * SPACING
    ax.add_patch(Circle((x, 0), DISH_RADIUS, facecolor="#e8f1f8", edgecolor="0.3", lw=1.2))
    if fraction > 0:
        ax.add_patch(Wedge((x, 0), PAPER_RADIUS, 90, 90 + 360 * fraction,
                           facecolor="#d9c7a3", edgecolor="0.3", lw=1.0, alpha=0.9))
    ax.text(x, -1.45, DRY_LABELS[dry], ha="center", va="top", fontsize=9)
ax.set_xlim(-SPACING / 2, 2 * SPACING + SPACING / 2)
ax.set_ylim(-1.95, 1.2)
ax.set_aspect("equal")
ax.set_axis_off()
ax.apply_aspect()
fig.text(photo_axes[0].get_position().x0, ax.get_position().y1, "D", fontweight="bold",
         fontsize=12, va="top", ha="left")

fig.savefig("Figure1.png", dpi=300, bbox_inches="tight", pad_inches=0.03)
print("Saved Figure1.png")

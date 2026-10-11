from pathlib import Path

import matplotlib
import numpy as np

DATA_DIR = Path("spectra")

SAMPLE_MAP = {
    2.5: {0: [None, 7304, 7316], 1: [7292, 7303, 7315], 2: [7291, 7302, 7314]},
    4.5: {0: [7290, 7301, 7313], 1: [7289, 7300, 7312], 2: [7288, 7299, 7311]},
    6.5: {0: [7287, 7298, 7310], 1: [7286, 7297, 7309], 2: [7285, 7296, 7308]},
    8.5: {0: [7284, 7295, 7307], 1: [7283, 7294, 7306], 2: [7282, 7293, 7305]},
}

EXCLUDED = {7292}

PH_LABELS = {2.5: "2.64", 4.5: "4.42", 6.5: "6.48", 8.5: "8.46"}

DRY_LABELS = {0: "Uncovered", 1: "1/3 covered", 2: "2/3 covered"}
DRY_MARKERS = {0: "o", 1: "s", 2: "^"}
DRY_COLORS = {0: "#0072B2", 1: "#E69F00", 2: "#CC79A7"}

ARTIFACT_WINDOW = (850, 872)


def set_figure_style():
    matplotlib.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 10,
    })


def load_asc(path):
    lines = Path(path).read_text(encoding="latin-1").splitlines()
    start = next(i for i, s in enumerate(lines) if s.strip() == "#DATA") + 1
    data = np.array([[float(v) for v in s.split("\t")] for s in lines[start:] if s.strip()])
    order = np.argsort(data[:, 0])
    return data[order, 0], data[order, 1]


def load_sample(number):
    return load_asc(DATA_DIR / f"Sample{number}.Sample.asc")


def features(w, t):
    return t[w == 600][0], t[w == 300][0]


def iter_samples():
    for ph, by_dry in SAMPLE_MAP.items():
        for dry, reps in by_dry.items():
            for rep, num in enumerate(reps, start=1):
                if num is not None and num not in EXCLUDED:
                    yield ph, dry, rep, num

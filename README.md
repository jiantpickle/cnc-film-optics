# CNC film optics: analysis code and data

This repository contains the data and Python code used for the figures and statistics in our
manuscript on how suspension pH and drying condition affect the optical properties of
evaporation-cast cellulose nanocrystal (CNC) films.

The input data are transmission spectra of 34 films, recorded from 200 to 1500 nm in 2 nm steps
with a PerkinElmer Lambda 750 UV-Vis-NIR spectrophotometer.

## Contents

```
cnc-film-optics/
├── README.md
├── requirements.txt
├── cnc_common.py            shared settings and functions used by every script
├── fig1_photos.py           Figure 1
├── fig2_spectra.py          Figure 2
├── fig3_transmittance.py    Figure 3
├── stats_anova.py           two-way ANOVA, Levene's test, Tukey's HSD test
├── fringe_thickness.py      film thickness from interference fringes
├── minima_search.py         search for transmission minima (reflection bands)
├── artifact_step.py         size of the step at the detector changeover (860.8 nm)
├── blank_no_sample.asc      blank scan with no sample in the beam
├── spectra/                 transmission spectra of the films
└── photos/                  photographs used in Figure 1
```

## Requirements

The code runs on macOS, Windows, and Linux. It was run with Python 3.10.5. The package versions
used are listed in `requirements.txt`.

## Installation

Download this repository (green **Code** button, then **Download ZIP**) and unzip it. Open a
terminal in the unzipped folder and run the following.

macOS or Linux:

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows:

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Usage

Run each script from the repository folder, with the environment activated:

```
python fig1_photos.py
python fig2_spectra.py
python fig3_transmittance.py
python stats_anova.py
python fringe_thickness.py
python minima_search.py
python artifact_step.py
```

The scripts are independent, and can be run in any order. 

| Script | Output |
|---|---|
| `fig1_photos.py` | Saves `Figure1.png`: three cropped photographs (A to C) and a schematic of the three drying conditions (D). |
| `fig2_spectra.py` | Saves `Figure2.png`: transmission spectra of all films from 250 to 1500 nm, one panel per pH. |
| `fig3_transmittance.py` | Saves `Figure3.png`: transmittance of each film at 600 nm and 300 nm, grouped by pH and drying condition, with mean and SD. |
| `stats_anova.py` | Prints group means and SDs, the two-way ANOVA table (Type III), Levene's test, and Tukey's HSD comparisons for transmittance at 600 nm and 300 nm. Films at pH 2.64 are excluded from the tests. |
| `fringe_thickness.py` | Prints, for the pH 2.64 and pH 4.42 films, whether interference fringes were detected and the film thickness calculated for refractive indices of 1.50, 1.55, and 1.60. The manuscript uses 1.55. |
| `minima_search.py` | Prints the wavelengths at which transmission minima were found and how many films at each pH showed them, for smoothing widths of 82, 122, and 202 nm. Only positions found in at least five films are listed. |
| `artifact_step.py` | Prints the size of the transmittance step at 860.8 nm for the blank scan and for each film, and the number of films in which the step exceeds three times the noise. |

## Data

### Spectra

Each file in `spectra/` is named `Sample<number>.Sample.asc` and is a PerkinElmer
ASCII export. The lines after `#DATA` contain two tab-separated columns: wavelength (nm) and
transmittance (%T).

The sample numbers correspond to the experimental conditions as follows.

| pH (target / measured) | Drying condition | Replicate 1 | Replicate 2 | Replicate 3 |
|---|---|---|---|---|
| 2.5 / 2.64 | Uncovered | none (broke during casting) | 7304 | 7316 |
| 2.5 / 2.64 | 1/3 covered | 7292 (excluded) | 7303 | 7315 |
| 2.5 / 2.64 | 2/3 covered | 7291 | 7302 | 7314 |
| 4.5 / 4.42 | Uncovered | 7290 | 7301 | 7313 |
| 4.5 / 4.42 | 1/3 covered | 7289 | 7300 | 7312 |
| 4.5 / 4.42 | 2/3 covered | 7288 | 7299 | 7311 |
| 6.5 / 6.48 | Uncovered | 7287 | 7298 | 7310 |
| 6.5 / 6.48 | 1/3 covered | 7286 | 7297 | 7309 |
| 6.5 / 6.48 | 2/3 covered | 7285 | 7296 | 7308 |
| 8.5 / 8.46 | Uncovered | 7284 | 7295 | 7307 |
| 8.5 / 8.46 | 1/3 covered | 7283 | 7294 | 7306 |
| 8.5 / 8.46 | 2/3 covered | 7282 | 7293 | 7305 |

Sample 7292 is excluded from all analyses because the mounted piece of film was too small to cover the measurement beam reliably. This leaves 34 films.

In the code, pH conditions are identified by their target values (2.5, 4.5, 6.5, 8.5), so the
printed output uses these values. The measured values (2.64, 4.42, 6.48, 8.46) are the ones
reported in the manuscript and shown in the figures.

### Blank scan

`blank_no_sample.asc` is a scan recorded with no sample in the beam. It is used only by
`artifact_step.py`, to check whether the step at 860.8 nm comes from the instrument.

### Photographs

`photos/` contains `fig1A_all_films.jpeg` (Figure 1A), `fig1B_pH2.64_film.jpeg` (Figure 1B),
and `fig1C_pH4.42_film_dark_background.jpeg` (Figure 1C). They are used only by `fig1_photos.py`.

## Notes

Figures use Arial when it is installed. On systems without Arial, other fonts are
used instead, so the figures may look slightly different from those in the manuscript.

# Updating the website CV

`assets/Kshitij_Mishra_CV.pdf` is compiled from `cv/cv-public.tex`; see `cv/README.md`.

1. Edit `data/publications.json` for publications, or the section files in `cv/` for
   everything else.
2. Run `python3 scripts/build_cv.py`, or push and let the GitHub Action build it.
3. To make browsers fetch the new PDF immediately, update the CV link version in
   `index.html` and rerun `python3 scripts/build_publications.py`.

The full CV, with pending manuscripts and referee contacts, stays in the private CV
project. Only the public source and its PDF belong in this repository.

Current PDF revision: September 24, 2026, built from `cv/` with PROBE (NeurIPS 2026).

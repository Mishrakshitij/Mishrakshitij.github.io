# Public CV source

LaTeX source of `assets/Kshitij_Mishra_CV.pdf`: the public edition of the CurVe CV
(theme by LianTze Lim), compiled with XeLaTeX.

## Build

From the repository root:

```sh
python3 scripts/build_cv.py
```

The script regenerates the publication lists and counts from `data/publications.json`,
compiles `cv-public.tex` with Tectonic (or latexmk and XeLaTeX), and writes
`assets/Kshitij_Mishra_CV.pdf`. The **Rebuild publication pages** GitHub Action runs it
on every push that changes the CV source or the publication data.

## Edit

- **Publications:** add or correct records in `data/publications.json`, the same file the
  website uses. The `publications-*.tex` files are regenerated on every build, so do not
  edit them. The optional `cvLabel` field sets a record's left-column label, e.g. `Neurocomp.`.
- **Page break:** `CONFERENCE_FIRST_PAGE` in `scripts/build_cv.py` sets how many conference
  papers appear on page 2 before "Conference Publications (continued)".
- **Everything else:** edit the section files directly: `header.tex`, `profile.tex`,
  `employment.tex`, `education.tex`, `patent.tex`, `systems.tex`, `teaching.tex`,
  `service.tex`, `misc.tex` (honors), `skills.tex`, and `training.tex`. Layout, colors,
  and the author markers are in `settings.sty`.

The full CV (`cv-llt.tex`) also loads `manuscripts.tex` and `referee-full.tex`, which hold
unpublished work and referee contacts. They are intentionally not in this public
repository; keep them in the private CV project. `cv-public.tex` never loads them.

Fonts: Crimson Text and Cabin, both under the SIL Open Font License; see `fonts/`.

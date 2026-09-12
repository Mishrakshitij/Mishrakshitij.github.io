# Updating the website CV

The website CV is compiled from Kshitij Mishra's CurVe LaTeX project.
The source project's public entry point is `cv-public.tex`, compiled with XeLaTeX.

To update the website:

1. Compile `cv-public.tex` in the maintained LaTeX project.
2. Replace `assets/Kshitij_Mishra_CV.pdf` with that compiled PDF.
3. Update the CV link version in `index.html`.
4. Run `python3 scripts/build_publications.py` to carry the menu into the publications page.
5. Check the Pages deployment and the resulting PDF.

The full project and full CV are maintained separately. Only the public PDF
belongs in this repository.

Current PDF revision: September 12, 2026 — LaTeX source edit; no photograph.

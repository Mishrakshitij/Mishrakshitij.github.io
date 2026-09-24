# Kshitij Mishra

Personal academic website for Kshitij Mishra, Postdoctoral Associate at MBZUAI.

The site presents my research on adaptive and trustworthy foundation-model agents, publications, patents, public research software, experience, and contact information. CAST—Consistent, Adaptive, Strategic, and Trustworthy—is the organizing research agenda.

## Website

Live address: **https://mishrakshitij.github.io/**

The repository is named `Mishrakshitij.github.io` to serve the account root. GitHub Pages publishes the static files from `main` at `/(root)`. Relative asset paths also support a future custom domain.

## Edit the site

| File | Purpose |
| --- | --- |
| `index.html` | Compact biography, Latest, research interests, CAST, patents, experience, and contact |
| `publications.html` | Complete static publication archive, grouped by year (generated; do not edit by hand) |
| `data/publications.json` | Public bibliography and author contribution metadata |
| `scripts/build_publications.py` | Regenerates the publication archive, totals, and venue tags |
| `.github/workflows/rebuild-pages.yml` | Rebuilds the archive pages and the CV on GitHub after the data, CV source, or shared header changes |
| `cv/` | LaTeX source of the public CV; see `cv/README.md` |
| `scripts/build_cv.py` | Regenerates the CV's publication lists from `data/publications.json` and compiles the CV |
| `publications.js` | Year ordering, venue filters, and publication search |
| `styles.css` | Layout, colors, typography, responsive behavior, and motion preferences |
| `script.js` | CAST research map, curiosity cycle, and mobile navigation |
| `assets/kshitij-mishra.png` | Profile portrait |
| `assets/Kshitij_Mishra_CV.pdf` | Public CV, compiled from `cv/` |
| `favicon.svg` | Browser icon |
| `sitemap.xml` | Canonical page URL for search engines |

All essential information is available in HTML. JavaScript enhances the research map and navigation. The page respects reduced-motion preferences and includes keyboard-accessible controls.

## Add a publication

Add one record at the top of `data/publications.json` (newest first) and push to `main`:

```json
{
  "id": "short-name",
  "title": "SHORT-NAME: Full Paper Title",
  "year": 2027,
  "venue": "ICLR 2027",
  "kind": "conference",
  "status": "accepted",
  "authors": [{"name": "Kshitij Mishra", "first": true}, {"name": "Co-author Name"}],
  "url": null,
  "code": null
}
```

The **Rebuild publication pages** GitHub Action then regenerates `publications.html` and the CV from that record and commits them; GitHub Pages publishes the result about a minute later. Pull before your next local edit, since the Action adds that commit. To preview first, run `python3 scripts/build_publications.py` and `python3 scripts/build_cv.py` locally; the Action then finds nothing to change.

Everything on the publications page is computed from the records: the total, the conference/journal/workshop split, per-year counts, and one venue tag per venue with its paper count. A venue that appears for the first time gets its own tag automatically. The Action log and the local run print the resulting tags. A malformed record stops the build with a list of problems instead of publishing a broken page.

- `id`: lowercase letters, digits, and hyphens; it becomes the paper's anchor, e.g. `publications.html#probe`.
- `venue`: the exact venue as cited, e.g. `NeurIPS 2026`, `Findings of EMNLP 2026`, or a journal name. The tag is the venue without its year (`NeurIPS`); set `venueGroup` to choose a different tag, e.g. a journal abbreviation such as `IEEE TCSS`.
- `kind`: `conference`, `journal`, or `workshop`. `status`: `published` or `accepted`; accepted papers carry an Accepted label, and work under review stays off the site.
- `first` marks the first listed author; `coFirst` marks explicitly documented equal contributions. Both default to false.
- Optional: `metadata` (journal volume and pages), `url` (paper link), `code` (repository link), `cvLabel` (the CV's left-column label when it differs from the tag, e.g. `Neurocomp.`).

Tags combine main-conference and Findings papers under the conference name and group IEEE Transactions journals under IEEE Txns.; IEEE SMC remains a separate conference. `VENUE_ORDER` at the top of `scripts/build_publications.py` sets the tag order; unlisted venues follow automatically. The website bolds Kshitij Mishra and adds dotted blue underlining to first and joint-first authors. The CV uses the same records for its publication lists and counts. The **Latest** bullets are updated separately.

## Other edits

Edit the bullet updates under **Latest**, the **Patents** entry, and **Open research** links directly in `index.html`. Patent metadata links to its public record; publication code links are maintained in `data/publications.json`. The CAST introduction states the focus on building trustworthy AI systems, with further safety and security details in the interactive T node. The **CV** navigation link opens `assets/Kshitij_Mishra_CV.pdf` in a new tab. The Sanskrit quote and its translation sit directly below Research interests. The portrait sidebar contains affiliation, both email addresses, LinkedIn, and the interactive curiosity cycle. The publications and patents pages copy the shared header from `index.html`; the Action regenerates both whenever it changes. Both animations have pause controls and respect reduced-motion preferences.

## Preview locally

From this directory:

```sh
python3 -m http.server 8000
```

Open http://localhost:8000 in a browser. Check a narrow mobile viewport before publishing edits.

## Public content

The downloadable CV contains the public professional record. Work under review and unpublished technical details are excluded. Research interests describe an evolving agenda; the site does not imply an established CAST laboratory or faculty appointment.

The website has no analytics, advertising, contact-form backend, or embedded tracking widgets. Contact links open the visitor's email application or the linked professional profile.

## Moving to a new address

Keep relative asset paths. Update the canonical URL, Open Graph URL/image in `index.html`, and `sitemap.xml`. Configure a custom domain in GitHub Pages settings before adding a `CNAME` file. Update links from the GitHub profile after the new address is live.

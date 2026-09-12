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
| `publications.html` | Complete static publication archive, grouped by year |
| `data/publications.json` | Public bibliography and author contribution metadata |
| `scripts/build_publications.py` | Regenerates the publication archive |
| `publications.js` | Year ordering, venue filters, and publication search |
| `styles.css` | Layout, colors, typography, responsive behavior, and motion preferences |
| `script.js` | CAST research map, curiosity cycle, and mobile navigation |
| `assets/kshitij-mishra.png` | Profile portrait |
| `assets/Kshitij_Mishra_CV.pdf` | Public CV |
| `favicon.svg` | Browser icon |
| `sitemap.xml` | Canonical page URL for search engines |

All essential information is available in HTML. JavaScript enhances the research map and navigation. The page respects reduced-motion preferences and includes keyboard-accessible controls.

To add or correct a publication, edit `data/publications.json`, then run:

```sh
python3 scripts/build_publications.py
```

The generator includes only published or accepted work and computes venue/year counts from the same records it renders. Keep each paper’s exact venue in its metadata. Summary counts and filters combine main-conference and Findings papers under the conference name, and group IEEE Transactions journals under IEEE Txns.; IEEE SMC remains a separate conference. The `first` flag marks the first listed author; `coFirst` marks explicitly documented equal contributions. The website bolds Kshitij Mishra and adds dotted blue underlining to first and joint-first authors. Update the public CV separately when the record changes.

Edit the bullet updates under **Latest**, the **Patents** entry, and **Open research** links directly in `index.html`. Patent metadata links to its public record; publication code links are maintained in `data/publications.json`. The CAST introduction states the focus on building trustworthy AI systems, with further safety and security details in the interactive T node. The **CV** navigation link opens `assets/Kshitij_Mishra_CV.pdf` in a new tab. The Sanskrit quote and its translation sit directly below Research interests. The portrait sidebar contains affiliation, both email addresses, LinkedIn, and the interactive curiosity cycle. After changing the shared header in `index.html`, rerun the publication generator to keep both pages consistent. Both animations have pause controls and respect reduced-motion preferences.

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

# Kshitij Mishra

Personal academic website for Kshitij Mishra, Postdoctoral Associate at MBZUAI.

The site presents my research on adaptive and trustworthy foundation-model agents, selected publications, public research software, experience, and contact information. CAST—Consistent, Adaptive, Strategic, and Trustworthy—is the organizing research agenda.

## Website

GitHub Pages address after activation:

**https://mishrakshitij.github.io/**

The repository must be named **Mishrakshitij.github.io** to serve this root address. If it is still named `KshitijMishra.github.io`, rename it under Settings → General → Repository name. The GitHub username does not need to change. Relative asset paths also support a future custom domain.

## Publish on GitHub Pages

1. Open **Settings → Pages** in this repository.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select **main** and **/(root)**, then **Save**.

GitHub publishes the static files after the Pages deployment finishes. Subsequent changes to `main` redeploy automatically. No build service, API key, paid hosting plan, or package installation is needed.

## Edit the site

| File | Purpose |
| --- | --- |
| `index.html` | Biography, research, publications, experience, and contact links |
| `styles.css` | Layout, colors, typography, responsive behavior, and motion preferences |
| `script.js` | Research-map interaction, publication filters, and mobile navigation |
| `assets/kshitij-mishra.png` | Profile portrait |
| `assets/Kshitij_Mishra_CV.pdf` | Public CV |
| `favicon.svg` | Browser icon |
| `sitemap.xml` | Canonical page URL for search engines |

All essential information is available in HTML. JavaScript enhances the research map and navigation. The page respects reduced-motion preferences and includes keyboard-accessible controls.

To add a publication, copy an existing publication entry in `index.html`, update its year/category and links, and keep its publication status accurate. Update the public CV separately when the record changes. Future affiliation, teaching, or group sections can be added without adopting a new site framework.

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

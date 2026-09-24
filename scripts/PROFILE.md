# Editing the academic profile

- Edit the biography in the `profile-content` block of `index.html`.
- Edit the Postdoc, Ph.D., and M.Tech. timeline in its `profile-bio` section, beneath
  the curiosity–learning–experience–innovation loop.
- Edit the CAST summary, Current questions, and Looking ahead in the
  `cast-overview` block of `index.html`, below Latest in the main column.
- Edit the short figure captions in `research-themes.js`; keep the initial
  Consistent caption in `index.html` in sync.
- Preserve the script order: `research-themes.js` before `script.js`.
- After changing the shared menu or stylesheet/script versions, run
  `python3 scripts/build_publications.py` and `python3 scripts/build_patents.py`
  to update both archive pages. The Rebuild publication pages GitHub Action
  also runs both after every push that touches `index.html`.
- Edit the patent citation in `scripts/build_patents.py` and regenerate its page.

The full career history remains in the CV; the homepage shows a compact
Bio timeline, with Honors and Fellowships below it. CAST is the homepage's Research Interests section.

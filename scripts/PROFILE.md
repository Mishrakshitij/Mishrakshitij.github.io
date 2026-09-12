# Editing the academic profile

- Edit the biography in the `profile-content` block of `index.html`.
- Edit roles, institutions, and dates in its `profile-experience` list, beneath
  the curiosity–learning–experience–innovation loop.
- Edit the four CAST panel descriptions and topics in `research-themes.js`.
  Keep the initial C panel and the no-JavaScript summaries in `index.html` in sync.
- Preserve the script order: `research-themes.js` before `script.js`.
- After changing the shared menu or stylesheet/script versions, run
  `python3 scripts/build_publications.py` to update the publication archive header.

The full career history remains in the CV; the homepage shows a compact
experience list. CAST is the homepage's Research Interests section.

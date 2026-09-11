"""Regenerate the static publication archive from its public metadata.

Run: python3 scripts/build_publications.py
The complete bibliography is HTML, so it remains readable without JavaScript.
"""
from collections import Counter
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT / 'data/publications.json').read_text())
assert len({p['id'] for p in records}) == len(records), 'Duplicate publication ID'
assert all(p['status'] in {'published', 'accepted'} for p in records)
assert all(any(a['name'] == 'Kshitij Mishra' for a in p['authors']) for p in records)
counts = Counter(p['venueGroup'] for p in records)
years = sorted({p['year'] for p in records}, reverse=True)
conference_count = sum(p['kind'] == 'conference' for p in records)
journal_count = sum(p['kind'] == 'journal' for p in records)
home = (ROOT / 'index.html').read_text()
header = home.split('  <main id="main">')[0]
header = header.replace('<title>Kshitij Mishra · Adaptive &amp; Trustworthy AI Agents</title>', '<title>Publications · Kshitij Mishra</title>')
header = re.sub(r'<title>.*?</title>', '<title>Publications · Kshitij Mishra</title>', header)
header = re.sub(r'<meta name="description"[^>]+>', '<meta name="description" content="Published and accepted research by Kshitij Mishra, grouped by year, with venue counts and first-author contribution markers.">', header)
header = header.replace('rel="canonical" href="https://mishrakshitij.github.io/"', 'rel="canonical" href="https://mishrakshitij.github.io/publications.html"')
header = header.replace('property="og:url" content="https://mishrakshitij.github.io/"', 'property="og:url" content="https://mishrakshitij.github.io/publications.html"')
header = re.sub(r'<meta property="og:title"[^>]+>', '<meta property="og:title" content="Publications · Kshitij Mishra">', header)
for anchor in ('about', 'research', 'experience', 'contact'):
    header = header.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
header = header.replace('href="publications.html">Publications', 'href="publications.html" aria-current="page">Publications')
header = header.replace('</head>', '  <script src="publications.js" defer></script>\n</head>')
footer = home[home.index('  <footer '):].replace('href="#about"', 'href="#main"')

def author_html(author):
    name = escape(author['name'])
    lead = author.get('first') or author.get('coFirst')
    classes = ('self-author ' if author['name'] == 'Kshitij Mishra' else '') + ('first-author' if lead else '')
    tag = 'strong' if author['name'] == 'Kshitij Mishra' else 'span'
    mark = '<sup>*</sup>' if author.get('coFirst') else ''
    return f'<{tag} class="{classes.strip()}">{name}</{tag}>{mark}'

def publication_html(pub):
    title = escape(pub['title'])
    if pub.get('url'):
        title = f'<a href="{escape(pub["url"], quote=True)}">{title} <span aria-hidden="true">↗</span></a>'
    authors = ', '.join(author_html(a) for a in pub['authors'])
    venue = escape(pub['venue'])
    metadata = escape(pub.get('metadata', ''))
    if metadata:
        venue += f' · {metadata}'
    if pub['kind'] == 'journal':
        venue += f' · {pub["year"]}'
    if pub['status'] == 'accepted':
        venue += '<span class="accepted-label">Accepted</span>'
    links = []
    if pub.get('url'):
        links.append(f'<a href="{escape(pub["url"], quote=True)}">Paper ↗</a>')
    if pub.get('code'):
        links.append(f'<a href="{escape(pub["code"], quote=True)}">Code ↗</a>')
    resources = '<div class="archive-links">' + ''.join(links) + '</div>' if links else ''
    return f'''<article class="archive-publication" id="{escape(pub['id'])}" data-venue="{escape(pub['venueGroup'], quote=True)}" data-year="{pub['year']}">
      <h3>{title}</h3><p class="archive-authors">{authors}</p><p class="archive-venue">{venue}</p>{resources}
    </article>'''

venue_order = ['ICML', 'ACL', 'EMNLP', 'Findings of EMNLP', 'EACL', 'Findings of EACL', 'Findings of NAACL', 'COLING', 'AAAI', 'IJCAI', 'IEEE SMC']
venue_order += sorted(v for v in counts if v not in venue_order)
chips = [f'<button class="venue-count" type="button" data-venue-filter="all" aria-pressed="true">All <strong>×{len(records)}</strong></button>']
for venue in venue_order:
    chips.append(f'<button class="venue-count" type="button" data-venue-filter="{escape(venue, quote=True)}" aria-pressed="false">{escape(venue)} <strong>×{counts[venue]}</strong></button>')
year_links = ''.join(f'<a href="#year-{y}">{y}</a>' for y in years)
groups = []
for year in years:
    papers = [p for p in records if p['year'] == year]
    items = '\n'.join(publication_html(p) for p in papers)
    groups.append(f'<section class="year-group" id="year-{year}" data-year="{year}" aria-labelledby="heading-{year}"><h2 id="heading-{year}">{year}<span>{len(papers)} publication{"s" if len(papers) != 1 else ""}</span></h2>{items}</section>')

page = header + f'''  <main id="main" class="publications-page container">
    <h1>Publications</h1>
    <p class="archive-intro">Published and accepted work, organized by year. <a class="text-link" href="https://scholar.google.com/citations?user=jfTVBUQAAAAJ">Google Scholar ↗</a></p>
    <p class="archive-totals"><strong>{len(records)} publications</strong> · {conference_count} conference papers · {journal_count} journal articles</p>
    <div class="venue-summary" role="group" aria-label="Publication counts and venue filters">{''.join(chips)}</div>
    <p class="publication-note">Counts include accepted papers. Main-conference and Findings publications are counted separately.</p>
    <div class="archive-controls"><label class="archive-search" for="publication-search">Search <input id="publication-search" type="search" placeholder="Title, author, or venue" autocomplete="off"></label><label class="archive-sort" for="publication-sort">Year order <select id="publication-sort"><option value="desc">Newest first</option><option value="asc">Oldest first</option></select></label></div>
    <p class="archive-legend"><strong>Kshitij Mishra</strong> is shown in bold. <span class="first-author">Dotted blue underline</span> marks first and joint-first authors; <sup>*</sup> denotes equal contribution.</p>
    <p id="publication-status" class="sr-only" aria-live="polite">Showing {len(records)} publications.</p>
    <div class="archive-layout"><nav class="year-nav" aria-label="Publication years"><span class="eyebrow">By year</span>{year_links}</nav><div id="publication-years">{''.join(groups)}<p class="archive-empty" id="publication-empty" hidden>No publications match this search. Try another term or select All.</p></div></div>
  </main>
''' + footer
(ROOT / 'publications.html').write_text(page)
print(f'Built publications.html: {len(records)} publications across {len(years)} years; {sum(counts.values())} venue-count entries.')

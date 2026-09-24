"""Regenerate the static publication archive from its public metadata.

Run: python3 scripts/build_publications.py
The complete bibliography is HTML, so it remains readable without JavaScript.
Totals, venue tags, and year groups are computed from data/publications.json,
so adding a record there is the only edit a new paper needs. GitHub Actions
reruns this script whenever that file changes on main.
"""
from collections import Counter
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
KINDS = {'conference': 'conference paper', 'journal': 'journal article', 'workshop': 'workshop paper'}
# Venue tag order on the publications page. A venue missing from this list still
# gets its own tag and count automatically, placed after the listed venues
# (conferences, then journals, then workshops; more papers first).
VENUE_ORDER = [
    'NeurIPS', 'ICML', 'ICLR', 'COLM', 'TMLR',
    'USENIX Security', 'IEEE S&P', 'ACM CCS', 'NDSS',
    'ACL', 'EMNLP', 'EACL', 'NAACL', 'COLING', 'TACL',
    'AAAI', 'IJCAI', 'IEEE Txns.', 'IEEE SMC',
]

def validate(records):
    """Stop with a readable list of problems instead of publishing a broken page."""
    problems, seen = [], set()
    for number, pub in enumerate(records, 1):
        where = f"record {number} ({pub.get('id') or 'no id'})"
        missing = [key for key in ('id', 'title', 'year', 'venue', 'kind', 'status', 'authors') if not pub.get(key)]
        if missing:
            problems.append(f'{where}: missing {", ".join(missing)}')
        if pub.get('id'):
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', pub['id']):
                problems.append(f'{where}: id must use lowercase letters, digits, and hyphens')
            if pub['id'] in seen:
                problems.append(f'{where}: duplicate id')
            seen.add(pub['id'])
        if pub.get('year') and not (isinstance(pub['year'], int) and 1900 < pub['year'] < 2100):
            problems.append(f'{where}: year must be a number such as 2026, without quotes')
        if pub.get('kind') and pub['kind'] not in KINDS:
            problems.append(f'{where}: kind must be one of: {", ".join(KINDS)}')
        if pub.get('status') and pub['status'] not in {'published', 'accepted'}:
            problems.append(f'{where}: status must be "published" or "accepted"; work under review stays off the site')
        if pub.get('authors'):
            if not all(isinstance(a, dict) and a.get('name') for a in pub['authors']):
                problems.append(f'{where}: write each author as {{"name": "..."}}')
            elif not any(a['name'] == 'Kshitij Mishra' for a in pub['authors']):
                problems.append(f'{where}: authors must include "Kshitij Mishra"')
        for key in ('url', 'code'):
            if pub.get(key) and not str(pub[key]).startswith(('https://', 'http://')):
                problems.append(f'{where}: {key} must be a full http(s) link or null')
    if problems:
        raise SystemExit('Cannot build publications.html:\n  - ' + '\n  - '.join(problems))

def venue_group(pub):
    """Venue without year or presentation note ("NeurIPS 2026" -> "NeurIPS"); venueGroup overrides."""
    group = re.sub(r'\s*\([^)]*\)$', '', pub['venue'].strip())
    return pub.get('venueGroup') or re.sub(r'\s*\b(?:19|20)\d{2}\b', '', group).strip()

def venue_family(pub):
    """Compact filter labels; each citation keeps its exact publication venue."""
    group = venue_group(pub)
    if group.startswith('Findings of '):
        return group.removeprefix('Findings of ')
    if pub['kind'] == 'journal' and (re.fullmatch(r'IEEE(?:/ACM)? T[A-Z]{2,}', group) or re.match(r'IEEE(?:/ACM)? Transactions\b', pub['venue'])):
        return 'IEEE Txns.'
    return group

def plural(count, noun):
    return f'{count} {noun}{"" if count == 1 else "s"}'

try:
    records = json.loads((ROOT / 'data/publications.json').read_text(encoding='utf-8'))
except json.JSONDecodeError as error:
    raise SystemExit(f'data/publications.json is not valid JSON: {error}')
validate(records)
counts = Counter(venue_family(p) for p in records)
years = sorted({p['year'] for p in records}, reverse=True)
kind_counts = Counter(p['kind'] for p in records)
totals = [f'<strong>{plural(len(records), "publication")}</strong>']
totals += [plural(kind_counts[kind], label) for kind, label in KINDS.items() if kind_counts[kind]]
home = (ROOT / 'index.html').read_text(encoding='utf-8')
header = home.split('  <main id="main">')[0]
header = header.replace('<title>Kshitij Mishra · Adaptive &amp; Trustworthy AI Agents</title>', '<title>Publications · Kshitij Mishra</title>')
header = re.sub(r'<title>.*?</title>', '<title>Publications · Kshitij Mishra</title>', header)
header = re.sub(r'<meta name="description"[^>]+>', '<meta name="description" content="Published and accepted research by Kshitij Mishra, grouped by year, with venue counts and first-author contribution markers.">', header)
header = header.replace('rel="canonical" href="https://mishrakshitij.github.io/"', 'rel="canonical" href="https://mishrakshitij.github.io/publications.html"')
header = header.replace('property="og:url" content="https://mishrakshitij.github.io/"', 'property="og:url" content="https://mishrakshitij.github.io/publications.html"')
header = re.sub(r'<meta property="og:title"[^>]+>', '<meta property="og:title" content="Publications · Kshitij Mishra">', header)
for anchor in ('about', 'research', 'patents', 'experience', 'contact'):
    header = header.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
header = re.sub(r'(href="publications\.html(?:\?[^" ]*)?")>Publications', r'\1 aria-current="page">Publications', header)
header = header.replace('</head>', '  <script src="publications.js" defer></script>\n</head>')
footer = home[home.index('  <footer '):].replace('href="#about"', 'href="#main"')

def author_html(author):
    name = escape(author['name'])
    lead = author.get('first') or author.get('coFirst')
    classes = ('self-author ' if author['name'] == 'Kshitij Mishra' else '') + ('first-author' if lead else '')
    tag = 'strong' if author['name'] == 'Kshitij Mishra' else 'span'
    return f'<{tag} class="{classes.strip()}">{name}</{tag}>'

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
    return f'''<article class="archive-publication" id="{escape(pub['id'])}" data-venue="{escape(venue_family(pub), quote=True)}" data-year="{pub['year']}">
      <h3>{title}</h3><p class="archive-authors">{authors}</p><p class="archive-venue">{venue}</p>{resources}
    </article>'''

family_kinds = {venue_family(p): p['kind'] for p in records}
def tag_position(venue):
    if venue in VENUE_ORDER:
        return (0, VENUE_ORDER.index(venue), 0, '')
    return (1, list(KINDS).index(family_kinds[venue]), -counts[venue], venue.casefold())

venue_order = sorted(counts, key=tag_position)
chips = [f'<button class="venue-count" type="button" data-venue-filter="all" aria-pressed="true">All <strong>×{len(records)}</strong></button>']
for venue in venue_order:
    chips.append(f'<button class="venue-count" type="button" data-venue-filter="{escape(venue, quote=True)}" aria-pressed="false">{escape(venue)} <strong>×{counts[venue]}</strong></button>')
year_links = ''.join(f'<a href="#year-{y}">{y}</a>' for y in years)
groups = []
for year in years:
    papers = [p for p in records if p['year'] == year]
    items = '\n'.join(publication_html(p) for p in papers)
    groups.append(f'<section class="year-group" id="year-{year}" data-year="{year}" aria-labelledby="heading-{year}"><h2 id="heading-{year}">{year}<span>{plural(len(papers), "publication")}</span></h2>{items}</section>')

page = header + f'''  <main id="main" class="publications-page container">
    <h1>Publications</h1>
    <p class="archive-intro">Published and accepted work, organized by year. <a class="text-link" href="https://scholar.google.com/citations?user=jfTVBUQAAAAJ">Google Scholar ↗</a></p>
    <p class="archive-totals">{' · '.join(totals)}</p>
    <div class="venue-summary" role="group" aria-label="Publication counts and venue filters">{''.join(chips)}</div>
    <p class="publication-note">Counts include accepted papers. Conference totals include Findings papers.</p>
    <div class="archive-controls"><label class="archive-search" for="publication-search">Search <input id="publication-search" type="search" placeholder="Title, author, or venue" autocomplete="off"></label><label class="archive-sort" for="publication-sort">Year order <select id="publication-sort"><option value="desc">Newest first</option><option value="asc">Oldest first</option></select></label></div>
    <p class="archive-legend"><strong>Kshitij Mishra</strong> is shown in bold. <span class="first-author">Dotted blue underline</span> marks first and joint-first authors.</p>
    <p id="publication-status" class="sr-only" aria-live="polite">Showing {len(records)} publications.</p>
    <div class="archive-layout"><nav class="year-nav" aria-label="Publication years"><span class="eyebrow">By year</span>{year_links}</nav><div id="publication-years">{''.join(groups)}<p class="archive-empty" id="publication-empty" hidden>No publications match this search. Try another term or select All.</p></div></div>
  </main>
''' + footer
(ROOT / 'publications.html').write_text(page, encoding='utf-8')
print(f'Built publications.html: {plural(len(records), "publication")} across {plural(len(years), "year")}.')
print('Venue tags: ' + ', '.join(f'{venue} ×{counts[venue]}' for venue in venue_order))

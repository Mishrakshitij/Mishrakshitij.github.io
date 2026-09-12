"""Regenerate the patent page while sharing the homepage header and footer.

Run: python3 scripts/build_patents.py
The patent citation remains readable without JavaScript.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
home = (ROOT / "index.html").read_text(encoding="utf-8")
header = home.split('  <main id="main">', 1)[0]
title = "Patents · Kshitij Mishra"
description = "Patents by Kshitij Mishra, with inventor credits and links to patent records."
url = "https://mishrakshitij.github.io/patents.html"

header = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", header)
header = re.sub(
    r'<meta name="description"[^>]+>',
    f'<meta name="description" content="{description}">',
    header,
)
header = re.sub(
    r'<link rel="canonical"[^>]+>',
    f'<link rel="canonical" href="{url}">',
    header,
)
for property_name, value in (
    ("og:title", title),
    ("og:description", description),
    ("og:url", url),
):
    header = re.sub(
        rf'<meta property="{property_name}"[^>]+>',
        f'<meta property="{property_name}" content="{value}">',
        header,
    )
for anchor in ("about", "research", "experience", "contact"):
    header = header.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
header = header.replace('href="#patents"', 'href="patents.html"')
header = re.sub(
    r'(href="patents\.html(?:\?[^" ]*)?")>Patents',
    r'\1 aria-current="page">Patents',
    header,
)
footer = home[home.index("  <footer "):].replace('href="#about"', 'href="#main"')

# Preserve the verified public citation formerly shown on the homepage.
page = header + '''  <main id="main" class="patents-page container">
    <h1>Patents</h1>
    <article class="patent-entry" aria-labelledby="patent-title">
      <h2 id="patent-title"><a href="https://patents.google.com/patent/US12456020B1/en">Systems and methods for updating large language models <span aria-hidden="true">↗</span></a></h2>
      <p class="patent-inventors"><strong>Kshitij Mishra</strong>, Tamer Soliman, Aram Galstyan, Anoop Kumar, and Anil K Ramakrishna</p>
      <p class="patent-meta">US Patent 12,456,020 B1 · Granted <time datetime="2025-10-28">October 28, 2025</time> · Amazon Technologies, Inc.</p>
      <a class="text-link" href="https://patents.google.com/patent/US12456020B1/en">Patent record ↗</a>
    </article>
  </main>
''' + footer
(ROOT / "patents.html").write_text(page, encoding="utf-8")
print("Generated patents.html")

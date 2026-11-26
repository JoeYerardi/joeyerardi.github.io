"""Build the portfolio with the Python standard library."""
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUTPUT = ROOT / "public"
DOMAIN = "https://joeyerardi.com"
INQUIRER = "https://www.inquirer.com/author/yerardi_joe/"
NAVIGATION = (("featured-work", "Work"), ("about", "About"), ("contact", "Contact"))


def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def publication_date(value):
    day = date.fromisoformat(value)
    return f'<time datetime="{day.isoformat()}">{day:%b} {day.day}, {day.year}</time>'


def page(title, description, route, body):
    base = "../" if route and route != "404.html" else "./"
    if route == "404.html":
        base = "/"
    links = []
    for path, label in NAVIGATION:
        current = ' aria-current="page"' if path == route else ""
        links.append(f'<a href="{base}{path}/"{current}>{label}</a>')
    canonical = (f'<link rel="canonical" href="{DOMAIN}/{route + "/" if route else ""}">'
                 if route != "404.html" else "")
    javascript = f'<script src="{base}assets/search.js" defer></script>' if route == "featured-work" else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  {canonical}
  <link rel="stylesheet" href="{base}assets/site.css">
  {javascript}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap masthead">
      <a class="wordmark" href="{base}">Joe Yerardi<span>.</span></a>
      <nav aria-label="Main navigation">{''.join(links)}</nav>
    </div>
  </header>
  <main id="main" class="wrap">{body}</main>
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <a class="wordmark" href="{base}">Joe Yerardi<span>.</span></a>
      <div><a href="mailto:joe.yerardi@gmail.com">Email</a><a href="https://github.com/JoeYerardi">GitHub</a><a href="https://www.linkedin.com/in/joeyerardi">LinkedIn</a></div>
    </div>
  </footer>
</body>
</html>
"""


def recent_card(story):
    return f"""
    <article class="recent-card">
      <p class="eyebrow">{escape(story['topic'])}</p>
      <h3><a href="{escape(story['url'])}">{escape(story['title'])}</a></h3>
      <p>{escape(story['summary'])}</p>
      <p class="meta">{publication_date(story['date'])}</p>
    </article>"""


def home(recent):
    return f"""
  <section class="intro">
    <h1>Joe Yerardi<span>.</span></h1>
    <p class="role">Data Journalist</p>
    <p class="dek">Over 15 years in journalism, I've used data, code, and traditional reporting techniques to tell stories about people and the institutions that shape their lives.</p>
    <div class="intro-links">
      <a href="./featured-work/" class="button">Explore my work</a>
      <a href="./about/">More about me</a>
    </div>
  </section>

  <section class="recent" aria-labelledby="recent-title">
    <div class="section-heading">
      <h2 id="recent-title">The Philadelphia Inquirer</h2>
      <a href="{INQUIRER}">All Inquirer bylines</a>
    </div>
    <div class="recent-grid">{''.join(map(recent_card, recent))}
    </div>
  </section>"""


def archive_card(story):
    paragraphs = "".join(f"<p>{paragraph}</p>" for paragraph in story["paragraphs"])
    tools = f"<p><strong>Tools</strong> {escape(story['tools'])}</p>" if story["tools"] else ""
    return f"""
    <article class="archive-card" data-clip>
      <p class="meta">{escape(story['publisher'])} <span aria-hidden="true">·</span> {publication_date(story['date'])}</p>
      <h3><a href="{escape(story['url'])}">{escape(story['title'])}</a></h3>
      <details><summary>Reporting notes</summary>{paragraphs}{tools}</details>
    </article>"""


def archive(recent, stories):
    return f"""
  <section class="page-intro">
    <h1>Featured work<span>.</span></h1>
    <p class="dek">Selected investigations, data stories and news apps.</p>
  </section>
  <section aria-labelledby="new-work" class="recent">
    <div class="section-heading">
      <h2 id="new-work">The Philadelphia Inquirer</h2>
      <a href="{INQUIRER}">All Inquirer bylines</a>
    </div>
    <div class="recent-list">{''.join(map(recent_card, recent))}
    </div>
  </section>
  <section id="archive" class="archive" aria-labelledby="archive-title">
    <div class="section-heading"><h2 id="archive-title">Reporting archive</h2></div>
    <div class="search" id="archive-search" hidden>
      <label for="query">Search the archive</label>
      <input type="search" id="query" placeholder="Try wage theft or QGIS" aria-controls="clip-list">
      <p class="meta" id="search-status" role="status"></p>
    </div>
    <div id="clip-list">{''.join(map(archive_card, stories))}
    </div>
  </section>"""


CONTACT = """
  <section class="page-intro">
    <h1>Get in touch<span>.</span></h1>
    <p class="dek">Have a news tip, a question about a story or just want to drop me a line?</p>
  </section>
  <ul class="contact-list">
    <li><strong>Email</strong><a href="mailto:joe.yerardi@gmail.com">joe.yerardi@gmail.com</a></li>
    <li><strong>GitHub</strong><a href="https://github.com/JoeYerardi">JoeYerardi</a></li>
    <li><strong>LinkedIn</strong><a href="https://www.linkedin.com/in/joeyerardi">joeyerardi</a></li>
    <li><strong>X</strong><a href="https://x.com/JoeYerardi">@JoeYerardi</a></li>
  </ul>"""


def build():
    recent = load("recent.json")
    stories = load("archive.json")
    about = (CONTENT / "about.html").read_text(encoding="utf-8")
    pages = (
        ("", "Joe Yerardi | Data Journalist", "The journalism portfolio of Joe Yerardi.", home(recent[:3])),
        ("featured-work", "Featured Work | Joe Yerardi", "Selected investigations, data stories and news apps by Joe Yerardi.", archive(recent, stories)),
        ("about", "About | Joe Yerardi", "Joe Yerardi’s journalism experience, awards and education.", about),
        ("contact", "Contact | Joe Yerardi", "Contact data reporter Joe Yerardi.", CONTACT),
        ("404.html", "Page not found | Joe Yerardi", "This page could not be found.", '<section class="page-intro"><h1>Page not found<span>.</span></h1><p><a href="/">Return to the homepage</a></p></section>'),
    )
    for route, title, description, body in pages:
        target = OUTPUT / route / "index.html" if route != "404.html" else OUTPUT / route
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(title, description, route, body), encoding="utf-8")
    shutil.copytree(ROOT / "assets", OUTPUT / "assets", dirs_exist_ok=True)
    urls = "".join(f"<url><loc>{DOMAIN}/{route + '/' if route else ''}</loc></url>" for route, *_ in pages if route != "404.html")
    (OUTPUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")


if __name__ == "__main__":
    build()

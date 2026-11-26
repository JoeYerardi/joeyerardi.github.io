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
BLUESKY_HANDLE = "joeyerardi.bsky.social"
NAVIGATION = (("featured-work", "Work"), ("about", "About"), ("contact", "Contact"))
CONTACT_LINKS = (
    ("Email", "mailto:joe.yerardi@gmail.com", "joe.yerardi@gmail.com"),
    ("GitHub", "https://github.com/JoeYerardi", "JoeYerardi"),
    ("LinkedIn", "https://www.linkedin.com/in/joeyerardi", "joeyerardi"),
    ("X", "https://x.com/JoeYerardi", "@JoeYerardi"),
    ("Bluesky", f"https://bsky.app/profile/{BLUESKY_HANDLE}", f"@{BLUESKY_HANDLE}"),
)


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
    footer_links = "".join(f'<a href="{url}">{label}</a>' for label, url, _ in CONTACT_LINKS)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  {canonical}
  <link rel="stylesheet" href="{base}assets/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap masthead">
      <a class="wordmark" href="{base}">Joe Yerardi</a>
      <nav aria-label="Main navigation">{''.join(links)}</nav>
    </div>
  </header>
  <main id="main" class="wrap">{body}</main>
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <a class="wordmark" href="{base}">Joe Yerardi</a>
      <div>{footer_links}</div>
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
    <h1>Joe Yerardi</h1>
    <p class="role">Data journalist</p>
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
    <article class="archive-card">
      <p class="meta">{escape(story['publisher'])} <span aria-hidden="true">·</span> {publication_date(story['date'])}</p>
      <h3><a href="{escape(story['url'])}">{escape(story['title'])}</a></h3>
      <details><summary>Reporting notes</summary>{paragraphs}{tools}</details>
    </article>"""


def archive(recent, stories):
    return f"""
  <section class="page-intro">
    <h1>Featured work</h1>
    <p class="dek">Selected investigations, data stories and news apps.</p>
  </section>
  <section aria-labelledby="new-work" class="recent">
    <div class="section-heading">
      <h2 id="new-work">Recent work</h2>
      <a href="{INQUIRER}">All Inquirer bylines</a>
    </div>
    <div class="recent-list">{''.join(map(recent_card, recent))}
    </div>
  </section>
  <section id="archive" class="archive" aria-labelledby="archive-title">
    <div class="section-heading"><h2 id="archive-title">Older work</h2></div>
    {''.join(map(archive_card, stories))}
  </section>"""


def contact():
    items = "".join(
        f'<li><strong>{label}</strong><a href="{url}">{handle}</a></li>'
        for label, url, handle in CONTACT_LINKS
    )
    return f"""
  <section class="page-intro">
    <h1>Get in touch</h1>
    <p class="dek">Have a news tip, a question about a story or just want to drop me a line?</p>
  </section>
  <ul class="contact-list">
    {items}
  </ul>"""


def build():
    recent = load("recent.json")
    stories = load("archive.json")
    about = (CONTENT / "about.html").read_text(encoding="utf-8")
    pages = (
        ("", "Joe Yerardi | Data journalist", "The journalism portfolio of Joe Yerardi.", home(recent[:3])),
        ("featured-work", "Featured Work | Joe Yerardi", "Selected investigations, data stories and news apps by Joe Yerardi.", archive(recent, stories)),
        ("about", "About | Joe Yerardi", "Joe Yerardi’s journalism experience, awards and education.", about),
        ("contact", "Contact | Joe Yerardi", "Contact data reporter Joe Yerardi.", contact()),
        ("404.html", "Page not found | Joe Yerardi", "This page could not be found.", '<section class="page-intro"><h1>Page not found</h1><p><a href="/">Return to the homepage</a></p></section>'),
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

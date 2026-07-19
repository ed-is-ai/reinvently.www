#!/usr/bin/env python3
"""Generate Reinvently's sitemap and article feeds from the static HTML."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape, unescape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://reinvently.co.uk"
FEED_TITLE = "Reinvently — Independent AI Research & Analysis"
FEED_DESCRIPTION = (
    "Independent analysis of enterprise AI adoption, UK AI policy, "
    "model evaluation, and AI engineering tools."
)


@dataclass(frozen=True)
class Page:
    path: Path
    url: str
    title: str
    description: str
    date_published: str | None = None
    date_modified: str | None = None
    is_article: bool = False


def tag_attributes(tag: str) -> dict[str, str]:
    attributes: dict[str, str] = {}
    for match in re.finditer(r'([:\w-]+)\s*=\s*(["\'])(.*?)\2', tag, re.DOTALL):
        attributes[match.group(1).lower()] = unescape(match.group(3).strip())
    return attributes


def extract_meta(source: str, name: str) -> str:
    for tag in re.findall(r"<meta\b[^>]*>", source, flags=re.IGNORECASE | re.DOTALL):
        attributes = tag_attributes(tag)
        if attributes.get("name", "").lower() == name.lower():
            return attributes.get("content", "")
    return ""


def extract_canonical(source: str) -> str:
    for tag in re.findall(r"<link\b[^>]*>", source, flags=re.IGNORECASE | re.DOTALL):
        attributes = tag_attributes(tag)
        if attributes.get("rel", "").lower() == "canonical":
            return attributes.get("href", "")
    return ""


def extract_title(source: str) -> str:
    match = re.search(r"<title>(.*?)</title>", source, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return unescape(re.sub(r"\s+", " ", match.group(1)).strip())


def json_ld_objects(source: str) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    blocks = re.findall(
        r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',
        source,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for block in blocks:
        try:
            value = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            objects.append(value)
        elif isinstance(value, list):
            objects.extend(item for item in value if isinstance(item, dict))
    return objects


def discover_pages() -> list[Page]:
    pages: list[Page] = []
    html_files = [ROOT / "index.html", *sorted(ROOT.glob("**/index.html"))]

    for path in dict.fromkeys(html_files):
        source = path.read_text(encoding="utf-8")
        robots = extract_meta(source, "robots").lower()
        if "noindex" in robots:
            continue

        canonical = extract_canonical(source)
        if not canonical.startswith(f"{SITE_URL}/") and canonical != f"{SITE_URL}/":
            continue

        structured_data = json_ld_objects(source)
        article = next(
            (item for item in structured_data if item.get("@type") == "BlogPosting"),
            None,
        )
        dated_entity = article or next(
            (
                item
                for item in structured_data
                if item.get("dateModified") or item.get("datePublished")
            ),
            None,
        )
        description = extract_meta(source, "description")
        if article and not description:
            description = str(article.get("description", ""))

        pages.append(
            Page(
                path=path.relative_to(ROOT),
                url=canonical,
                title=extract_title(source),
                description=description,
                date_published=(
                    str(dated_entity.get("datePublished"))
                    if dated_entity and dated_entity.get("datePublished")
                    else None
                ),
                date_modified=(
                    str(dated_entity.get("dateModified"))
                    if dated_entity and dated_entity.get("dateModified")
                    else None
                ),
                is_article=article is not None,
            )
        )

    return sorted(pages, key=lambda page: (page.url != f"{SITE_URL}/", page.url))


def iso_datetime(date: str) -> str:
    return f"{date}T00:00:00Z"


def rss_datetime(date: str) -> str:
    parsed = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return format_datetime(parsed)


def xml_text(value: str) -> str:
    return escape(value, quote=True)


def build_sitemap(pages: list[Page]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in pages:
        lines.extend(("  <url>", f"    <loc>{xml_text(page.url)}</loc>"))
        if page.date_modified:
            lines.append(f"    <lastmod>{page.date_modified}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def articles_by_date(pages: list[Page]) -> list[Page]:
    return sorted(
        (page for page in pages if page.is_article and page.date_published),
        key=lambda page: (page.date_published or "", page.url),
        reverse=True,
    )


def build_atom(articles: list[Page]) -> str:
    updated = max((article.date_modified or article.date_published or "" for article in articles))
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f"  <title>{xml_text(FEED_TITLE)}</title>",
        f'  <link href="{SITE_URL}/"/>',
        f'  <link href="{SITE_URL}/f.atom" rel="self" type="application/atom+xml"/>',
        f"  <updated>{iso_datetime(updated)}</updated>",
        f"  <id>{SITE_URL}/</id>",
        f"  <subtitle>{xml_text(FEED_DESCRIPTION)}</subtitle>",
    ]
    for article in articles:
        lines.extend(
            (
                "  <entry>",
                f"    <title>{xml_text(article.title.removesuffix(' — Reinvently'))}</title>",
                f'    <link href="{article.url}"/>',
                f"    <id>{article.url}</id>",
                f"    <published>{iso_datetime(article.date_published or '')}</published>",
                f"    <updated>{iso_datetime(article.date_modified or article.date_published or '')}</updated>",
                "    <author><name>Ed Yau</name></author>",
                f"    <summary>{xml_text(article.description)}</summary>",
                "  </entry>",
            )
        )
    lines.append("</feed>")
    return "\n".join(lines) + "\n"


def build_rss(articles: list[Page]) -> str:
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<rss version="2.0">',
        "  <channel>",
        f"    <title>{xml_text(FEED_TITLE)}</title>",
        f"    <link>{SITE_URL}/</link>",
        f"    <description>{xml_text(FEED_DESCRIPTION)}</description>",
        "    <language>en-gb</language>",
    ]
    for article in articles:
        lines.extend(
            (
                "    <item>",
                f"      <title>{xml_text(article.title.removesuffix(' — Reinvently'))}</title>",
                f"      <link>{article.url}</link>",
                f'      <guid isPermaLink="true">{article.url}</guid>',
                f"      <pubDate>{rss_datetime(article.date_published or '')}</pubDate>",
                f"      <description>{xml_text(article.description)}</description>",
                "    </item>",
            )
        )
    lines.extend(("  </channel>", "</rss>"))
    return "\n".join(lines) + "\n"


def build_json_feed(articles: list[Page]) -> str:
    payload = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": FEED_TITLE,
        "home_page_url": f"{SITE_URL}/",
        "feed_url": f"{SITE_URL}/f.json",
        "description": FEED_DESCRIPTION,
        "authors": [{"name": "Ed Yau", "url": "https://uk.linkedin.com/in/edmond-yau"}],
        "language": "en-GB",
        "items": [
            {
                "id": article.url,
                "url": article.url,
                "title": article.title.removesuffix(" — Reinvently"),
                "summary": article.description,
                "date_published": iso_datetime(article.date_published or ""),
                "date_modified": iso_datetime(article.date_modified or article.date_published or ""),
                "authors": [
                    {"name": "Ed Yau", "url": "https://uk.linkedin.com/in/edmond-yau"}
                ],
            }
            for article in articles
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    pages = discover_pages()
    articles = articles_by_date(pages)

    (ROOT / "sitemap.xml").write_text(build_sitemap(pages), encoding="utf-8")
    (ROOT / "f.atom").write_text(build_atom(articles), encoding="utf-8")
    (ROOT / "f.rss").write_text(build_rss(articles), encoding="utf-8")
    (ROOT / "f.json").write_text(build_json_feed(articles), encoding="utf-8")

    print(f"Generated discovery files for {len(pages)} pages and {len(articles)} articles.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check Reinvently's static HTML for the SEO invariants that rot silently.

Everything here has an objectively right answer, so a failure is a defect
rather than an opinion. Prose quality, readability and tone are deliberately
out of scope: they are judgement calls and belong in an advisory linter, not
in a job that blocks a merge.

    python3 scripts/check_seo.py                  # every blog post
    python3 scripts/check_seo.py blog/rag-vs-graphrag/index.html
    python3 scripts/check_seo.py --format github  # inline PR annotations
    python3 scripts/check_seo.py --strict         # warnings fail too

Exits 1 when any error is found, 0 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://reinvently.co.uk"

# Google truncates around these lengths. Outside the range is a warning, not a
# defect — an occasional long title is a reasonable editorial choice.
TITLE_RANGE = (30, 65)
DESCRIPTION_RANGE = (110, 165)

REQUIRED_OG = ("og:title", "og:description", "og:image", "og:url", "og:type")
REQUIRED_TWITTER = ("twitter:card", "twitter:title", "twitter:description")
REQUIRED_BLOGPOSTING = (
    "headline",
    "description",
    "datePublished",
    "dateModified",
    "image",
    "author",
    "publisher",
    "url",
)

# Links we cannot resolve on disk and do not want to hear about.
SKIP_LINK_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:")


@dataclass
class Problem:
    path: Path
    line: int
    message: str
    is_error: bool = True

    def render(self, fmt: str) -> str:
        rel = self.path.relative_to(ROOT)
        if fmt == "github":
            level = "error" if self.is_error else "warning"
            # Annotations must not contain raw newlines.
            message = self.message.replace("\n", " ")
            return f"::{level} file={rel},line={self.line}::{message}"
        label = "ERROR" if self.is_error else "warn "
        return f"{label} {rel}:{self.line}  {self.message}"


@dataclass
class Document:
    """The parts of a page the checks care about, with source line numbers."""

    path: Path
    lang: str | None = None
    title: str | None = None
    title_line: int = 1
    metas: dict[str, tuple[str, int]] = field(default_factory=dict)
    canonical: tuple[str, int] | None = None
    headings: list[tuple[int, int]] = field(default_factory=list)
    images: list[tuple[dict[str, str], int]] = field(default_factory=list)
    links: list[tuple[str, int]] = field(default_factory=list)
    json_ld: list[tuple[str, int]] = field(default_factory=list)


class DocumentParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.doc = Document(path=path)
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._buffer_line = 1
        # The inline charts carry <title> tooltips and their own <a>/<text>
        # nodes. None of that is page metadata, so it is skipped wholesale.
        self._svg_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {k.lower(): (v or "") for k, v in attrs}
        line = self.getpos()[0]

        if tag == "svg":
            self._svg_depth += 1
            return
        if self._svg_depth:
            return

        if tag == "html":
            self.doc.lang = attributes.get("lang")
        elif tag == "title" and self.doc.title is None:
            self._start_capture("title", line)
        elif tag == "meta":
            # name= covers description and twitter:*, property= covers og:*.
            key = attributes.get("name") or attributes.get("property")
            if key:
                self.doc.metas.setdefault(key.lower(), (attributes.get("content", ""), line))
        elif tag == "link" and attributes.get("rel", "").lower() == "canonical":
            if self.doc.canonical is None:
                self.doc.canonical = (attributes.get("href", ""), line)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.doc.headings.append((int(tag[1]), line))
        elif tag == "img":
            self.doc.images.append((attributes, line))
        elif tag == "a" and "href" in attributes:
            self.doc.links.append((attributes["href"], line))
        elif tag == "script":
            if attributes.get("type", "").lower() == "application/ld+json":
                self._start_capture("json_ld", line)

    def handle_endtag(self, tag: str) -> None:
        if tag == "svg":
            self._svg_depth = max(0, self._svg_depth - 1)
            return
        if self._svg_depth:
            return

        if self._capture == "title" and tag == "title":
            self.doc.title = "".join(self._buffer).strip()
            self.doc.title_line = self._buffer_line
            self._stop_capture()
        elif self._capture == "json_ld" and tag == "script":
            self.doc.json_ld.append(("".join(self._buffer), self._buffer_line))
            self._stop_capture()

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)

    def _start_capture(self, kind: str, line: int) -> None:
        self._capture = kind
        self._buffer = []
        self._buffer_line = line

    def _stop_capture(self) -> None:
        self._capture = None
        self._buffer = []


def parse(path: Path) -> Document:
    parser = DocumentParser(path)
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser.doc


def site_url_to_path(url: str) -> Path | None:
    """Map an on-site absolute URL to the file it should be served from."""
    if not url.startswith(SITE_URL):
        return None
    relative = urlsplit(url[len(SITE_URL) :]).path.lstrip("/")
    target = ROOT / relative
    return target / "index.html" if url.endswith("/") else target


def expected_canonical(path: Path) -> str:
    directory = path.parent.relative_to(ROOT).as_posix()
    return f"{SITE_URL}/" if directory == "." else f"{SITE_URL}/{directory}/"


def sitemap_urls() -> set[str]:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        return set()
    return set(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap.read_text(encoding="utf-8")))


def check_metadata(doc: Document, problems: list[Problem]) -> None:
    def error(line: int, message: str) -> None:
        problems.append(Problem(doc.path, line, message))

    def warn(line: int, message: str) -> None:
        problems.append(Problem(doc.path, line, message, is_error=False))

    if not doc.lang:
        error(1, "<html> has no lang attribute")

    if not doc.title:
        error(1, "missing or empty <title>")
    else:
        low, high = TITLE_RANGE
        if not low <= len(doc.title) <= high:
            warn(doc.title_line, f"title is {len(doc.title)} chars, outside {low}-{high}")

    description = doc.metas.get("description")
    if not description or not description[0].strip():
        error(1, "missing meta description")
    else:
        low, high = DESCRIPTION_RANGE
        if not low <= len(description[0]) <= high:
            warn(description[1], f"meta description is {len(description[0])} chars, outside {low}-{high}")

    for key in REQUIRED_OG + REQUIRED_TWITTER:
        entry = doc.metas.get(key)
        if not entry or not entry[0].strip():
            error(1, f"missing {key}")

    if "og:image:alt" not in doc.metas:
        warn(1, "no og:image:alt — social cards lose their alt text")


def check_canonical(doc: Document, sitemap: set[str], problems: list[Problem]) -> None:
    if doc.canonical is None:
        problems.append(Problem(doc.path, 1, "missing rel=canonical"))
        return

    href, line = doc.canonical
    expected = expected_canonical(doc.path)
    if href != expected:
        problems.append(Problem(doc.path, line, f"canonical is {href!r}, expected {expected!r}"))

    og_url = doc.metas.get("og:url")
    if og_url and og_url[0] != href:
        problems.append(Problem(doc.path, og_url[1], f"og:url {og_url[0]!r} does not match canonical {href!r}"))

    if sitemap and href not in sitemap:
        problems.append(
            Problem(doc.path, line, f"{href} is absent from sitemap.xml — rerun scripts/build_discovery.py")
        )


def check_headings(doc: Document, problems: list[Problem]) -> None:
    h1s = [line for level, line in doc.headings if level == 1]
    if not h1s:
        problems.append(Problem(doc.path, 1, "no <h1>"))
    elif len(h1s) > 1:
        problems.append(Problem(doc.path, h1s[1], f"{len(h1s)} <h1> elements, expected exactly one"))

    previous = None
    for level, line in doc.headings:
        if previous is not None and level > previous + 1:
            problems.append(Problem(doc.path, line, f"heading jumps from h{previous} to h{level}"))
        previous = level


def check_images(doc: Document, problems: list[Problem]) -> None:
    for attributes, line in doc.images:
        if not attributes.get("alt", "").strip():
            src = attributes.get("src", "?")
            problems.append(Problem(doc.path, line, f"<img src={src!r}> has no alt text"))

    og_image = doc.metas.get("og:image")
    if og_image:
        target = site_url_to_path(og_image[0])
        if target is None:
            problems.append(Problem(doc.path, og_image[1], f"og:image {og_image[0]!r} is not on {SITE_URL}"))
        elif not target.exists():
            relative = target.relative_to(ROOT)
            problems.append(Problem(doc.path, og_image[1], f"og:image file {relative} does not exist"))


_anchor_cache: dict[Path, set[str]] = {}


def anchors_in(path: Path) -> set[str]:
    """Every id= on a page, so #fragments can be resolved against it."""
    if path not in _anchor_cache:
        text = path.read_text(encoding="utf-8", errors="replace")
        _anchor_cache[path] = set(re.findall(r'\bid\s*=\s*["\']([^"\']+)["\']', text))
    return _anchor_cache[path]


def check_links(doc: Document, problems: list[Problem]) -> None:
    for href, line in doc.links:
        if not href or href.lower().startswith(SKIP_LINK_SCHEMES):
            continue

        parts = urlsplit(href)
        fragment = unquote(parts.fragment)

        if not parts.path:
            # A same-page anchor: resolve it against this document.
            if fragment and fragment not in anchors_in(doc.path):
                problems.append(Problem(doc.path, line, f"link {href!r} has no matching id on this page"))
            continue

        if parts.path.startswith("/"):
            target = ROOT / parts.path.lstrip("/")
        else:
            target = (doc.path.parent / parts.path).resolve()

        if target.is_dir():
            target = target / "index.html"

        if not target.exists():
            problems.append(Problem(doc.path, line, f"internal link {href!r} does not resolve"))
        elif fragment and target.suffix == ".html" and fragment not in anchors_in(target):
            relative = target.relative_to(ROOT)
            problems.append(Problem(doc.path, line, f"link {href!r} points at an id absent from {relative}"))


def check_structured_data(doc: Document, problems: list[Problem]) -> None:
    blocks = []
    for raw, line in doc.json_ld:
        try:
            blocks.append((json.loads(raw), line))
        except json.JSONDecodeError as exc:
            problems.append(Problem(doc.path, line, f"JSON-LD block does not parse: {exc.msg} at line {exc.lineno}"))

    posting = next((block for block, _ in blocks if block.get("@type") == "BlogPosting"), None)
    if posting is None:
        problems.append(Problem(doc.path, 1, "no BlogPosting JSON-LD"))
        return

    line = next(line for block, line in blocks if block.get("@type") == "BlogPosting")
    missing = [key for key in REQUIRED_BLOGPOSTING if not posting.get(key)]
    if missing:
        problems.append(Problem(doc.path, line, f"BlogPosting missing {', '.join(missing)}"))

    published, modified = posting.get("datePublished"), posting.get("dateModified")
    if published and modified and modified < published:
        problems.append(Problem(doc.path, line, f"dateModified {modified} precedes datePublished {published}"))

    if doc.canonical and posting.get("url") and posting["url"] != doc.canonical[0]:
        problems.append(
            Problem(doc.path, line, f"BlogPosting url {posting['url']!r} does not match canonical {doc.canonical[0]!r}")
        )


def check(path: Path, sitemap: set[str]) -> list[Problem]:
    problems: list[Problem] = []
    doc = parse(path)
    check_metadata(doc, problems)
    check_canonical(doc, sitemap, problems)
    check_headings(doc, problems)
    check_images(doc, problems)
    check_links(doc, problems)
    check_structured_data(doc, problems)
    return problems


def default_targets() -> list[Path]:
    """Every blog post, plus a warning for any post directory missing its page."""
    return sorted(ROOT.glob("blog/*/index.html"))


def orphan_directories() -> list[Path]:
    return sorted(d for d in ROOT.glob("blog/*/") if d.is_dir() and not (d / "index.html").exists())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", type=Path, help="HTML files to check (default: every blog post)")
    parser.add_argument("--format", choices=("text", "github"), default="text", help="output style")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()

    targets = [p.resolve() for p in args.paths] if args.paths else default_targets()
    if not targets:
        print("no pages to check", file=sys.stderr)
        return 1

    sitemap = sitemap_urls()
    problems: list[Problem] = []
    for path in targets:
        if not path.exists():
            print(f"no such file: {path}", file=sys.stderr)
            return 1
        problems.extend(check(path, sitemap))

    if not args.paths:
        for directory in orphan_directories():
            problems.append(
                Problem(directory / "index.html", 1, "post directory has no index.html", is_error=False)
            )

    for problem in problems:
        print(problem.render(args.format))

    errors = sum(1 for p in problems if p.is_error)
    warnings = len(problems) - errors
    print(f"\n{len(targets)} pages checked: {errors} errors, {warnings} warnings", file=sys.stderr)

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

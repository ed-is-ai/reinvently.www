#!/usr/bin/env python3
"""Run and archive the reproducible OpenAlex search used for the PRISMA update."""

from __future__ import annotations

import csv
import html
import json
import re
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTICLE = ROOT / "blog/ai-coding-productivity-evidence/index.html"
OUTPUT_DIR = Path(__file__).resolve().parent
SEARCH_DATE = "2026-07-29"
PUBLICATION_START = "2024-01-01"
PUBLICATION_END = "2026-07-28"

QUERIES = [
    ("Q01", "AI coding assistant"),
    ("Q02", "AI code assistant"),
    ("Q03", "AI-assisted programming"),
    ("Q04", "AI-assisted software development"),
    ("Q05", "generative AI software development"),
    ("Q06", "coding agent"),
    ("Q07", "agentic coding"),
    ("Q08", "agentic code review"),
    ("Q09", "GitHub Copilot productivity"),
    ("Q10", "software development productivity AI"),
    ("Q11", "AI code review"),
    ("Q12", "AI generated code maintainability"),
    ("Q13", "AI generated code security"),
    ("Q14", "spec-driven development"),
]

AI_TERMS = (
    "artificial intelligence",
    "generative ai",
    "genai",
    "large language model",
    " llm",
    "chatgpt",
    "copilot",
    "coding agent",
    "code agent",
    "code assistant",
    "ai-assisted",
    "ai generated",
    "ai-generated",
    "agentic",
)
SOFTWARE_TERMS = (
    "software",
    "code",
    "coding",
    "programmer",
    "programming",
    "developer",
    "repository",
    "pull request",
    "code review",
    "unit test",
    "debug",
    "maintainab",
)
EVIDENCE_TERMS = (
    "productiv",
    "experiment",
    "trial",
    "empirical",
    "evaluation",
    "impact",
    "effect",
    "performance",
    "throughput",
    "task time",
    "completion time",
    "quality",
    "security",
    "maintainab",
    "review",
    "deployment",
    "release",
    "adoption",
    "experience",
)
WORKFLOW_TERMS = (
    "developer",
    "programmer",
    "software engineer",
    "engineering team",
    "workplace",
    "enterprise",
    "organisation",
    "organization",
    "repository",
    "pull request",
    "code review",
    "software project",
    "coding task",
    "deployment",
    "release",
    "adoption",
)
DESIGN_TERMS = (
    "randomized",
    "randomised",
    "experiment",
    "trial",
    "controlled",
    "comparative",
    "comparison",
    "observational",
    "longitudinal",
    "empirical",
    "field study",
    "case study",
    "survey",
    "telemetry",
    "participants",
    "developers",
    "repositories",
    "pull requests",
)


def normalise_title(value: str) -> str:
    value = html.unescape(value).lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def normalise_doi(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return value


def abstract_from_index(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, offsets in index.items():
        positions.extend((offset, word) for offset in offsets)
    return " ".join(word for _, word in sorted(positions))


class CorpusParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.heading_tag = ""
        self.heading_parts: list[str] = []
        self.category = ""
        self.awaiting_register = False
        self.in_register = False
        self.register_depth = 0
        self.in_item = False
        self.item_parts: list[str] = []
        self.item_links: list[str] = []
        self.records: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "h3":
            self.heading_tag = tag
            self.heading_parts = []
        elif tag == "ul" and (
            "source-register" in (attr.get("class") or "").split() or self.awaiting_register
        ):
            self.in_register = True
            self.register_depth = 1
            self.awaiting_register = False
        elif tag == "ul" and self.in_register:
            self.register_depth += 1
        elif tag == "li" and self.in_register:
            self.in_item = True
            self.item_parts = []
            self.item_links = []
        elif tag == "a" and self.in_item and attr.get("href"):
            self.item_links.append(attr["href"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "h3" and self.heading_tag:
            heading = " ".join("".join(self.heading_parts).split())
            if heading.startswith("A."):
                self.category = "empirical"
            elif heading.startswith("B."):
                self.category = "secondary_synthesis"
            elif heading.startswith("C."):
                self.category = "contextual"
            if self.category:
                self.awaiting_register = True
            self.heading_tag = ""
        elif tag == "li" and self.in_item:
            text = " ".join("".join(self.item_parts).split())
            study_match = re.search(r"\bST-\d{2}\b", text)
            title = text
            if " — " in text:
                parts = [part.strip() for part in text.split(" — ") if part.strip()]
                if study_match and len(parts) > 1:
                    title = parts[1]
                elif parts:
                    title = parts[0]
            self.records.append(
                {
                    "existing_category": self.category,
                    "study_id": study_match.group(0) if study_match else "",
                    "title": title.rstrip("."),
                    "url": next(
                        (link for link in self.item_links if link.startswith(("http://", "https://"))),
                        "",
                    ),
                }
            )
            self.in_item = False
        elif tag == "ul" and self.in_register:
            self.register_depth -= 1
            if self.register_depth == 0:
                self.in_register = False

    def handle_data(self, data: str) -> None:
        if self.heading_tag:
            self.heading_parts.append(data)
        if self.in_item:
            self.item_parts.append(data)


def extract_existing_corpus() -> list[dict[str, str]]:
    parser = CorpusParser()
    parser.feed(ARTICLE.read_text(encoding="utf-8"))
    counts = defaultdict(int)
    for record in parser.records:
        counts[record["existing_category"]] += 1
    expected = {"empirical": 59, "secondary_synthesis": 2, "contextual": 55}
    if dict(counts) != expected:
        raise RuntimeError(f"Unexpected corpus counts: {dict(counts)}; expected {expected}")
    return parser.records


def openalex_url(phrase: str, cursor: str) -> str:
    filters = ",".join(
        [
            f"from_publication_date:{PUBLICATION_START}",
            f"to_publication_date:{PUBLICATION_END}",
            "language:en",
            f'title_and_abstract.search:"{phrase}"',
        ]
    )
    params = {
        "filter": filters,
        "per-page": "200",
        "cursor": cursor,
        "select": ",".join(
            [
                "id",
                "doi",
                "title",
                "publication_year",
                "publication_date",
                "type",
                "language",
                "primary_location",
                "open_access",
                "abstract_inverted_index",
            ]
        ),
    }
    return "https://api.openalex.org/works?" + urllib.parse.urlencode(params)


def fetch_json(url: str) -> dict:
    for attempt in range(6):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Reinvently systematic review (https://reinvently.co.uk/)"},
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code != 429 or attempt == 5:
                raise
            retry_after = int(error.headers.get("Retry-After", "0") or "0")
            time.sleep(max(retry_after, min(30, 2 ** (attempt + 1))))
    raise RuntimeError("OpenAlex request failed after retries")


def run_searches() -> tuple[list[dict], list[dict[str, str]]]:
    works: dict[str, dict] = {}
    query_matches: dict[str, set[str]] = defaultdict(set)
    search_log: list[dict[str, str]] = []

    for query_id, phrase in QUERIES:
        cursor = "*"
        query_count = 0
        pages = 0
        while cursor:
            payload = fetch_json(openalex_url(phrase, cursor))
            pages += 1
            if pages == 1:
                query_count = int(payload["meta"]["count"])
            for work in payload.get("results", []):
                work_id = work["id"]
                works[work_id] = work
                query_matches[work_id].add(query_id)
            next_cursor = payload["meta"].get("next_cursor")
            if not next_cursor or not payload.get("results"):
                break
            cursor = next_cursor
            time.sleep(0.12)
        search_log.append(
            {
                "query_id": query_id,
                "source": "OpenAlex",
                "search_date": SEARCH_DATE,
                "publication_start": PUBLICATION_START,
                "publication_end": PUBLICATION_END,
                "field": "title and abstract",
                "query": phrase,
                "records_returned_before_cross_query_deduplication": str(query_count),
            }
        )

    output: list[dict] = []
    for work_id, work in works.items():
        record = dict(work)
        record["query_ids"] = sorted(query_matches[work_id])
        output.append(record)
    return output, search_log


def automated_screen(title: str, abstract: str, publication_type: str) -> tuple[str, str]:
    text = f" {title} {abstract}".lower()
    if publication_type not in {
        "article",
        "conference-paper",
        "preprint",
        "report",
        "dissertation",
    }:
        return "exclude", "Ineligible publication type for the empirical stream"
    if not any(term in text for term in AI_TERMS):
        return "exclude", "No AI coding intervention indicated"
    if not any(term in text for term in SOFTWARE_TERMS):
        return "exclude", "Outside software-development scope"
    if not any(term in text for term in WORKFLOW_TERMS):
        return "exclude", "No identifiable developer, team or repository workflow"
    if not any(term in text for term in DESIGN_TERMS):
        return "exclude", "No empirical study design indicated"
    if not any(term in text for term in EVIDENCE_TERMS):
        return "exclude", "No empirical productivity or adjacent outcome indicated"
    return "human_review", "Potentially eligible from title or abstract"


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def merge_records(existing: list[dict[str, str]], works: list[dict]) -> list[dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    doi_to_key: dict[str, str] = {}

    for record in existing:
        doi = normalise_doi(record["url"]) if "doi.org/" in record["url"] else ""
        key = f"title:{normalise_title(record['title'])}"
        merged[key] = {
            "title": record["title"],
            "publication_year": "",
            "publication_type": "",
            "doi": doi,
            "url": record["url"],
            "openalex_id": "",
            "record_sources": "existing_corpus",
            "query_ids": "",
            "existing_category": record["existing_category"],
            "study_id": record["study_id"],
            "abstract": "",
            "automated_screen": (
                "include_empirical"
                if record["existing_category"] == "empirical"
                else "route_supporting"
            ),
            "automated_reason": (
                "Included empirical study in locked corpus"
                if record["existing_category"] == "empirical"
                else "Secondary or contextual evidence stream"
            ),
            "human_decision": (
                "include_empirical"
                if record["existing_category"] == "empirical"
                else "route_supporting"
            ),
            "exclusion_reason": "",
        }
        if doi:
            doi_to_key[doi] = key

    for work in works:
        doi = normalise_doi(work.get("doi") or "")
        title = work.get("title") or ""
        title_key = f"title:{normalise_title(title)}"
        if doi and doi in doi_to_key:
            key = doi_to_key[doi]
        elif title_key in merged:
            key = title_key
        else:
            key = title_key
        location = work.get("primary_location") or {}
        url = location.get("landing_page_url") or work.get("doi") or work.get("id") or ""
        abstract = abstract_from_index(work.get("abstract_inverted_index"))
        decision, reason = automated_screen(title, abstract, work.get("type") or "")
        if key in merged:
            current = merged[key]
            sources = set(current["record_sources"].split(";"))
            sources.add("OpenAlex")
            current["record_sources"] = ";".join(sorted(sources))
            query_ids = set(filter(None, current["query_ids"].split(";")))
            query_ids.update(work.get("query_ids", []))
            current["query_ids"] = ";".join(sorted(query_ids))
            current["openalex_id"] = work.get("id") or ""
            current["publication_year"] = str(work.get("publication_year") or "")
            current["publication_type"] = work.get("type") or ""
            if not current["doi"]:
                current["doi"] = doi
            if not current["abstract"]:
                current["abstract"] = abstract
            continue
        merged[key] = {
            "title": title,
            "publication_year": str(work.get("publication_year") or ""),
            "publication_type": work.get("type") or "",
            "doi": doi,
            "url": url,
            "openalex_id": work.get("id") or "",
            "record_sources": "OpenAlex",
            "query_ids": ";".join(work.get("query_ids", [])),
            "existing_category": "",
            "study_id": "",
            "abstract": abstract,
            "automated_screen": decision,
            "automated_reason": reason,
            "human_decision": "pending" if decision == "human_review" else "exclude_title_abstract",
            "exclusion_reason": "" if decision == "human_review" else reason,
        }
        if doi:
            doi_to_key[doi] = key

    rows = sorted(
        merged.values(),
        key=lambda item: (
            item["existing_category"] == "",
            normalise_title(item["title"]),
        ),
    )
    for number, row in enumerate(rows, start=1):
        row["record_id"] = f"R-{number:04d}"
    return rows


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    existing = extract_existing_corpus()
    works, search_log = run_searches()
    master = merge_records(existing, works)

    write_csv(
        OUTPUT_DIR / "existing-corpus.csv",
        existing,
        ["existing_category", "study_id", "title", "url"],
    )
    write_csv(
        OUTPUT_DIR / "search-log.csv",
        search_log,
        [
            "query_id",
            "source",
            "search_date",
            "publication_start",
            "publication_end",
            "field",
            "query",
            "records_returned_before_cross_query_deduplication",
        ],
    )
    with (OUTPUT_DIR / "openalex-records.jsonl").open("w", encoding="utf-8") as handle:
        for work in sorted(works, key=lambda item: item["id"]):
            handle.write(json.dumps(work, ensure_ascii=False) + "\n")
    write_csv(
        OUTPUT_DIR / "screening-register.csv",
        master,
        [
            "record_id",
            "title",
            "publication_year",
            "publication_type",
            "doi",
            "url",
            "openalex_id",
            "record_sources",
            "query_ids",
            "existing_category",
            "study_id",
            "automated_screen",
            "automated_reason",
            "human_decision",
            "exclusion_reason",
            "abstract",
        ],
    )

    summary = {
        "existing_corpus_records": len(existing),
        "openalex_records_before_cross_source_deduplication": len(works),
        "master_records_after_cross_source_deduplication": len(master),
        "pending_human_review": sum(row["human_decision"] == "pending" for row in master),
        "initial_rule_based_exclusions": sum(
            row["human_decision"] == "exclude_title_abstract" for row in master
        ),
        "empirical_records_from_locked_corpus": sum(
            row["human_decision"] == "include_empirical" for row in master
        ),
        "supporting_records_from_locked_corpus": sum(
            row["human_decision"] == "route_supporting" for row in master
        ),
    }
    (OUTPUT_DIR / "search-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Enumerate priority software-engineering journals and deduplicate candidates."""

from __future__ import annotations

import csv
import gzip
import html
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SEARCH_DATE = "2026-07-31"
PUBLICATION_START = "2022-01-01"
PUBLICATION_END = "2026-07-31"

JOURNALS = [
    ("J01", "Empirical Software Engineering", "1382-3256"),
    ("J02", "IEEE Transactions on Software Engineering", "0098-5589"),
    ("J03", "ACM Transactions on Software Engineering and Methodology", "1049-331X"),
    ("J04", "Journal of Systems and Software", "0164-1212"),
    ("J05", "Information and Software Technology", "0950-5849"),
    ("J06", "IEEE Software", "0740-7459"),
    ("J07", "Automated Software Engineering", "0928-8910"),
    ("J08", "Software Quality Journal", "0963-9314"),
    ("J09", "Journal of Software: Evolution and Process", "2047-7481"),
    ("J10", "Software: Practice and Experience", "0038-0644"),
    ("J11", "Science of Computer Programming", "0167-6423"),
    ("J12", "Requirements Engineering", "0947-3602"),
    ("J13", "ACM Transactions on Computing Education", "1946-6226"),
    ("J14", "IEEE Transactions on Dependable and Secure Computing", "1545-5971"),
    ("J15", "ACM Transactions on Privacy and Security", "2471-2566"),
]

AI_PATTERNS = [
    r"\bgenerative ai\b",
    r"\bgenai\b",
    r"\blarge language model",
    r"\bllms?\b",
    r"\bchatgpt\b",
    r"\bcopilot\b",
    r"\bcode assistants?\b",
    r"\bcoding assistants?\b",
    r"\bprogramming assistants?\b",
    r"\bcoding agents?\b",
    r"\bagentic\b",
    r"\bfoundation models?\b",
    r"\bai-assisted\b",
    r"\bai-generated\b",
    r"\bai pair programming\b",
]
SOFTWARE_PATTERNS = [
    r"\bsoftware\b",
    r"\bcode\b",
    r"\bcoding\b",
    r"\bprogram",
    r"\bdeveloper",
    r"\brepositor",
    r"\bpull request",
    r"\bcode review",
    r"\btest",
    r"\bdebug",
    r"\bmaintain",
    r"\brefactor",
    r"\brequirement",
]


def normalise_title(value: str) -> str:
    value = html.unescape(value).lower()
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def normalise_doi(value: str) -> str:
    value = value.strip().lower()
    return re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)


def clean_markup(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(value.split())


def first_text(value: object) -> str:
    if isinstance(value, list):
        return clean_markup(str(value[0])) if value else ""
    return clean_markup(str(value or ""))


def publication_year(record: dict) -> str:
    for field in ("published-online", "published-print", "published", "issued"):
        parts = (record.get(field) or {}).get("date-parts") or []
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def crossref_url(issn: str, cursor: str) -> str:
    params = {
        "filter": ",".join(
            [
                f"from-pub-date:{PUBLICATION_START}",
                f"until-pub-date:{PUBLICATION_END}",
                "type:journal-article",
            ]
        ),
        "rows": "1000",
        "cursor": cursor,
    }
    return f"https://api.crossref.org/journals/{issn}/works?" + urllib.parse.urlencode(params)


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Reinvently systematic review (https://reinvently.co.uk/)",
        },
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response)


def archive_record(record: dict) -> dict:
    fields = [
        "title",
        "abstract",
        "DOI",
        "URL",
        "type",
        "subtype",
        "published-online",
        "published-print",
        "published",
        "issued",
        "journal_search_id",
        "journal_search_name",
        "journal_search_issn",
    ]
    return {field: record[field] for field in fields if field in record}


def fetch_journal(venue_id: str, journal: str, issn: str) -> tuple[list[dict], int]:
    records: list[dict] = []
    cursor = "*"
    total = 0
    while cursor:
        payload = fetch_json(crossref_url(issn, cursor))
        message = payload["message"]
        total = int(message.get("total-results") or total)
        items = message.get("items") or []
        for item in items:
            item["journal_search_id"] = venue_id
            item["journal_search_name"] = journal
            item["journal_search_issn"] = issn
            records.append(archive_record(item))
        next_cursor = message.get("next-cursor")
        if not items or len(records) >= total or not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor
        time.sleep(0.15)
    return records, total


def candidate_reason(title: str, abstract: str) -> tuple[bool, str]:
    text = f" {title} {abstract} ".lower()
    ai_matches = [pattern for pattern in AI_PATTERNS if re.search(pattern, text)]
    software_matches = [pattern for pattern in SOFTWARE_PATTERNS if re.search(pattern, text)]
    if not ai_matches:
        return False, "No generative-AI or AI-coding marker in title/abstract"
    if not software_matches:
        return False, "No software-development marker in title/abstract"
    return True, "AI-coding and software-development markers present"


def included_documents() -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []
    with (HERE / "existing-corpus.csv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            documents.append(row)
    with (HERE / "report-assessments.csv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["full_text_decision"] in {
                "include_productivity",
                "include_adjacent",
                "upgrade_existing_adjacent",
            }:
                documents.append(row)
    return documents


def prior_openalex_records() -> list[dict[str, str]]:
    with (HERE / "screening-register.csv").open(
        encoding="utf-8",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def dedupe_status(
    title: str,
    doi: str,
    included_titles: set[str],
    included_dois: set[str],
    prior_titles: set[str],
    prior_dois: set[str],
) -> str:
    if doi and doi in included_dois:
        return "duplicate_included_doi"
    if normalise_title(title) in included_titles:
        return "duplicate_included_title"
    if doi and doi in prior_dois:
        return "prior_openalex_record_reassessed"
    if normalise_title(title) in prior_titles:
        return "prior_openalex_record_reassessed"
    return "unique_for_screening"


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


def main() -> None:
    snapshot = HERE / "journal-records.jsonl.gz"
    reuse_snapshot = "--reuse-snapshot" in sys.argv
    if reuse_snapshot:
        raw_records = [
            archive_record(json.loads(line))
            for line in gzip.open(snapshot, "rt", encoding="utf-8")
            if line
        ]
        totals: defaultdict[str, int] = defaultdict(int)
        for record in raw_records:
            totals[record["journal_search_id"]] += 1
        search_log = [
            {
                "venue_id": venue_id,
                "journal": journal,
                "issn": issn,
                "search_date": SEARCH_DATE,
                "publication_start": PUBLICATION_START,
                "publication_end": PUBLICATION_END,
                "records_enumerated": str(totals[venue_id]),
                "crossref_total_results": str(totals[venue_id]),
            }
            for venue_id, journal, issn in JOURNALS
        ]
    else:
        raw_records = []
        search_log = []
        for venue_id, journal, issn in JOURNALS:
            records, total = fetch_journal(venue_id, journal, issn)
            raw_records.extend(records)
            search_log.append(
                {
                    "venue_id": venue_id,
                    "journal": journal,
                    "issn": issn,
                    "search_date": SEARCH_DATE,
                    "publication_start": PUBLICATION_START,
                    "publication_end": PUBLICATION_END,
                    "records_enumerated": str(len(records)),
                    "crossref_total_results": str(total),
                }
            )

    included = included_documents()
    included_titles = {normalise_title(row.get("title", "")) for row in included}
    included_dois = {
        normalise_doi(row.get("doi") or row.get("url") or "")
        for row in included
        if row.get("doi") or "doi.org/" in row.get("url", "")
    }
    prior = prior_openalex_records()
    prior_titles = {normalise_title(row.get("title", "")) for row in prior}
    prior_dois = {
        normalise_doi(row.get("doi") or row.get("url") or "")
        for row in prior
        if row.get("doi") or "doi.org/" in row.get("url", "")
    }

    candidates: dict[str, dict[str, str]] = {}
    within_search_duplicates: defaultdict[str, set[str]] = defaultdict(set)
    for raw in raw_records:
        title = first_text(raw.get("title"))
        abstract = clean_markup(raw.get("abstract") or "")
        is_candidate, reason = candidate_reason(title, abstract)
        if not is_candidate:
            continue
        doi = normalise_doi(str(raw.get("DOI") or ""))
        key = f"doi:{doi}" if doi else f"title:{normalise_title(title)}"
        within_search_duplicates[key].add(raw["journal_search_id"])
        row = {
            "title": title,
            "publication_year": publication_year(raw),
            "journal": raw["journal_search_name"],
            "issn": raw["journal_search_issn"],
            "doi": doi,
            "url": str(raw.get("URL") or (f"https://doi.org/{doi}" if doi else "")),
            "abstract": abstract,
            "automated_screen": "candidate",
            "automated_reason": reason,
            "dedupe_status": dedupe_status(
                title,
                doi,
                included_titles,
                included_dois,
                prior_titles,
                prior_dois,
            ),
        }
        candidates.setdefault(key, row)

    rows = sorted(
        candidates.values(),
        key=lambda row: (row["dedupe_status"] != "unique_for_screening", row["journal"], row["title"]),
    )
    for number, row in enumerate(rows, start=1):
        row["journal_record_id"] = f"JR-{number:03d}"
        key = f"doi:{row['doi']}" if row["doi"] else f"title:{normalise_title(row['title'])}"
        row["within_search_venues"] = ";".join(sorted(within_search_duplicates[key]))

    with snapshot.open("wb") as raw_handle:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=raw_handle,
            mtime=0,
        ) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8") as handle:
                for record in raw_records:
                    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    write_csv(
        HERE / "journal-search-log.csv",
        search_log,
        [
            "venue_id",
            "journal",
            "issn",
            "search_date",
            "publication_start",
            "publication_end",
            "records_enumerated",
            "crossref_total_results",
        ],
    )
    write_csv(
        HERE / "journal-screening-register.csv",
        rows,
        [
            "journal_record_id",
            "title",
            "publication_year",
            "journal",
            "issn",
            "doi",
            "url",
            "within_search_venues",
            "automated_screen",
            "automated_reason",
            "dedupe_status",
            "abstract",
        ],
    )
    with (HERE / "journal-attributed-existing-corpus.csv").open(
        encoding="utf-8",
        newline="",
    ) as handle:
        reattributed_count = sum(1 for _ in csv.DictReader(handle))

    summary = {
        "search_date": SEARCH_DATE,
        "journals_enumerated": len(JOURNALS),
        "records_enumerated": len(raw_records),
        "candidate_reports_after_marker_screen": len(rows),
        "duplicates_against_existing_corpus": sum(
            row["dedupe_status"].startswith("duplicate_included") for row in rows
        ),
        "prior_openalex_records_reassessed": sum(
            row["dedupe_status"] == "prior_openalex_record_reassessed"
            for row in rows
        ),
        "new_records_for_screening": sum(
            row["dedupe_status"] == "unique_for_screening"
            for row in rows
        ),
        "records_screened_or_reassessed": sum(
            not row["dedupe_status"].startswith("duplicate_included")
            for row in rows
        ),
        "initial_agentic_records_reassigned_to_journals": reattributed_count,
    }
    (HERE / "journal-search-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

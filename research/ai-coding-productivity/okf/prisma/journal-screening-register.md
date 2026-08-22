---
type: Research Register
title: Journal-stream screening and decision register
description: All topical journal-search candidates, deduplication status against the existing corpus, and title/abstract decisions.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/journal-screening-register.csv
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: journal-search-log
    resource: journal-search-log.md
    title: Direct journal (Crossref) search log
  - id: journal-records
    resource: journal-records.md
    title: Raw Crossref record snapshot
  - id: script
    resource: ../../prisma/screen_journals.py
    title: screen_journals.py
---

# Schema

659 rows.

| Column | Type | Description |
|---|---|---|
| `journal_record_id` | string | `JR-001` and up. Primary key. |
| `title` | string | |
| `publication_year` | year | |
| `journal` | string | |
| `issn` | string | |
| `doi` | string | |
| `url` | string | |
| `within_search_venues` | string | Matching [journal-search-log](journal-search-log.md).`venue_id`.[^journal-search-log] |
| `automated_screen` | string | |
| `automated_reason` | string | |
| `dedupe_status` | string | |
| `abstract` | string | |
| `human_decision` | string | |
| `title_abstract_reason` | string | |
| `full_text_decision` | string | |
| `full_text_reason` | string | |
| `study_id` | string | Joins to [evidence-weight-register](/evidence-weight-register.md).`study_id` for included studies. |
| `evidence_weight` | string | `high`, `moderate` or `low`. |

# Provenance

Built from [journal-search-log](journal-search-log.md)[^journal-search-log]
and [journal-records](journal-records.md),[^journal-records] with
decisions applied by
[`screen_journals.py`](../../prisma/screen_journals.py).[^script] The 30
records advancing past this stage are recorded in
[journal-full-text-candidates](journal-full-text-candidates.md) and
[journal-report-assessments](journal-report-assessments.md).

[^journal-search-log]: Direct journal (Crossref) search log
[^journal-records]: Raw Crossref record snapshot
[^script]: screen_journals.py

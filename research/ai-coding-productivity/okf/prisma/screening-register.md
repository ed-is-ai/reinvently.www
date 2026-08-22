---
type: Research Register
title: Master OpenAlex-stream screening and decision register
description: Deduplicated record register spanning identification through report-level eligibility for the agentic-web and OpenAlex streams.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/screening-register.csv
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: search-log
    resource: search-log.md
    title: OpenAlex query log
  - id: openalex-records
    resource: openalex-records.md
    title: Raw OpenAlex record snapshot
  - id: screen-script
    resource: ../../prisma/screen_title_abstract.py
    title: screen_title_abstract.py
---

# Schema

948 rows, spanning identification through title/abstract screening and,
for a subset, report-level eligibility.

| Column | Type | Description |
|---|---|---|
| `record_id` | string | `R-0001` and up. Primary key. |
| `title` | string | |
| `publication_year` | year | |
| `publication_type` | string | |
| `doi` | string | |
| `url` | string | |
| `openalex_id` | string | Links to [openalex-records](openalex-records.md) where present.[^openalex-records] |
| `record_sources` | string | Retrieval route, e.g. `existing_corpus`, `openalex`. |
| `query_ids` | string | Semicolon-separated [search-log](search-log.md).`query_id` value(s) that surfaced this record.[^search-log] Not a single-value key. |
| `existing_category` | string | |
| `study_id` | string | Joins to [evidence-weight-register](/evidence-weight-register.md).`study_id` for included studies. |
| `automated_screen` | string | |
| `automated_reason` | string | |
| `human_decision` | string | |
| `exclusion_reason` | string | |
| `abstract` | string | |
| `full_text_decision` | string | |
| `full_text_reason` | string | |
| `estimate_id` | string | |
| `confidence` | string | `low` or `moderate`. |

# Provenance

Built from [search-log](search-log.md)[^search-log] and
[openalex-records](openalex-records.md),[^openalex-records] with
title/abstract decisions applied by
[`screen_title_abstract.py`](../../prisma/screen_title_abstract.py).[^screen-script]
One AI-assisted reviewer performed the screening, without independent
duplicate review — the article and
[`../../prisma/README.md`](../../prisma/README.md) state this
limitation explicitly. The 69 records advancing past this stage are
recorded in [full-text-candidates](full-text-candidates.md) and
[report-assessments](report-assessments.md).

[^search-log]: OpenAlex query log
[^openalex-records]: Raw OpenAlex record snapshot
[^screen-script]: screen_title_abstract.py

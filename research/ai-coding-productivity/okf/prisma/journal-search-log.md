---
type: Research Register
title: Direct journal (Crossref) search log
description: Per-venue Crossref enumeration parameters and result counts for the 15 named software-engineering journals, searched by ISSN.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/journal-search-log.csv
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: script
    resource: ../../prisma/search_journals.py
    title: search_journals.py
---

# Schema

| Column | Type | Description |
|---|---|---|
| `venue_id` | string | `J01` to `J15`. Primary key. |
| `journal` | string | |
| `issn` | string | |
| `search_date` | date | |
| `publication_start` | date | |
| `publication_end` | date | |
| `records_enumerated` | integer | |
| `crossref_total_results` | integer | |

# Provenance

Produced by [`search_journals.py`](../../prisma/search_journals.py).[^script]
`venue_id` is referenced by [journal-screening-register](journal-screening-register.md)'s
`within_search_venues` column. Rerunning with `--reuse-snapshot` rebuilds
the candidate register from the committed snapshot without re-querying
Crossref.

[^script]: search_journals.py

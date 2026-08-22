---
type: Research Register
title: OpenAlex query log
description: Exact OpenAlex query strings, dates, fields and result counts for the 14 archived title/abstract queries.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/search-log.csv
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: script
    resource: ../../prisma/search_openalex.py
    title: search_openalex.py
---

# Schema

| Column | Type | Description |
|---|---|---|
| `query_id` | string | `Q01` to `Q14`. Primary key. |
| `source` | string | `OpenAlex`. |
| `search_date` | date | |
| `publication_start` | date | |
| `publication_end` | date | |
| `field` | string | e.g. `title and abstract`. |
| `query` | string | Exact query string. |
| `records_returned_before_cross_query_deduplication` | integer | |

# Provenance

Produced by [`search_openalex.py`](../../prisma/search_openalex.py).[^script]
Rerunning it can change identification counts, since OpenAlex is a live
index; the committed log preserves the snapshot used in article version
1.23. `query_id` is referenced (as a semicolon-delimited list, not a
single-value key) by the `query_ids` column of the [screening
register](screening-register.md).

[^script]: search_openalex.py

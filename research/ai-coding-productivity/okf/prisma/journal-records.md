---
type: Raw Record Snapshot
title: Raw Crossref record snapshot
description: Compressed newline-delimited raw Crossref records for the 31 July 2026 direct journal search.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/journal-records.jsonl.gz
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
---

# Schema

Gzip-compressed, newline-delimited JSON; one Crossref work record per
line, tagged with the originating `journal_search_id`,
`journal_search_name` and `journal_search_issn` (matching
[journal-search-log](journal-search-log.md)'s `venue_id`). No fixed
column schema — this is a raw external-API dump, not a curated table.

# Provenance

Underlies [journal-screening-register](journal-screening-register.md).

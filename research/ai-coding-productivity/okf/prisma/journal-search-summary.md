---
type: Aggregate Summary
title: Aggregate journal-stream counts
description: Aggregate PRISMA counts for the direct journal (Crossref) search stream only.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/journal-search-summary.json
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: journal-screening-register
    resource: journal-screening-register.md
    title: Journal-stream screening and decision register
---

# Schema

A flat JSON object: `search_date`, `journals_enumerated` (15),
`records_enumerated` (10,995), `candidate_reports_after_marker_screen`
(658), `duplicates_against_existing_corpus` (10),
`new_records_for_screening` (643), `reports_assessed` (30),
`included_new_empirical_studies` (17), `included_new_secondary_syntheses`
(2), `included_new_contextual_documents` (8), `replacement_reports` (1),
`full_text_exclusions` (2).

# Provenance

Aggregated from [journal-screening-register](journal-screening-register.md).[^journal-screening-register]
Nested verbatim inside [search-summary](search-summary.md)'s
`journal_search_update` object.

[^journal-screening-register]: Journal-stream screening and decision register

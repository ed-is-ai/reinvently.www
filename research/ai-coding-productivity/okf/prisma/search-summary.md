---
type: Aggregate Summary
title: Aggregate OpenAlex-stream and corpus-wide counts
description: Current aggregate PRISMA counts (identification through inclusion) for the agentic-web/OpenAlex stream and the combined corpus, as cited in the article.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/search-summary.json
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: screening-register
    resource: screening-register.md
    title: Master OpenAlex-stream screening and decision register
  - id: journal-search-summary
    resource: journal-search-summary.md
    title: Aggregate journal-stream counts
---

# Schema

A flat JSON object of named counts, including `existing_corpus_records`,
`openalex_records_before_cross_source_deduplication`,
`master_records_after_cross_source_deduplication`,
`title_abstract_records_screened`, `reports_assessed_for_eligibility`,
`updated_source_documents` (181), `updated_empirical_studies` (116),
`updated_productivity_effect_estimates` (46), and a nested
`journal_search_update` object mirroring
[journal-search-summary](journal-search-summary.md).[^journal-search-summary]

# Provenance

Aggregated from [screening-register](screening-register.md)[^screening-register]
and the journal-stream equivalent; these are the exact figures the
article's methodology section and PRISMA diagram cite.

[^screening-register]: Master OpenAlex-stream screening and decision register
[^journal-search-summary]: Aggregate journal-stream counts

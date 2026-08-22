---
type: Research Register
title: OpenAlex-stream reports advanced to full-text assessment
description: The 69 reports advanced from the screening register to eligibility assessment.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/full-text-candidates.csv
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: screening-register
    resource: screening-register.md
    title: Master OpenAlex-stream screening and decision register
---

# Schema

Same columns as [screening-register](screening-register.md),[^screening-register]
filtered to the 69 records that reached full-text eligibility assessment
(`record_id`, `title`, `publication_year`, `publication_type`, `doi`,
`url`, `openalex_id`, `record_sources`, `query_ids`, `existing_category`,
`study_id`, `automated_screen`, `automated_reason`, `human_decision`,
`exclusion_reason`, `abstract`, `full_text_decision`, `full_text_reason`,
`estimate_id`, `confidence`).

# Provenance

Byte-identical to [report-assessments](report-assessments.md): every
candidate received its decision in place, so no rows were dropped
between the "advanced to assessment" stage and the "final decision"
stage. Kept as two named concepts because they represent two distinct
pipeline stages per [`../../prisma/README.md`](../../prisma/README.md),
even though nothing currently distinguishes their contents.

[^screening-register]: Master OpenAlex-stream screening and decision register

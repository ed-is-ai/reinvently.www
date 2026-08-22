---
type: Research Register
title: Locked pre-update corpus
description: The 115-document corpus retained from the article's initial version, with its original publication-source grouping.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/existing-corpus.csv
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: readme
    resource: ../../prisma/README.md
    title: PRISMA reconstruction README
---

# Schema

| Column | Type | Description |
|---|---|---|
| `existing_category` | string | `empirical`, `secondary_synthesis`, or `contextual`. |
| `study_id` | string | Joins to [evidence-weight-register](/evidence-weight-register.md).`study_id`. |
| `title` | string | |
| `url` | string | |
| `source_group` | string | `arXiv`, `ACM`, or `Other web/publisher`. |

# Provenance

The baseline the [OpenAlex](screening-register.md) and [journal](journal-screening-register.md)
search streams were deduplicated against.[^readme] 59 empirical studies, 2
secondary syntheses and 54 contextual documents were retained from this
corpus into the updated review.

[^readme]: PRISMA reconstruction README

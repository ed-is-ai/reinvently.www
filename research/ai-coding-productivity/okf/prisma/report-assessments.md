---
type: Research Register
title: OpenAlex-stream report-level decision and exclusion register
description: Final report-level eligibility decisions, exclusion reasons and stable study/effect ID assignment for the 69 assessed reports.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/report-assessments.csv
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: full-text-candidates
    resource: full-text-candidates.md
    title: OpenAlex-stream reports advanced to full-text assessment
  - id: assess-script
    resource: ../../prisma/assess_reports.py
    title: assess_reports.py
---

# Schema

Same columns as [full-text-candidates](full-text-candidates.md).[^full-text-candidates]

# Provenance

Final decisions applied to [full-text-candidates](full-text-candidates.md)[^full-text-candidates]
by [`assess_reports.py`](../../prisma/assess_reports.py),[^assess-script]
which also assigns the stable `study_id`/`estimate_id` identifiers used
across every other register in this bundle. Byte-identical to
full-text-candidates.md — see that concept's provenance note.

[^full-text-candidates]: OpenAlex-stream reports advanced to full-text assessment
[^assess-script]: assess_reports.py

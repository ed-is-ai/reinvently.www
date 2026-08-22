---
type: Aggregate Summary
title: Study-level risk-of-bias totals
description: Aggregate counts of overall risk-of-bias judgements by routed instrument, as cited in the article's risk-of-bias section.
resource: https://reinvently.co.uk/research/ai-coding-productivity/risk-of-bias/risk-of-bias-summary.json
tags: [ai-coding-productivity, risk-of-bias, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: register
    resource: risk-of-bias-register.md
    title: Study-level risk-of-bias domain register
---

# Schema

A flat JSON object: `assessment_date`, `empirical_studies` (116),
`study_level_assessments` (116), `productivity_effect_estimates` (46),
`adjacent_outcome_studies` (72), `independent_duplicate_appraisal`
(`false`), and `study_level_counts` — a nested object keyed by
instrument (`RoB 2`, `ROBINS-I`, `JBI quasi`, `JBI analytical`, `JBI
case`), each mapping overall-judgement label to study count.

# Provenance

Aggregated from [risk-of-bias-register](risk-of-bias-register.md).[^register]
`independent_duplicate_appraisal: false` is the machine-readable form of
the reviewer limitation documented in
[`../../risk-of-bias/README.md`](../../risk-of-bias/README.md).

[^register]: Study-level risk-of-bias domain register

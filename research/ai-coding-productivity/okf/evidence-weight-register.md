---
type: Research Register
title: Study-level evidence-weight register
description: One evidence-weight grade (high/moderate/low) per empirical study, combining risk of bias with outcome directness, precision and relevance.
resource: https://reinvently.co.uk/research/ai-coding-productivity/evidence-weight-register.csv
tags: [ai-coding-productivity, evidence-weight, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: rob-register
    resource: /risk-of-bias/risk-of-bias-register.md
    title: Study-level risk-of-bias domain register
  - id: rob-script
    resource: ../generate_evidence_weight_register.py
    title: generate_evidence_weight_register.py
---

# Schema

One row per empirical study (116 rows: 44 productivity/delivery, 72
adjacent-outcome).

| Column | Type | Description |
|---|---|---|
| `study_id` | string | Stable identifier, `ST-01` to `ST-116`. Primary key. |
| `title` | string | |
| `effect_ids` | string | Linked productivity effect identifier(s), e.g. `E-01`; `ST-29` and `ST-31` each carry two. |
| `evidence_stream` | string | `productivity/delivery` or `adjacent outcome`. |
| `evidence_weight` | string | `high`, `moderate` or `low`. |
| `overall_risk_of_bias` | string | Judgement in the routed instrument's own vocabulary (Low, Some concerns, Moderate, Serious, High). |
| `appraisal_instrument` | string | One of `RoB 2`, `ROBINS-I V2`, or a named JBI(-derived) checklist. |
| `weight_basis` | string | |
| `main_limitation` | string | |
| `grade_source` | string | File this grade was consolidated from. |
| `assessment_date` | date | |

# Provenance

Consolidates the study-level grade already recorded in each study's
original appraisal register, principally the [risk-of-bias
register](/risk-of-bias/risk-of-bias-register.md),[^rob-register] via
[`generate_evidence_weight_register.py`](../generate_evidence_weight_register.py).[^rob-script]
Risk of bias and evidence weight are deliberately kept as separate
grades: risk of bias judges internal validity only, while evidence
weight additionally weighs directness, precision, replication and
relevance to the review question.

This is the canonical study-id → evidence-weight join point: the
[operating-model audit](operating-model-audit.md), the [PRISMA
registers](/prisma/) and the [risk-of-bias
register](/risk-of-bias/risk-of-bias-register.md) all key off `study_id`
defined here.

[^rob-register]: Study-level risk-of-bias domain register
[^rob-script]: generate_evidence_weight_register.py

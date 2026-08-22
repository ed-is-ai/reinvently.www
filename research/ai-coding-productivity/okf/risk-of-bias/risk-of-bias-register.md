---
type: Research Register
title: Study-level risk-of-bias domain register
description: One domain-judgement row per empirical study, routed to RoB 2, ROBINS-I V2, or a JBI(-derived) checklist per study design.
resource: https://reinvently.co.uk/research/ai-coding-productivity/risk-of-bias/risk-of-bias-register.csv
tags: [ai-coding-productivity, risk-of-bias, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: existing-corpus
    resource: /prisma/existing-corpus.md
    title: Locked pre-update corpus
  - id: script
    resource: ../../risk-of-bias/assess_risk_of_bias.py
    title: assess_risk_of_bias.py
---

# Schema

117 rows (`ST-01` to `ST-116`; two studies each contribute a paired-effect row).

| Column | Type | Description |
|---|---|---|
| `assessment_id` | string | `RB-ST-01` and up. Primary key. |
| `study_id` | string | Joins to [evidence-weight-register](/evidence-weight-register.md).`study_id`. |
| `effect_ids` | string | |
| `evidence_stream` | string | `productivity/delivery` or `adjacent outcome`. |
| `title` | string | |
| `url` | string | |
| `target_results` | string | The specific reported result this assessment targets. |
| `instrument` | string | One of `RoB 2`, `ROBINS-I V2`, `JBI quasi-experimental checklist with prespecified overall-risk rule`, `JBI analytical cross-sectional/cohort checklist with prespecified overall-risk rule`, `JBI-derived software benchmark/case checklist with prespecified overall-risk rule`. |
| `instrument_version` | string | |
| `profile` | string | Study-design profile used for routing to an instrument. |
| `domain_1` … `domain_10` | string | Per-domain judgements; count and meaning vary by routed instrument. |
| `overall_risk_of_bias` | string | Qualitative overall judgement in the routed instrument's own vocabulary. |
| `study_specific_note` | string | |
| `decision_rationale` | string | |
| `appraisal_basis` | string | |
| `assessor` | string | |
| `assessment_date` | date | |

# Provenance

Routes every study from [existing-corpus](/prisma/existing-corpus.md)[^existing-corpus]
and the journal stream to a design-appropriate instrument via
[`assess_risk_of_bias.py`](../../risk-of-bias/assess_risk_of_bias.py).[^script]
One AI-assisted reviewer completed the appraisal without independent
duplicate review — see
[`../../risk-of-bias/README.md`](../../risk-of-bias/README.md) for the
full reviewer-limitation statement. No study was judged low risk across
every applicable domain. Feeds
[evidence-weight-register](/evidence-weight-register.md), which keeps
risk of bias and evidence weight as deliberately separate grades.

[^existing-corpus]: Locked pre-update corpus
[^script]: assess_risk_of_bias.py

---
type: Research Register
title: Effect-level operating-model and plotting audit
description: One row per productivity/delivery effect estimate, classifying the automation operating model and whether the effect is plotted as a ratio in the study-results graph.
resource: https://reinvently.co.uk/research/ai-coding-productivity/operating-model-audit.csv
tags: [ai-coding-productivity, operating-model, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
sources:
  - id: ewr
    resource: /evidence-weight-register.md
    title: Study-level evidence-weight register
---

# Schema

One row per productivity/delivery effect (46 rows, `E-01` to `E-46`).

| Column | Type | Description |
|---|---|---|
| `effect_id` | string | `E-01` to `E-46`. Primary key. |
| `study_id` | string | Joins to [evidence-weight-register](evidence-weight-register.md).`study_id`.[^ewr] |
| `evidence_weight` | string | `high`, `medium` or `low`. |
| `operating_model` | string | `assisted`, `spec_driven`, `agent_native`, `cross_level_or_undisclosed`, or `cross_level_stratified`. |
| `plot_status` | string | `ratio` or `non_ratio` — whether the effect is plotted as a ratio in the article's study-results graph. |
| `classification_basis` | string | Rationale for the operating-model classification. |

Note: this file spells the middle evidence-weight grade `medium`, while
[evidence-weight-register.md](evidence-weight-register.md) spells the
same grade `moderate`.[^ewr] A terminology inconsistency in the
underlying data, not a modelling choice — worth normalising if this
register is regenerated.

[^ewr]: Study-level evidence-weight register

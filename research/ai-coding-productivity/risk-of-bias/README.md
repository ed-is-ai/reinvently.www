# Formal risk-of-bias assessment

Status: **complete for the 116 empirical studies included in article version
1.23**.

## Scope

The register contains 116 study-level assessments:

- 44 assessments cover productivity and delivery studies and retain links to
  all 46 estimates (`E-01` to `E-46`);
- 72 assessments cover the primary adjacent outcome family cited for each
  remaining empirical study.

`ST-29` and `ST-31` each contribute two productivity estimates. Their paired
effect identifiers are retained in a single study row because the applicable
design, risk domains and overall judgement are the same.

Risk of bias is kept separate from the article's evidence-weight grade. Risk
of bias concerns whether a study's result is internally valid. Evidence weight
also considers directness, precision, replication and usefulness for the
review question. A large observational delivery study can therefore have
serious risk of bias but remain useful, moderate-weight evidence for scenario
planning.

## Design routing

- Randomised and randomised-crossover trials: **Cochrane RoB 2**, current
  version dated 22 August 2019.
- Non-randomised comparative intervention effects: **ROBINS-I V2**, draft
  version dated 20 November 2025.
- Non-randomised experiments: **JBI quasi-experimental checklist (2024)** with
  a prespecified qualitative overall-risk rule.
- Repository, telemetry and other analytical observational studies: **JBI
  analytical cross-sectional/cohort tools (2025–2026)** with a prespecified
  qualitative overall-risk rule.
- Descriptive organisational cases and software benchmarks: a **JBI-derived
  software benchmark/case checklist**. This adaptation makes the reference
  standard, completeness of runs, failure reporting and generalisability
  explicit. It is not presented as a validated Cochrane or JBI instrument.

The JBI-derived overall rule is:

- **Low:** every material criterion is met and no plausible bias is likely to
  change the result.
- **Some concerns:** at least one material criterion is unclear, but none is
  clearly likely to reverse the result.
- **High:** at least one material criterion is not met and could materially
  change attribution or magnitude.

No numerical checklist score is calculated. Such scores can conceal a critical
failure by averaging it with less important items.

## Interpretation

The appraisal is conservative. Open-label AI interventions commonly raise
concerns about deviations from intended use and selective reporting.
Observational adoption studies are vulnerable to confounding because early
adopters, teams and repositories differ from controls. Organisational cases
and benchmarks frequently lack concurrent comparators or complete failure
reporting.

The study-level results are:

| Design route | Studies | Overall judgements |
| --- | ---: | --- |
| RoB 2 randomised trials | 10 | 9 some concerns; 1 high |
| ROBINS-I non-randomised intervention studies | 18 | 2 moderate; 16 serious |
| JBI quasi-experiments | 18 | 13 some concerns; 5 high |
| JBI analytical observational studies | 39 | 28 some concerns; 11 high |
| JBI-derived cases and benchmarks | 31 | 15 some concerns; 16 high |

No study was judged low risk across every applicable domain.

The appraisal does **not** imply that every result is unreliable. It limits
causal language and determines how heavily each result can support a
conclusion. In particular, the 1.1–1.3× release range remains a useful
observational planning range, but it is not a causal forecast.

A sensitivity restriction to results rated no worse than **Some concerns**
(RoB 2/JBI-derived routes) or **Moderate** (ROBINS-I) preserves the direction
of the bounded assistant evidence. It removes the empirical basis for a
precise end-to-end release multiplier and for the 4.5× agent-native case.

## Reviewer and evidence limitations

One AI-assisted reviewer completed the assessment. It was not independently
duplicated. The linked report and available methods/results information were
used; where reporting was incomplete, the relevant domain was rated
conservatively rather than assumed to be low risk. Before journal submission,
the register should be checked independently by a second reviewer against each
full report, with disagreements recorded and resolved.

## Files

- `assess_risk_of_bias.py` — routing rules, domain judgements, rationales and
  validation checks.
- `risk-of-bias-register.csv` — one domain judgement row for every empirical
  study, retaining all linked productivity effect identifiers.
- `risk-of-bias-summary.json` — study-level totals used in the article.
- `../evidence-weight-register.csv` — one evidence-weight grade for every
  empirical study, kept separate from the risk-of-bias judgement.
- `../generate_evidence_weight_register.py` — consolidates the existing
  study-level grades from their original appraisal registers.

## Reproduction

Run:

```sh
python3 research/ai-coding-productivity/risk-of-bias/assess_risk_of_bias.py
python3 research/ai-coding-productivity/generate_evidence_weight_register.py
```

The risk-of-bias script reads the article's stable study and effect registers,
verifies complete and non-overlapping routing for `ST-01` to `ST-116`, and
rewrites its CSV and JSON outputs. The evidence-weight script consolidates the
existing grades, verifies one grade per study and checks the published totals.

## Risk of bias is not evidence weight

These files record risk of bias only — whether a study's design could
systematically overstate or understate its own result. They do not record the
**evidence weight** grade reported in the article, which additionally weighs
directness, precision and relevance to the review question, and so cannot be
derived from the judgements here.

The canonical `../evidence-weight-register.csv` publishes one grade for each
of the **116 empirical studies**: 12 high, 77 moderate and 27 low. It contains
44 productivity/delivery studies and 72 adjacent-outcome studies. Studies
with more than one productivity effect are counted once at study level. The
effect-level operating-model and plotting decisions remain in
`../operating-model-audit.csv`.

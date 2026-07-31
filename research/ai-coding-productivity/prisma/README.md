# PRISMA reconstruction for the AI coding productivity review

Status: **updated search and report-level eligibility assessment complete**.

The repository did not contain the original raw search export, duplicate log or
exclusion log. These files therefore document a reproducible update rather than
inventing retrospective counts.

## Scope

- Empirical search window: 1 January 2024 to 28 July 2026.
- Search run: 29 July 2026.
- Database: OpenAlex title and abstract search.
- Other-method stream: 115 documents assembled through agentic Google web
  retrieval, evidence extraction and citation chasing.
- Publication-source breakdown of that 115-document stream: 40 arXiv-hosted
  reports, 14 ACM publications identified through the `10.1145` DOI prefix,
  and 61 other web, publisher or repository sources. arXiv and ACM are shown
  separately because each supplied at least 10 documents; they are source
  categories within the agentic retrieval stream, not separate database
  searches.
- The small number of 2022–2023 mechanism sources in the article are contextual
  citation-chasing sources, not part of the empirical database search.

## Completed flow

- 115 documents were retained from the initial article: 59 empirical studies,
  2 secondary syntheses and 54 contextual documents.
- Fourteen archived OpenAlex queries returned 1,463 records and 1,188 remained
  after cross-query deduplication by OpenAlex identifier.
- DOI and normalised-title deduplication, followed by merging with the existing
  corpus, produced 947 records.
- The existing 59 empirical reports and 56 supporting reports were retained in
  their existing streams.
- Of 832 newly identified database records, 763 were excluded at title or
  abstract screening.
- Sixty-nine reports were assessed for eligibility: 39 new source documents
  were included, one report replaced an existing contextual version, 27 were
  ineligible and two were duplicate reports.
- The updated corpus contains 154 source documents: 99 empirical studies,
  2 secondary syntheses and 53 contextual documents. The productivity stream
  contains 44 studies and 46 effect estimates; 55 studies report adjacent
  outcomes.

The title/abstract and report-level passes were performed by one AI-assisted
reviewer. Decisions and one exclusion reason per excluded report are recorded
in the registers. This is not an independent dual-review process and the
article states that limitation. Full reports were inspected where publicly
accessible; otherwise the eligibility decision used the detailed publisher or
repository record.

## Files

- `search_openalex.py` — reproducible search, corpus extraction and deduplication.
- `search-log.csv` — exact query strings, dates, fields and result counts.
- `openalex-records.jsonl` — raw database snapshot.
- `existing-corpus.csv` — the locked 115-document corpus, including its
  publication-source grouping.
- `screening-register.csv` — master deduplicated record and decision register.
- `screen_title_abstract.py` — archived AI-assisted title/abstract decisions.
- `full-text-candidates.csv` — the 69 reports advanced to eligibility assessment.
- `assess_reports.py` — archived report-level eligibility decisions and stable
  study/effect ID assignment.
- `report-assessments.csv` — report-level decision and exclusion register.
- `search-summary.json` — current aggregate counts.

## Reproduction

Run `search_openalex.py`, then `screen_title_abstract.py`, then
`assess_reports.py`. OpenAlex is a live index, so rerunning the search can
change the identification counts. The committed JSONL and CSV files preserve
the 29 July 2026 snapshot used in article version 1.18.

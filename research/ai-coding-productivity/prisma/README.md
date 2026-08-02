# PRISMA reconstruction for the AI coding productivity review

Status: **updated search and report-level eligibility assessment complete**.

The repository did not contain the original raw search export, duplicate log or
exclusion log. These files therefore document a reproducible update rather than
inventing retrospective counts.

## Scope

- Empirical search window: 1 January 2022 to 31 July 2026.
- Search runs: OpenAlex on 29 July 2026; direct journal search on 31 July 2026.
- Databases: OpenAlex title and abstract search; Crossref enumeration of 15
  software-engineering journals by ISSN.
- Initial working corpus: 115 documents assembled through agentic Google web
  retrieval, evidence extraction and citation chasing.
- Source attribution within that working corpus: 108 agentic-web documents and
  7 publications reassigned to the selected direct-journal stream.
- Publication-source breakdown of the 108-document agentic stream: 40
  arXiv-hosted reports, 12 ACM sources outside the selected journal set and 56
  other web, publisher or repository sources.
- The small number of 2022–2023 mechanism sources in the article are contextual
  citation-chasing sources, not part of the empirical database search.

## Completed flow

- 115 documents were retained from the initial article: 59 empirical studies,
  2 secondary syntheses and 54 contextual documents. Their retrieval
  attribution is 108 agentic-web documents and 7 direct-journal publications.
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
- The direct journal search enumerated 10,995 records. A broad topical marker
  screen retained 658 candidates, 10 of which duplicated the included corpus.
  Seven of those ten matches came from the initial working corpus and were
  reassigned from agentic-web retrieval to their named journal sources; the
  other three retained their OpenAlex attribution. Of the 648 records screened,
  643 were new and 5 overlapped the earlier OpenAlex screen. Those five were
  reassessed from richer publisher records rather than counted as new
  identifications. In total, 618 were excluded at title/abstract stage and 30
  reports were assessed.
- The journal assessment added 17 primary adjacent-outcome studies, 2
  secondary syntheses and 8 contextual documents. One existing synthesis was
  replaced by its peer-reviewed journal version and 2 reports were excluded
  at full text.
- The updated corpus contains 181 source documents: 116 empirical studies,
  4 secondary syntheses and 61 contextual documents. The productivity stream
  contains 44 studies and 46 effect estimates; 72 studies report adjacent
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
- `journal-attributed-existing-corpus.csv` — the seven working-corpus
  publications reassigned from agentic web retrieval to named journal sources.
- `screening-register.csv` — master deduplicated record and decision register.
- `screen_title_abstract.py` — archived AI-assisted title/abstract decisions.
- `full-text-candidates.csv` — the 69 reports advanced to eligibility assessment.
- `assess_reports.py` — archived report-level eligibility decisions and stable
  study/effect ID assignment.
- `report-assessments.csv` — report-level decision and exclusion register.
- `search-summary.json` — current aggregate counts.
- `search_journals.py` — ISSN-based Crossref enumeration, topical marker
  screening and deduplication against the included corpus.
- `journal-search-log.csv` and `journal-records.jsonl.gz` — journal query log
  and compressed 31 July 2026 snapshot of the Crossref fields used for
  screening.
- `journal-screening-register.csv` — all topical journal candidates,
  deduplication status and title/abstract decisions.
- `screen_journals.py` — archived journal title/abstract and full-text
  decisions.
- `journal-full-text-candidates.csv` and `journal-report-assessments.csv` —
  journal reports advanced to assessment and their final decisions.
- `journal-search-summary.json` — aggregate journal-stream counts.

## Reproduction

Run `search_openalex.py`, `screen_title_abstract.py` and `assess_reports.py`
for the OpenAlex stream. Run `search_journals.py` and `screen_journals.py` for
the journal stream. Both indexes are live, so rerunning either search can
change identification counts. The committed JSONL and CSV files preserve the
snapshots used in article version 1.22. Use
`search_journals.py --reuse-snapshot` to rebuild the journal candidate
register without querying Crossref again.

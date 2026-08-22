# PRISMA Search and Screening

Reconstructed PRISMA 2020 flow for the review's two retrieval streams:
115 documents assembled by agentic web retrieval and citation chasing,
tested and expanded by 14 archived OpenAlex queries, then supplemented
by a direct Crossref search of 15 named software-engineering journals.
See [`../../prisma/README.md`](../../prisma/README.md) for the full
narrative and reproduction instructions.

# Agentic-web / OpenAlex stream

* [Existing corpus](existing-corpus.md) - the 115-document corpus retained from the article's initial version
* [Search log](search-log.md) - the 14 archived OpenAlex query strings, dates and result counts
* [OpenAlex records](openalex-records.md) - raw OpenAlex API snapshot
* [Screening register](screening-register.md) - master deduplicated record and decision register (948 rows)
* [Full-text candidates](full-text-candidates.md) - the 69 reports advanced to eligibility assessment
* [Report assessments](report-assessments.md) - final report-level eligibility decisions
* [Search summary](search-summary.md) - aggregate stream-wide and corpus-wide counts

# Direct journal (Crossref) stream

* [Journal search log](journal-search-log.md) - per-venue Crossref enumeration parameters and counts
* [Journal records](journal-records.md) - compressed raw Crossref snapshot
* [Journal screening register](journal-screening-register.md) - all topical journal candidates and title/abstract decisions (659 rows)
* [Journal full-text candidates](journal-full-text-candidates.md) - the 30 journal reports advanced to assessment
* [Journal report assessments](journal-report-assessments.md) - final journal-stream eligibility decisions
* [Journal search summary](journal-search-summary.md) - aggregate journal-stream counts

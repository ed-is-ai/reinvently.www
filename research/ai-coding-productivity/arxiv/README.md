# arXiv preprint package: "How Much Does AI Improve Software Development Productivity?"

This directory contains a submission-ready LaTeX package adapting the Reinvently systematic
review published at
[reinvently.co.uk/blog/ai-coding-productivity-evidence](https://reinvently.co.uk/blog/ai-coding-productivity-evidence/)
(version 1.28.2, published 28 July 2026, last updated 22 August 2026) into an arXiv preprint.

This package was prepared by an AI assistant (Claude) from the published article. **Ed still
needs to review the manuscript himself before submitting it** — see "What Ed still needs to do"
below.

## Contents

- `main.tex` — the complete manuscript (plain `article` class, 11pt). Structure: title/author,
  abstract, introduction, methods (PRISMA screening, risk-of-bias appraisal, evidence synthesis,
  detailed methods), results (three operating models, downstream-conversion/delivery results,
  moderators, quality/security/review effects), the 46-row productivity effect register,
  discussion (measurement guidance, limitations, conclusion), and references.
  - Three figures are reproduced as native TikZ/pgfplots diagrams (no external image files):
    the PRISMA flow diagram, the three-level "implementation upside" ladder chart, and the
    34-estimate (36-point) forest/scatter plot by operating model. All data values and labels
    were taken directly from the `<text>` elements and `<desc>` accessibility descriptions in
    the original article's SVGs, not approximated.
  - Three tables reproduce the article's risk-of-bias-by-design-route table, its evidence-weight
    table, and its greenfield/brownfield comparison table; a fourth (`longtable`) reproduces the
    full 46-row productivity effect register (E-01–E-46).
- `references.bib` — 185 `@misc` entries: one per source in the article's own registers
  (116 empirical studies + 4 syntheses + 61 contextual/supporting documents = 181) plus the
  4 method-citation sources (PRISMA 2020, Cochrane RoB 2, ROBINS-I V2, JBI critical appraisal
  tools). Each entry has only `title`, `url`, and — where the source article itself states one —
  a `note` (venue/author annotation, e.g. "Google enterprise RCT", "ICSE 2026") and a `year`
  (included only when safely inferable from an arXiv id, a year-coded IEEE DOI, or an explicit
  year/venue mention in the article text). **No author names, journals, volumes, issues or page
  ranges have been invented** for entries where the source article gives only a title and URL.
- `main.bbl` — a pre-compiled bibliography (via `bibtex`), included as a fallback in case arXiv's
  own build does not run `bibtex` against `references.bib` automatically. If you upload
  `references.bib` and arXiv's TeX Live successfully runs `bibtex`, this file is regenerated and
  can be ignored; keeping it in the tarball is a safe no-op either way.
- `main.pdf` — a compiled reference copy (39 pages before the `howpublished` cleanup, 37 pages
  in the final build), so you can review the typeset output without installing LaTeX.

## How to compile

Requires a standard TeX Live installation (tested with TeX Live 2026 / pdfTeX 3.141592653).
No internet connection or external tools are required — `pgfplots`, `tikz`, `natbib`, `xurl` and
`hyperref` are all standard TeX Live packages.

```bash
cd research/ai-coding-productivity/arxiv
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

or, if `latexmk` is installed:

```bash
latexmk -pdf main.tex
```

This was verified to compile cleanly (no errors, no undefined citations, no oversized floats)
with `pdflatex`/`bibtex` from TeX Live 2026 on 22 August 2026.

## Decisions already applied (do not need to be revisited)

- **Primary category:** cs.SE (Software Engineering).
- **Cross-list category:** cs.AI (Artificial Intelligence).
- **License:** CC BY 4.0.
- **Byline:** Ed Yau, Applied AI Architect, Kerv — matching the blog post's own byline and
  `<meta>`/JSON-LD author record (`https://reinvently.co.uk/about/#ed-yau`, LinkedIn
  `uk.linkedin.com/in/edmond-yau`, GitHub `github.com/ed-is-ai`). A footnote on the title page
  notes that the work was produced in a personal capacity and the views are the author's own,
  matching the wording already used on the site's About page.

## What Ed still needs to do himself on arxiv.org

1. **Create or log into** an arXiv account (submission must come from Ed's own account —
   this package does not attempt to access arxiv.org).
2. **Review the manuscript.** Read `main.pdf` (or recompile it) end to end before submitting —
   an AI assistant prepared this conversion and, while every number was checked against the
   published article during preparation (see the parent task's final report for what was
   checked), Ed should not skip his own read-through of a document going out under his name.
3. Start a **new submission**, upload the tarball of `main.tex`, `references.bib` (and
   `main.bbl` as a fallback — no other figure assets exist, since all three figures are native
   TikZ/pgfplots code inside `main.tex`).
4. Choose **cs.SE** as the primary category and add **cs.AI** as a cross-list category.
5. Choose the **CC BY 4.0** license at the licensing step of the submission form.
6. Note that **a first submission to a new category (cs.SE/cs.AI) may require endorsement** from
   an existing arXiv author in that category if Ed's account does not already have submission
   history there — check arXiv's endorsement page if prompted.
7. After arXiv processes the submission, double-check the rendered PDF and abstract page on
   arxiv.org match `main.pdf` (arXiv's own LaTeX toolchain can occasionally differ slightly from
   a local TeX Live install, particularly for `pgfplots`/`tikz` figure rendering).

## Known minor cosmetic issue

Because every bibliography entry omits an `author` field (to avoid inventing authors the source
article does not name), the `plainnat` bibliography style inserts a small stray ", ." after some
titles before the URL (an artifact of `plainnat.bst` handling author-less `@misc` entries). This
is cosmetic only — it does not affect which source each citation points to — but a bibliography
style specialist could clean it up further if Ed wants it removed before submission.

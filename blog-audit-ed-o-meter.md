# Blog Audit — Building the Ed-o-meter (single-post scope)

**Audit date:** 18 July 2026
**File:** `blog/building-the-ed-o-meter-llm-eval-harness/index.html`
**Published:** 16 July 2026 (2 days old — freshness: no action)
**Score:** 66/100

| Category | Score |
|---|---|
| Content quality | 21/30 |
| SEO | 18/25 |
| E-E-A-T | 11/15 |
| Technical | 10/15 |
| AI citation readiness | 6/15 |

## Link health

Not an orphan. Inbound from `index.html`, `blog/index.html`, `tools/ed-o-meter/index.html`,
and both GLM-5.2 posts. Outbound: 3 in-body internal + 3 related + 7 external (all tier 1–2).
Sitemap and blog index entries present with matching dates. No cannibalisation — no other post
targets eval-harness construction.

## Fix queue

### 1. AI-citation structure (biggest single lift: 6/15)
The body is 23 consecutive `<p>` tags. No lists, no table, no `<h3>`, no summary block.
- Add a **"The short answer:"** block after the intro (sibling convention, `glm-5-2-fable-5-gpt-5-5-eval-results/index.html` line 66).
- Convert the "other rules that hardened" paragraph and the "Next" paragraph to `<ul>`.
- Add a design-decisions table (decision / rationale / trade-off).

### 2. FAQPage schema — this post is an outlier
24 of 26 posts carry a second `FAQPage` JSON-LD block. This one doesn't. Add it.
Optional: `SoftwareSourceCode` for Featherbench (MIT, repo URL) is a natural second type.

### 3. Duplicate social image
`images/hero-eval-results.jpg` is used as og:image/twitter:image/hero here **and** by the
eval-results post, the Ed-o-meter tool page, and three homepage cards. The alt text is
byte-identical to the sibling's. The sibling has a dedicated `glm-5-2-eval-og.png` for social;
this post has none.
- Generate `images/ed-o-meter-harness-og.png` (1200×630), update lines 16, 22, 31.
- Rewrite the hero alt so it isn't a copy.

### 4. Prose — house style violations
- **~13 epigrams against a cap of 1–2.** Keep two ("a claim, not a measurement", line 86;
  "settled for measuring it", line 98) and flatten the rest.
- **Triplet fragments at line 128** ("Multi-trial runs… An independent judge… A fresh run…") —
  rewrite as one sentence or a list. Same shape at 124 and 130.
- **~32 em dashes in 2,060 words** (~15/1K). Line 88 alone has five. Target under 15 total.
- **580-word intro before the first H2.** Paragraphs 3 and 4 (lines 68, 70) make overlapping
  points about untrustworthy public numbers — cut ~150 words and add a subhead.
- Avg sentence 27 words (target 15–20); Flesch ~45 (target 60–70).

### 5. Title tag and headings
- Title is 75 chars, keyword at the tail. Suggest `LLM Benchmark Design: Building the
  Ed-o-meter — Reinvently` (58).
- No H2 contains the topic term. Convert two or three where it's natural
  ("Why a New Harness" → "Why Build a New Eval Harness?"). Not all seven — the terse
  build-notes voice is deliberate and shouldn't be turned into a listicle.
- Meta description is well-sized but carries no statistic; "28 tasks" is the obvious candidate.

### 6. Smaller items
- **Chart reference without a chart** (line 116): "drawn as whiskers on the chart" — the
  whiskers are on `/tools/ed-o-meter/`, not this page. Link it or reword.
- **Entity ambiguity**: title says Ed-o-meter, the artefact built is Featherbench. Add one
  early definition sentence.
- **Unsourced claim** (line 68): benchmark test sets "leak into training data" and labs "tune
  for the suites". The linked Goodhart's law page doesn't support this — cite a contamination
  paper or mark it as opinion.
- **No `/contact/` signup CTA**, contrary to standing CTA policy.
- **Verify the "around 850 lines" claim** against the current `eval.py` before it gets cited.
- Hero image is `.jpg` with no width/height — CLS risk.

## Checked and cleared

The 26.4-second TTFT figure and the "top rubric score to a model most shortlists omit, judged
blind by a competitor" claim are **correct** — they match `tools/ed-o-meter/index.html`
(kimi-k3, rubric 9.5, judged by fable-5, ttft 26.4). They describe the full leaderboard run,
not the 3-model sibling post. No fix needed beyond optionally linking the figures to the
leaderboard at the point of use.

AI-detection signals are clean: burstiness ~0.62 (natural), zero blocklisted phrases,
TTR ~0.47. The style problems are house-style ones, not AI-tells.

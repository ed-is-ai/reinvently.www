# Blog Audit Report

**Audit Date:** 2026-07-19
**Total Posts:** 26
**Average Score:** 81/100 (normalized across Content /25, SEO /20, Schema /20, AI Citation /20 — see note on scoring below)

> **Scoring note:** This audit scored four of the five standard categories in depth (Content Quality, SEO, Schema/Technical, AI Citation Readiness) plus a separate Link Health and Freshness pass, via six parallel general-purpose agents. E-E-A-T signals weren't scored as a standalone category. Scores below are normalized to /100 from the 85-point sum of the four scored categories, and are **not directly comparable** to a prior 100-point audit that used a 25/20/20/15/20 (content/SEO/E-E-A-T/technical/AI) split — see git history for that version.

### Health Overview

| Metric | Count |
|--------|-------|
| Posts scoring 90+ (Excellent) | 0 |
| Posts scoring 70–89 (Good) | 26 |
| Posts scoring 50–69 (Needs Work) | 0 |
| Posts scoring <50 (Poor) | 0 |
| Orphan pages | 0 |
| Dead-end pages | 0 |
| Cannibalization issues | 0 |
| Stale content (90+ days) | 0 |

**Headline:** the site is structurally healthy — no orphans, no dead-ends, no broken internal links, no genuine keyword cannibalization, and every post is under 90 days old. The whole corpus clusters tightly in the "Good" band (75–86/100); there are no standout failures and no standout wins. The gaps are systemic template issues, not one-off bad posts.

### Three site-wide systemic issues (fix once, benefits all 26 posts)

1. **`publisher.logo` missing from every post's JSON-LD** — a one-line template fix affecting all 26 posts' rich-result eligibility.
2. **No genuine "Key Takeaways" / TL;DR box anywhere** — every post has only a one-sentence summary line under the H1, not a scannable bulleted capsule. This is the single biggest AI-citation-readiness gap site-wide.
3. **Readability runs well below target across the board** — Flesch Reading Ease sits in the 25–40s site-wide (target 60–70), and average sentence length is consistently 18–26 words (target 15–20). This isn't a content-depth problem, it's a sentence-construction habit, likely fixable with a lighter editing pass rather than a rewrite.

Also worth a light template fix: about half of posts have oversized `<title>` tags (70–117 chars vs. 50–60 ideal), and the suspiciously uniform `dateModified: 2026-07-02` across ~22 of 26 posts looks like a bulk timestamp touch rather than 22 genuine content refreshes — worth confirming that's intentional.

### Per-Post Scores

| Post | Score /100* | Content /25 | SEO /20 | Schema /20 | AI Citation /20 |
|------|-------|---------|-----|-----------|--------------|
| the-rise-of-ai-in-web-development | 86 | 22 | 18 | 17 | 16 |
| is-claude-fable-5-worth-it-for-enterprise-coding | 85 | 19 | 19 | 17 | 17 |
| generative-ai-adoption-by-industry | 85 | 20 | 18 | 17 | 17 |
| claude-mythos-anthropic-opportunity-for-companies | 84 | 21 | 18 | 17 | 15 |
| enterprise-ai-adoption-reality-check-2026 | 84 | 19 | 17 | 17 | 18 |
| gpt-5-5-autonomous-task-completion | 84 | 20 | 19 | 17 | 15 |
| rag-vs-graphrag | 84 | 20 | 18 | 17 | 16 |
| ai-agent-governance-gap | 82 | 18 | 17 | 17 | 18 |
| claude-memory-dream-enterprise-agents | 82 | 21 | 15 | 17 | 17 |
| copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | 82 | 20 | 18 | 16 | 16 |
| github-copilot-vs-claude-code-vs-cursor | 82 | 17 | 19 | 17 | 17 |
| glm-5-2-fable-5-gpt-5-5-eval-results | 82 | 19 | 16 | 17 | 18 |
| ai-agent-interoperability-a2a-protocol | 81 | 20 | 17 | 17 | 15 |
| global-ai-adoption-attitudes | 81 | 20 | 16 | 17 | 16 |
| top-10-uk-ai-companies | 81 | 18 | 19 | 17 | 15 |
| uk-ai-policy-landscape-enterprise-2026 | 81 | 19 | 17 | 17 | 16 |
| uk-ai-skills-gap-education-opportunity | 81 | 21 | 15 | 17 | 16 |
| building-the-ed-o-meter-llm-eval-harness | 80 | 18 | 18 | 17 | 15 |
| microsoft-foundry-deep-dive | 80 | 19 | 16 | 17 | 16 |
| uk-ai-growth-labs-regulatory-sandboxes | 80 | 17 | 17 | 17 | 17 |
| ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit | 79 | 19 | 15 | 17 | 16 |
| uk-sovereign-ai-programme | 79 | 17 | 17 | 17 | 16 |
| multi-agent-orchestration-frameworks-compared | 78 | 19 | 14 | 17 | 16 |
| uk-ai-regulation-ico-employment-2026 | 77 | 17 | 15 | 17 | 16 |
| microvm-sandbox-options-firecracker-opensandbox-smolvm-nono | 75 | 17 | 14 | 17 | 16 |
| uk-government-ai-institutes | 75 | 16 | 15 | 17 | 16 |

*Normalized to /100 from the 85-point raw sum.

### Prioritized Action Queue (lowest score first)

| Priority | Post | Score | Top Issue | Recommended Action |
|----------|------|-------|-----------|--------------------|
| 1 | uk-government-ai-institutes | 75 | Longest avg. sentence length in the corpus (25.5 words); H1/title framing mismatch ("Public AI Infrastructure" vs. "Government AI Institutes") | Light readability edit + align H1 to title tag |
| 2 | microvm-sandbox-options-... | 75 | Title (101 chars) and slug (61 chars) both excessively long; 17 paragraphs in the dense 80–150 word zone | Shorten title tag; break up dense paragraphs |
| 3 | uk-ai-regulation-ico-employment-2026 | 77 | Title tag excessively long (105 chars); sentences read legalistic/dense (24.4 words avg) | Shorten title; simplify sentence structure |
| 4 | multi-agent-orchestration-frameworks-compared | 78 | Title tag extremely long (113–117 chars), heavy SERP truncation | Rewrite title tag to ~55–60 chars |
| 5 | ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit | 79 | Title tag far too long (97 chars) plus a 51-char slug | Shorten title tag |
| 5 | uk-sovereign-ai-programme | 79 | Hardest post in the corpus to read (Flesch 25, avg. sentence 26.2 words); title tag over ideal length (89 chars) | Readability pass + trim title |
| 7 | building-the-ed-o-meter-llm-eval-harness | 80 | Only 2 inbound internal links (weakly connected, not orphaned); code appendix wrapped in `<p>` not `<pre>`/`<code>` | Add 1–2 inbound links from tooling-adjacent posts; fix code markup |
| 7 | microsoft-foundry-deep-dive | 80 | H1 much longer/different from short title tag; very dense (Flesch 26) | Align H1 to title; simplify prose |
| 7 | uk-ai-growth-labs-regulatory-sandboxes | 80 | Avg. sentence 24.2 words — long throughout; title tag over ideal length (84 chars) | Readability pass + trim title |

*(Remaining 17 posts score 81–86 and need only the site-wide template fixes below, not individual rework.)*

### Cannibalization Report

No genuine keyword cannibalization found. Every cluster initially flagged as a risk (UK policy posts, eval/benchmark posts, tool comparisons, adoption-stats posts) turned out to be either intentional hub-and-spoke architecture with existing cross-links, or segmented by a distinct axis (entity, geography, sector, technical layer) with no real search-intent overlap.

| Keyword/Intent | Competing Posts | Recommendation |
|---|---|---|
| Microsoft Foundry ("what it is") | microsoft-foundry-deep-dive vs. copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | Differentiate (already done, bidirectionally linked) — monitor that the comparison post's Foundry section doesn't expand into a second deep-dive |
| UK AI policy (broad map vs. spokes) | uk-ai-policy-landscape-enterprise-2026 (pillar) vs. its 5 UK spokes | Not cannibalization — deliberate pillar/spoke, already cross-linked |
| Fable 5 / GLM-5.2 coding evals | is-claude-fable-5-worth-it-for-enterprise-coding vs. glm-5-2-fable-5-gpt-5-5-eval-results vs. building-the-ed-o-meter-llm-eval-harness | Not cannibalization — benchmark report / build methodology / buy decision are distinct intents, already cross-linked |
| AI adoption statistics | generative-ai-adoption-by-industry vs. global-ai-adoption-attitudes vs. enterprise-ai-adoption-reality-check-2026 | Not cannibalization — segmented by sector / geography / ROI respectively |

### Orphan Pages

None. All 26 posts have ≥2 inbound internal links from other posts and are listed on `blog/index.html`. Two posts are worth reinforcing (not orphaned, just thin):

| Page | Inbound Links | Recommended Link Sources |
|------|---------------|--------------------------|
| building-the-ed-o-meter-llm-eval-harness | 2 | multi-agent-orchestration-frameworks-compared, github-copilot-vs-claude-code-vs-cursor |
| glm-5-2-fable-5-gpt-5-5-eval-results | 2 | gpt-5-5-autonomous-task-completion, ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit |

Dead-end pages: none — every post has ≥2 outbound internal links. No broken internal link targets found anywhere in the corpus.

### Stale Content

All 26 posts fall under 90 days since `dateModified` (today: 2026-07-19), so by the stated thresholds every post is **Low priority** on urgency. However:

- **~22 of 26 posts share the identical `dateModified: 2026-07-02`** — this pattern is consistent with a site-wide template/metadata touch rather than 22 individual content reviews on that day. Recommend confirming whether these posts actually had their content revised on that date, since the freshness signal may be overstating how recently the *content itself* (not just the timestamp) was reviewed.
- Refresh effort ratings below reflect topic decay speed (how fast the subject matter goes stale), not current urgency:

| Post | Last Updated | Days Stale | Priority | Refresh Effort |
|------|-------------|------------|----------|----------------|
| copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | 2026-07-02 | 17 | Low | Heavy |
| github-copilot-vs-claude-code-vs-cursor | 2026-07-02 | 17 | Low | Heavy |
| gpt-5-5-autonomous-task-completion | 2026-07-02 | 17 | Low | Heavy |
| microsoft-foundry-deep-dive | 2026-07-02 | 17 | Low | Heavy |
| top-10-uk-ai-companies | 2026-07-02 | 17 | Low | Heavy |
| uk-ai-policy-landscape-enterprise-2026 | 2026-07-02 | 17 | Low | Heavy |
| uk-ai-regulation-ico-employment-2026 | 2026-07-02 | 17 | Low | Heavy |
| glm-5-2-fable-5-gpt-5-5-eval-results | 2026-07-05 | 14 | Low | Heavy |
| is-claude-fable-5-worth-it-for-enterprise-coding | 2026-07-19 | 0 | Low | Heavy |
| ai-agent-governance-gap | 2026-07-02 | 17 | Low | Moderate |
| ai-agent-interoperability-a2a-protocol | 2026-07-02 | 17 | Low | Moderate |
| ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit | 2026-07-02 | 17 | Low | Moderate |
| enterprise-ai-adoption-reality-check-2026 | 2026-07-02 | 17 | Low | Moderate |
| generative-ai-adoption-by-industry | 2026-07-02 | 17 | Low | Moderate |
| global-ai-adoption-attitudes | 2026-07-02 | 17 | Low | Moderate |
| microvm-sandbox-options-... | 2026-07-02 | 17 | Low | Moderate |
| multi-agent-orchestration-frameworks-compared | 2026-07-02 | 17 | Low | Moderate |
| uk-ai-growth-labs-regulatory-sandboxes | 2026-07-02 | 17 | Low | Moderate |
| uk-government-ai-institutes | 2026-07-02 | 17 | Low | Moderate |
| uk-sovereign-ai-programme | 2026-07-02 | 17 | Low | Moderate |
| rag-vs-graphrag | 2026-07-01 | 18 | Low | Light |
| claude-memory-dream-enterprise-agents | 2026-07-02 | 17 | Low | Light |
| the-rise-of-ai-in-web-development | 2026-07-02 | 17 | Low | Light |
| uk-ai-skills-gap-education-opportunity | 2026-07-02 | 17 | Low | Light |
| building-the-ed-o-meter-llm-eval-harness | 2026-07-16 | 3 | Low | Light |
| claude-mythos-anthropic-opportunity-for-companies | 2026-07-19 | 0 | Low | Light |

### Recommended next steps

1. Fix the two site-wide template issues first (highest leverage, one change benefits all 26 posts): add `publisher.logo` to the JSON-LD template, and add a real "Key Takeaways" bulleted box under the H1 across the template.
2. Run `/blog analyze uk-government-ai-institutes` and `/blog analyze microvm-sandbox-options-firecracker-opensandbox-smolvm-nono` first — the two lowest-scoring posts.
3. Run `/blog geo` on the eval/benchmark cluster (glm-5-2-fable-5-gpt-5-5-eval-results, is-claude-fable-5-worth-it-for-enterprise-coding, building-the-ed-o-meter-llm-eval-harness) to tighten AI-citation formatting, since these are high-value, fast-decaying topics.
4. Add the two recommended inbound links to strengthen the thinly-connected eval posts.
5. Confirm whether the shared 2026-07-02 `dateModified` reflects real content revisions or just a template touch — if the latter, treat those 22 posts' actual freshness as their `datePublished`, not `dateModified`.

> **Note:** a prior, more forensic audit of this same corpus exists in git history (see `git log -- blog-audit-report.md`), which cross-referenced git-tracked file state, per-line prose style issues, and specific unsourced-statistic claims. That audit flagged items this pass didn't check (uncited statistics, `og:image` pointing at a generic hero, nav inconsistency across posts, prose-style tells like repeated "X is not Y. It is Z." constructions). Worth revisiting those P0/P1 items directly rather than assuming this pass supersedes them — this run used a different, more generic scoring rubric and did not re-verify sourcing or prose style.

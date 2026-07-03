# Blog Audit Report

**Audit Date:** 3 July 2026
**Total Posts:** 27 (26 published + 1 noindexed draft)
**Average Score:** 71.6 / 100 (73.5 excluding the draft)
**Method:** Full editorial deep-read by parallel review agents (content quality, E-E-A-T, AI-citation readiness) plus deterministic structural checks (SEO tags, schema, link graph, freshness). This rubric is substantially stricter than the 2 July structural-only audit (which scored 95.9) — the two are not comparable. Structural hygiene is now largely clean; the remaining findings are editorial: sourcing, schema/content mismatches, title lengths, and copy defects.

## Health Overview

| Metric | Count |
|--------|-------|
| Posts scoring 90+ (Excellent) | 0 |
| Posts scoring 70–89 (Good) | 18 |
| Posts scoring 50–69 (Needs work) | 8 |
| Posts scoring <50 (Poor) | 1 (noindexed draft) |
| Orphan pages | 1 (the same draft — intentional) |
| Dead-end pages | 0 |
| Broken internal links | 0 |
| FAQ schema without visible FAQ | 8 |
| Stale content (90+ days) | 0 |

Structural checks that pass site-wide: every post has a correct canonical, complete OG + Twitter tags, exactly one H1, a 149–160-char meta description, BlogPosting schema, and ≥6 internal body links. No post is stale (all dateModified within 1 day).

## Per-Post Scores

| Post | Score | Content /25 | SEO /20 | E-E-A-T /20 | Technical /15 | AI Citation /20 | Issues |
|------|-------|---------|-----|---------|-----------|-------------|--------|
| glm-5-2-vs-claude-opus-vs-gpt-5-5-coding | 84 | 22 | 17 | 17 | 14 | 14 | 5 |
| glm-5-2-china-data-residency-api-vs-open-weights | 83 | 22 | 16 | 17 | 14 | 14 | 5 |
| multi-agent-orchestration-frameworks-compared | 83 | 22 | 15 | 16 | 13 | 17 | 4 |
| open-weight-frontier-models-enterprise-glm-5-2 | 82 | 22 | 17 | 17 | 13 | 13 | 5 |
| microvm-sandbox-options-firecracker-opensandbox-smolvm-nono | 81 | 23 | 15 | 13 | 13 | 17 | 4 |
| gpt-5-5-autonomous-task-completion | 80 | 20 | 17 | 13 | 14 | 16 | 5 |
| ai-agent-governance-gap | 79 | 21 | 15 | 17 | 13 | 13 | 5 |
| the-rise-of-ai-in-web-development | 77 | 21 | 16 | 13 | 12 | 15 | 5 |
| uk-ai-growth-labs-regulatory-sandboxes | 77 | 22 | 15 | 17 | 10 | 13 | 5 |
| uk-ai-policy-landscape-enterprise-2026 | 77 | 22 | 15 | 16 | 10 | 14 | 5 |
| uk-sovereign-ai-programme | 75 | 21 | 14 | 13 | 12 | 15 | 5 |
| ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit | 74 | 20 | 13 | 13 | 12 | 16 | 6 |
| enterprise-ai-adoption-reality-check-2026 | 73 | 20 | 14 | 12 | 12 | 15 | 6 |
| rag-vs-graphrag | 73 | 20 | 16 | 10 | 12 | 15 | 6 |
| top-10-uk-ai-companies | 72 | 20 | 15 | 10 | 12 | 15 | 7 |
| uk-ai-regulation-ico-employment-2026 | 72 | 20 | 13 | 13 | 11 | 15 | 7 |
| uk-government-ai-institutes | 72 | 20 | 14 | 11 | 12 | 15 | 6 |
| github-copilot-vs-claude-code-vs-cursor | 70 | 18 | 15 | 14 | 11 | 12 | 7 |
| claude-memory-dream-enterprise-agents | 69 | 18 | 13 | 10 | 13 | 15 | 7 |
| copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | 69 | 20 | 14 | 12 | 11 | 12 | 6 |
| global-ai-adoption-attitudes | 69 | 18 | 16 | 8 | 12 | 15 | 7 |
| generative-ai-adoption-by-industry | 68 | 19 | 14 | 9 | 12 | 14 | 9 |
| ai-agent-interoperability-a2a-protocol | 65 | 15 | 13 | 10 | 12 | 15 | 8 |
| uk-ai-skills-gap-education-opportunity | 65 | 17 | 14 | 8 | 12 | 14 | 8 |
| microsoft-foundry-deep-dive | 63 | 17 | 14 | 8 | 10 | 14 | 8 |
| claude-mythos-anthropic-opportunity-for-companies | 60 | 14 | 13 | 7 | 13 | 13 | 8 |
| glm-5-2-fable-5-codex-real-task-results (draft, noindex) | 22 | 5 | 4 | 5 | 5 | 3 | 12+ |

## Prioritized Action Queue

Copy defects first (fast, embarrassing if found by a reader), then the systemic fixes.

| Priority | Post | Score | Top Issue | Recommended Action |
|----------|------|-------|-----------|--------------------|
| 1 | uk-ai-regulation-ico-employment-2026 | 72 | Body still advises submitting to the ICO consultation that "closes on 29 May 2026" — the FAQ says it already closed | Rewrite the consultation passage in past tense; fix the unclosed `<p>` at the "central warning" paragraph |
| 2 | ai-agent-interoperability-a2a-protocol | 65 | Broken mid-edit sentence: "…but getting The conventional approach to multi-agent…" | Repair the sentence; link the "150+ organisations" claim to a primary source |
| 3 | microsoft-foundry-deep-dive | 63 | Malformed nested anchor (`href="https://<a href="…`) renders broken HTML | Fix the anchor; refresh stale model names (Opus 4.1, GPT-5.2); add sources beyond vendor homepages |
| 4 | 8 posts (see below) | — | FAQPage JSON-LD with no visible FAQ on the page — rich-result policy violation | Either render the FAQ section (preferred — the Q&As are good) or strip the schema |
| 5 | open-weight-frontier-models-enterprise-glm-5-2 | 82 | SWE-bench Pro 62.1-vs-58.6 presented as a direct beat in meta, schema, intro, and chart — cross-harness runs are not comparable, and the sibling coding post says so explicitly | Add the harness caveat everywhere the number appears |
| 6 | copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | 69 | FAQ schema names a nonexistent product, "Azure Bedrock" | Correct to AWS Bedrock; also add third-party sources (currently vendor-only) |
| 7 | claude-mythos-anthropic-opportunity-for-companies | 60 | No byline, extraordinary claims sourced only to Anthropic, strongest AI-writing cadence of the set | Add byline + independent sources; de-hype vocabulary ("significant" ×10) |
| 8 | uk-ai-skills-gap-education-opportunity | 65 | Headline stats (73%, £400bn, £187m, 10m by 2030) have zero source links | Source every number or cut it; tone down motivational-fragment closers |
| 9 | github-copilot-vs-claude-code-vs-cursor | 70 | Same "anecdotally… switched" passage appears verbatim twice | Delete one instance; source the "one-third of API price" Microsoft claim |
| 10 | global-ai-adoption-attitudes | 69 | Visible date (13 Feb 2026) conflicts with schema datePublished (2026-04-20); unsourced 73%/$100bn/$40bn stats | Align the dates; add sources |
| 11 | reality-check / generative-ai / multi-agent posts | — | Literal `\$202m` backslash renders in related-posts links (3 posts) | Remove the stray backslashes |
| 12 | glm-5-2-fable-5-codex-real-task-results | 22 | Draft with [DATA NEEDED]/[DATE] placeholders and invalid `2026-07-XX` schema dates — correctly noindexed and unlinked, but the URL is live | Fill in results and publish (it is cluster spoke 5), or hold it out of the repo until ready |

### FAQ schema/content mismatch (8 posts)

`ai-agent-governance-gap`, `copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock`, `github-copilot-vs-claude-code-vs-cursor`, `glm-5-2-china-data-residency-api-vs-open-weights`, `glm-5-2-vs-claude-opus-vs-gpt-5-5-coding`, `open-weight-frontier-models-enterprise-glm-5-2`, `uk-ai-growth-labs-regulatory-sandboxes`, `uk-ai-policy-landscape-enterprise-2026`

The other 18 published posts render their FAQs correctly — the template used for the newest posts diverged. Rendering the existing schema Q&As as a visible FAQ section fixes the policy risk *and* adds the Q&A formatting the AI-citation scores dock these posts for.

## Topic Cannibalization

| Keyword | Competing Posts | Recommendation |
|---------|----------------|----------------|
| "GLM-5.2 vs Claude coding" | glm-5-2-vs-claude-opus-vs-gpt-5-5-coding, glm-5-2-fable-5-codex-real-task-results | **Differentiate** — benchmark/spec comparison vs first-hand task results; cross-link explicitly when the draft publishes. Also: the coding post's slug says "claude-opus" but compares Fable 5 |
| "UK AI regulation 2026" | uk-ai-policy-landscape-enterprise-2026, uk-ai-regulation-ico-employment-2026 | **Differentiate** — keep the landscape post broad; tilt the ICO post's title/meta harder toward employment/HR obligations |
| "Microsoft Foundry" | microsoft-foundry-deep-dive, copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | **Differentiate** — distinct intents, but normalise the product name (one says "Microsoft Foundry", the other "Azure AI Foundry") |

The GLM cluster (pillar + spokes), UK-policy cluster, and the three adoption-stats posts are intentional hub-and-spoke structures with distinct intents — not cannibalization.

## Orphan Pages

| Page | Inbound Links | Notes / Recommended Link Sources |
|------|---------------|----------------------------------|
| glm-5-2-fable-5-codex-real-task-results | 0 | Intentional (noindexed draft). On publish: link from the pillar (open-weight-frontier-models…), glm-5-2-vs-claude-opus…, glm-5-2-china…, and list on /blog/ + /news/ hubs |

No dead-end pages; no broken internal links; every published post is listed on at least one hub page.

## Stale Content

None. All 26 published posts have dateModified of 1–2 July 2026. (The site's real freshness risk is *content* staleness flagged above — the ICO consultation copy and the Foundry model catalogue — not date staleness.)

## Site-Wide Patterns (fix once, apply everywhere)

1. **No TL;DR / Key Takeaways boxes anywhere.** Every reviewer docked AI-citation points for this. The highest-leverage single addition across the site.
2. **Generic og:image.** All 27 posts share `/images/hero.jpg` — no post-specific social cards, and zero images in any article body.
3. **Author attribution inconsistent.** Some posts have an Ed Yau byline with Organization schema author, some Person schema, several posts (claude-mythos, reality-check, generative-ai-adoption, microvm, global-attitudes) have no visible byline at all. Standardise: visible byline + Person author (jobTitle "Applied AI Architect") on every post.
4. **Title tags too long.** 12 posts exceed 70 chars with the brand suffix (worst: multi-agent 113, ICO 105, microvm 101, ai-dev-workflow 97). Several already have correctly-sized twitter:title variants to promote.
5. **Unsourced statistics.** The most common E-E-A-T deduction — load-bearing numbers linked to homepages or nothing (worst offenders: skills-gap, top-10-uk-ai-companies, global-attitudes, claude-memory-dream, uk-government-institutes).
6. **AI-writing cadence.** Flagged in claude-mythos, microsoft-foundry, claude-memory-dream, global-attitudes, skills-gap: "significant" repetition, "not X, but Y" reflex, symmetric section scaffolding, motivational triplets. The GLM cluster and microvm posts read clean — use them as the house-style reference.

## Suggested Next Steps

- `/blog analyze blog/claude-mythos-anthropic-opportunity-for-companies/index.html` — lowest published score
- Batch-fix the FAQ schema mismatch (8 posts, one template pattern)
- `/blog geo` on the pillar posts (open-weight-frontier…, uk-ai-policy-landscape…) once FAQs are visible

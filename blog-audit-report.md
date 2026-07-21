# Blog Audit Report

**Audit Date:** 2026-07-21 (rescore after edits)
**Total Posts:** 26
**Average Score:** 76/100 (was 74 pre-edit)

> **Scoring note:** Full standard 5-category rubric (Content Quality /30, SEO /25, E-E-A-T /15, Technical /15, AI Citation Readiness /15), scored per-post by `blog-reviewer` agents. This is a rescore following edits to six posts. The 20 untouched posts are byte-for-byte unchanged since the initial 2026-07-21 audit, so their scores are carried forward rather than re-run (re-scoring unchanged files only adds ±2-3pt scorer noise). The six edited posts were re-scored fresh.

## Health Overview

| Metric | Count | Was |
|--------|-------|-----|
| Posts Scoring 90+ (Excellent) | 0 | 0 |
| Posts Scoring 80-89 (Strong) | 7 | 5 |
| Posts Scoring 70-79 (Acceptable) | 17 | 16 |
| Posts Scoring 60-69 (Below Standard) | 2 | 5 |
| Posts Scoring <60 (Poor) | 0 | 0 |
| Orphan Pages | 0 | 0 |
| Dead-End Pages | 0 | 0 |
| Cannibalization Issues | 2 (low severity) | 2 |
| Stale Content (90+ days) | 0 | 0 |

The six-post edit pass lifted two posts out of the Below-Standard band and added two to the Strong band. The two posts remaining Below Standard (`claude-mythos` 63, `uk-government-ai-institutes` 69) were not part of the edit pass.

## Per-Post Scores (sorted, highest first)

| Post | Score | Prev | Δ | Content /30 | SEO /25 | E-E-A-T /15 | Tech /15 | AI-Cite /15 |
|------|-------|------|-----|------|-----|------|------|------|
| glm-5-2-fable-5-gpt-5-5-eval-results ✏️ | 88 | 86 | +2 | 27 | 22 | 13 | 12 | 14 |
| is-claude-fable-5-worth-it-for-enterprise-coding ✏️ | 86 | 82 | +4 | 26 | 22 | 12 | 12 | 14 |
| top-10-uk-ai-companies ✏️ | 84 | 64 | +20 | 24 | 22 | 13 | 12 | 13 |
| uk-ai-skills-gap-education-opportunity ✏️ | 84 | 68 | +16 | 25 | 22 | 13 | 11 | 13 |
| building-the-ed-o-meter-llm-eval-harness ✏️ | 82 | 81 | +1 | 26 | 21 | 12 | 11 | 12 |
| ai-agent-governance-gap | 80 | 80 | — | 23 | 20 | 11 | 13 | 13 |
| claude-memory-dream-enterprise-agents | 80 | 80 | — | 24 | 19 | 12 | 12 | 13 |
| copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock ✏️ | 79 | 65 | +14 | 22 | 21 | 11 | 12 | 13 |
| the-rise-of-ai-in-web-development | 79 | 79 | — | 25 | 18 | 11 | 12 | 13 |
| github-copilot-vs-claude-code-vs-cursor | 78 | 78 | — | 24 | 19 | 11 | 11 | 13 |
| ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit | 77 | 77 | — | 23 | 16 | 11 | 14 | 13 |
| microvm-sandbox-options-firecracker-opensandbox-smolvm-nono | 77 | 77 | — | 24 | 15 | 13 | 12 | 13 |
| uk-ai-policy-landscape-enterprise-2026 | 77 | 77 | — | 23 | 19 | 12 | 10 | 13 |
| enterprise-ai-adoption-reality-check-2026 | 76 | 76 | — | 23 | 20 | 10 | 11 | 12 |
| multi-agent-orchestration-frameworks-compared | 76 | 76 | — | 25 | 16 | 11 | 11 | 13 |
| rag-vs-graphrag | 73 | 73 | — | 20 | 19 | 7 | 13 | 14 |
| uk-sovereign-ai-programme | 73 | 73 | — | 21 | 17 | 11 | 12 | 12 |
| ai-agent-interoperability-a2a-protocol | 72 | 72 | — | 23 | 17 | 10 | 10 | 12 |
| gpt-5-5-autonomous-task-completion | 72 | 72 | — | 20 | 20 | 7 | 12 | 13 |
| uk-ai-growth-labs-regulatory-sandboxes | 72 | 72 | — | 19 | 19 | 10 | 11 | 13 |
| generative-ai-adoption-by-industry | 71 | 71 | — | 21 | 19 | 9 | 10 | 12 |
| microsoft-foundry-deep-dive | 71 | 71 | — | 21 | 19 | 7 | 13 | 11 |
| uk-ai-regulation-ico-employment-2026 | 71 | 71 | — | 20 | 19 | 10 | 10 | 12 |
| global-ai-adoption-attitudes | 70 | 70 | — | 20 | 19 | 8 | 10 | 13 |
| uk-government-ai-institutes | 69 | 69 | — | 20 | 17 | 8 | 11 | 13 |
| claude-mythos-anthropic-opportunity-for-companies | 63 | 63 | — | 18 | 14.5 | 9 | 10 | 11.5 |

✏️ = edited in the 2026-07-21 fix pass and re-scored.

## What the Edit Pass Changed

Six posts were edited: three low scorers (top-10, copilot-studio, skills-gap) got the biggest lifts; three eval posts got smaller polish gains. Key changes:

- **Factual corrections** — several stale/wrong stats fixed with sourced citations: Darktrace (9,000→~10,000 orgs), Synthesia (55,000→60,000+ companies), PolyAI ($120M→$200M+), BenevolentAI (removed unverified MHRA claim; corrected to FDA EUA, credited Eli Lilly), Quantexa valuation, Copilot Studio pricing (messages→Copilot Credits), Bedrock feature renames (Agents→AgentCore).
- **Entity fix** — copilot-studio's "Azure AI Foundry" (title) vs "Microsoft Foundry" (body) mismatch aligned.
- **Schema integrity** — ed-o-meter's FAQPage JSON-LD described 5 Q&As absent from the page (a Google structured-data policy risk); a matching visible FAQ was added.
- **Content gap** — skills-gap's meta promised a "where it bites hardest" breakdown the body never delivered; added a sourced DSIT sector/region section + table.
- **Structure** — comparison tables (top-10, skills-gap), contextual internal links woven into body copy, title-tag length fixes, visible "Updated" freshness signals.

## Systemic Issues (still the main score ceiling)

Two gaps still recur across the *unedited* posts and cap the site average:

1. **Missing experience/originality signals.** Most posts synthesize third-party data with no first-person "when we deployed for a client…" markers. This is the dominant E-E-A-T ceiling (posts like `rag-vs-graphrag`, `gpt-5-5-autonomous`, `microsoft-foundry-deep-dive` sit at 7/15). It is the one fix that requires the author's own material and cannot be automated.
2. **No contextual internal links in body copy** on ~11 remaining posts (footer "related posts" only). The 3 edited posts fixed this; the rest still rely on the footer block.

Common Technical cap: most posts have only 2 schema types (BlogPosting + FAQPage) vs the 3+ bonus threshold, and `.jpg` heroes rather than WebP/AVIF.

## Prioritized Action Queue (Lowest Score First)

| Priority | Post | Score | Top Issue | Recommended Action |
|----------|------|-------|-----------|--------------------|
| 1 | claude-mythos-anthropic-opportunity-for-companies | 63 | Weakest content depth + no internal links | Deepen analysis, add 3-6 contextual internal links |
| 2 | uk-government-ai-institutes | 69 | No in-body internal links across 7 sections | Weave 3-6 contextual internal links |
| 3 | global-ai-adoption-attitudes | 70 | No originality/experience markers | Add first-person experience block |
| 4 | generative-ai-adoption-by-industry | 71 | Zero original data | Add experience passage + more internal links |
| 5 | microsoft-foundry-deep-dive | 71 | No internal links + no experience markers | Add internal links + experience note |
| 6 | uk-ai-regulation-ico-employment-2026 | 71 | No original data/experience | Add experience/insight passage |
| 7 | ai-agent-interoperability-a2a-protocol | 72 | Zero contextual internal links | Weave 3-5 internal links into body |
| 8 | gpt-5-5-autonomous-task-completion | 72 | E-E-A-T weakest (7/15): no firsthand markers | Add firsthand experience + 2-3 tier 1-3 citations |
| 9 | uk-ai-growth-labs-regulatory-sandboxes | 72 | Title over length; no originality markers | Shorten title; add unique-insight block |
| 10 | rag-vs-graphrag | 73 | No originality/experience signals | Add first-hand example + in-body internal links |

## Cannibalization Report

| Topic | Competing Posts | Recommendation |
|-------|-----------------|-----------------|
| Microsoft Foundry / Copilot Studio | copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock (79), microsoft-foundry-deep-dive (71) | Differentiate — now cross-linked in body; sharpen each intro to state distinct intent (buyer comparison vs. architecture reference) |
| AI adoption statistics | enterprise-ai-adoption-reality-check-2026 (76), generative-ai-adoption-by-industry (71), global-ai-adoption-attitudes (70) | Low severity — differentiated by angle (ROI / industry / country) but overlapping survey sources; monitor as the cluster grows |

## Orphan Pages, Dead-End Pages, Stale Content

None found. Link graph fully connected; all 26 posts have `dateModified` within the freshness threshold (six now dated 2026-07-21 after the edit pass).

## Quick Stats

- Total posts audited: 26
- Average score: 76/100 (was 74)
- Score range: 63-88 (was 63-86)
- Strong (80-89): 7 posts (was 5)
- Below Standard (60-69): 2 posts (was 5)
- Posts still missing experience/originality markers: ~11
- Posts still missing in-body contextual internal links: ~11
- Internal link graph: fully connected, no orphans or dead-ends

# Blog Audit Report

**Audit Date:** 1 July 2026
**Total Posts:** 20
**Average Score:** 76.8 / 100
**Method:** Automated structural audit (SEO tags, schema, internal-link graph, freshness, word count). Category scores are heuristic proxies, not a full editorial read — run `/blog-analyze <file>` for a deep per-post score.

> **Headline finding:** the "Related posts" block is **static** — every post links to the same three articles (`ai-dev-workflow-frameworks`, `claude-memory-dream`, `gpt-5-5`). That single template choice creates **13 orphan pages** and makes most internal links topically irrelevant. Fixing it lifts SEO and AI-citation signals across the whole site.

## Health Overview
| Metric | Count |
|--------|-------|
| Posts scoring 90+ (Excellent) | 1 |
| Posts scoring 70–89 (Good) | 15 |
| Posts scoring 50–69 (Needs work) | 4 |
| Posts scoring <50 (Poor) | 0 |
| Orphan pages (0 inbound internal links) | 13 |
| Dead-end pages (0 outbound internal links) | 1 |
| Topic cannibalization clusters | 1 (soft) |
| Stale content (>90 days since publish) | 5 |

## Per-Post Scores (lowest first)
| Post | Score | Content /25 | SEO /20 | E-E-A-T /20 | Technical /15 | AI Citation /20 | Top issue |
|------|-------|-------------|---------|-------------|---------------|-----------------|-----------|
| the-rise-of-ai-in-web-development | 63 | 8 | 17 | 13 | 15 | 10 | Thin content (<700 words) |
| claude-mythos-anthropic-opportunity-for-companies | 68 | 14 | 14 | 13 | 15 | 12 | Orphan (0 inbound links) |
| enterprise-ai-adoption-reality-check-2026 | 68 | 20 | 8 | 13 | 15 | 12 | Orphan (0 inbound links) |
| uk-sovereign-ai-programme | 68 | 20 | 8 | 13 | 15 | 12 | Orphan (0 inbound links) |
| microvm-sandbox-options-firecracker-opensandbox-smolvm-nono | 70 | 25 | 5 | 13 | 15 | 12 | Orphan + dead-end (0 in/0 out) |
| rag-vs-graphrag | 71 | 14 | 17 | 13 | 15 | 12 | Orphan (0 inbound links) |
| uk-ai-regulation-ico-employment-2026 | 71 | 20 | 11 | 13 | 15 | 12 | Meta description too long (231 chars) |
| claude-memory-dream-enterprise-agents | 74 | 20 | 11 | 16 | 15 | 12 | Meta description too long (204 chars) |
| generative-ai-adoption-by-industry | 75 | 25 | 10 | 13 | 15 | 12 | Orphan (0 inbound links) |
| uk-ai-skills-gap-education-opportunity | 75 | 14 | 14 | 20 | 15 | 12 | Orphan (0 inbound links) |
| ai-agent-interoperability-a2a-protocol | 76 | 20 | 13 | 16 | 15 | 12 | Meta description too long (233 chars) |
| gpt-5-5-autonomous-task-completion | 78 | 20 | 15 | 16 | 15 | 12 | Meta description too long (214 chars) |
| uk-government-ai-institutes | 79 | 25 | 14 | 13 | 15 | 12 | Orphan (0 inbound links) |
| global-ai-adoption-attitudes | 80 | 25 | 15 | 13 | 15 | 12 | Orphan (0 inbound links) |
| microsoft-foundry-deep-dive | 82 | 25 | 14 | 16 | 15 | 12 | Orphan (0 inbound links) |
| ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit | 83 | 25 | 11 | 20 | 15 | 12 | No FAQ schema (GEO) |
| copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | 85 | 20 | 10 | 20 | 15 | 20 | Orphan (0 inbound links) |
| top-10-uk-ai-companies | 86 | 25 | 14 | 20 | 15 | 12 | Orphan (0 inbound links) |
| multi-agent-orchestration-frameworks-compared | 88 | 25 | 8 | 20 | 15 | 20 | Orphan (0 inbound links) |
| github-copilot-vs-claude-code-vs-cursor | 95 | 25 | 15 | 20 | 15 | 20 | Meta description too long (223 chars) |

## Prioritised Action Queue (lowest score first)
| # | Post | Score | Top issue | Recommended action |
|---|------|-------|-----------|--------------------|
| 1 | the-rise-of-ai-in-web-development | 63 | Thin content (<700 words) | Expand to 1,000+ words or merge into a stronger post |
| 2 | claude-mythos-anthropic-opportunity-for-companies | 68 | Orphan (0 inbound links) | Link to it from 2–3 topically-related posts |
| 3 | enterprise-ai-adoption-reality-check-2026 | 68 | Orphan (0 inbound links) | Link to it from 2–3 topically-related posts |
| 4 | uk-sovereign-ai-programme | 68 | Orphan (0 inbound links) | Link to it from 2–3 topically-related posts |
| 5 | microvm-sandbox-options-firecracker-opensandbox-smolvm-nono | 70 | Orphan + dead-end (0 in/0 out) | Add a Related-posts block AND get 2–3 relevant posts to link to it |
| 6 | rag-vs-graphrag | 71 | Orphan (0 inbound links) | Link to it from 2–3 topically-related posts |
| 7 | uk-ai-regulation-ico-employment-2026 | 71 | Meta description too long (231 chars) | Trim meta description to 150–160 chars |
| 8 | claude-memory-dream-enterprise-agents | 74 | Meta description too long (204 chars) | Trim meta description to 150–160 chars |

## Internal Linking (the core problem)
Every post carries a `<ul class="related-list">` pointing to the **same three** posts. Result: three posts hoard inbound links (`ai-dev-workflow` 18, `claude-memory` 16, `gpt-5-5` 16) while **13 posts get zero**. Recommended fix: replace the static block with 3 topically-chosen links per post, so link equity is distributed and the "related" links are genuinely related.

## Orphan Pages (0 inbound internal links) + suggested sources
| Orphan | Suggested inbound links from |
|--------|------------------------------|
| microvm-sandbox-options-... | multi-agent-orchestration-frameworks-compared, ai-dev-workflow-frameworks, github-copilot-vs-claude-code-vs-cursor |
| multi-agent-orchestration-frameworks-compared | ai-dev-workflow-frameworks, gpt-5-5-autonomous-task-completion, microvm-sandbox-options |
| rag-vs-graphrag | claude-memory-dream-enterprise-agents, enterprise-ai-adoption-reality-check |
| copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | github-copilot-vs-claude-code-vs-cursor, microsoft-foundry-deep-dive |
| microsoft-foundry-deep-dive | copilot-studio-vs-azure..., enterprise-ai-adoption-reality-check |
| enterprise-ai-adoption-reality-check-2026 | generative-ai-adoption-by-industry, global-ai-adoption-attitudes |
| generative-ai-adoption-by-industry | enterprise-ai-adoption-reality-check, global-ai-adoption-attitudes |
| global-ai-adoption-attitudes | enterprise-ai-adoption-reality-check, generative-ai-adoption-by-industry |
| top-10-uk-ai-companies | uk-government-ai-institutes, uk-sovereign-ai-programme, uk-ai-skills-gap |
| uk-government-ai-institutes | uk-sovereign-ai-programme, top-10-uk-ai-companies |
| uk-sovereign-ai-programme | uk-government-ai-institutes, uk-ai-regulation-ico-employment, top-10-uk-ai-companies |
| uk-ai-skills-gap-education-opportunity | uk-government-ai-institutes, top-10-uk-ai-companies |
| claude-mythos-anthropic-opportunity-for-companies | claude-memory-dream-enterprise-agents, gpt-5-5-autonomous-task-completion |

## Dead-End Pages (0 outbound internal links)
| Post | Fix |
|------|-----|
| microvm-sandbox-options-... | Add a Related-posts block linking to multi-agent-orchestration, ai-dev-workflow-frameworks, github-copilot-vs-claude. (It was published today with no related-list at all.) |

## Topic Cannibalization
| Cluster | Competing posts | Recommendation |
|---------|-----------------|----------------|
| "AI adoption" | enterprise-ai-adoption-reality-check-2026, generative-ai-adoption-by-industry, global-ai-adoption-attitudes | Differentiate: make intents explicit (enterprise reality-check vs by-industry breakdown vs global attitudes) and cross-link as a cluster rather than compete. |

Note: the five `uk-*` posts are NOT cannibalizing — they cover distinct intents (institutes, sovereign programme, regulation, skills, companies). Treat them as a **topic cluster** and interlink them.

## Meta Descriptions Over 180 Characters (trim to 150–160)
| Post | Length |
|------|--------|
| ai-agent-interoperability-a2a-protocol | 233 |
| uk-ai-regulation-ico-employment-2026 | 231 |
| github-copilot-vs-claude-code-vs-cursor | 223 |
| multi-agent-orchestration-frameworks-compared | 220 |
| gpt-5-5-autonomous-task-completion | 214 |
| enterprise-ai-adoption-reality-check-2026 | 206 |
| claude-memory-dream-enterprise-agents | 204 |
| uk-sovereign-ai-programme | 198 |
| copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | 197 |
| microvm-sandbox-options-firecracker-opensandbox-smolvm-nono | 183 |

## Stale Content (>90 days since publish)
| Post | Published | Days | Priority | Refresh effort |
|------|-----------|------|----------|----------------|
| the-rise-of-ai-in-web-development | 2025-11-12 | 230 | High | Moderate (refresh stats + links) |
| generative-ai-adoption-by-industry | 2026-01-22 | 159 | Medium | Light (verify stats + links) |
| uk-government-ai-institutes | 2026-02-10 | 140 | Medium | Light (verify stats + links) |
| microsoft-foundry-deep-dive | 2026-02-18 | 132 | Medium | Light (verify stats + links) |
| uk-ai-skills-gap-education-opportunity | 2026-03-14 | 108 | Medium | Light (verify stats + links) |

## AI-Citation (GEO) Gaps
- **FAQPage schema present on only 4 of 20 posts** (copilot-studio, github-copilot, multi-agent, top-10-uk). Adding FAQ schema to research-heavy posts improves eligibility for AI Overviews / ChatGPT citation. Run `/blog-geo <file>` on priority posts.
- Several research-heavy posts name sources in prose but include **zero outbound links** (e.g. the new microVM post cites Firecracker docs, Docker's blog and the OpenSandbox repo without linking them). Linking named sources strengthens E-E-A-T and citability.

## Recommended Next Steps
1. **Replace the static Related-posts block** with per-post topical links (fixes 13 orphans + 1 dead-end at once). Highest leverage.
2. Add a Related-posts block to **microvm-sandbox-options** (currently orphan + dead-end).
3. Expand or merge **the-rise-of-ai-in-web-development** (463 words — thinnest post, lowest score 63).
4. Trim the 8 over-long meta descriptions to 150–160 characters.
5. Refresh **the-rise-of-ai-in-web-development** (230 days) and the 4 medium-stale posts.
6. Run `/blog-analyze the-rise-of-ai-in-web-development/index.html` for a deep score on the weakest post, and `/blog-geo` on the top research posts.

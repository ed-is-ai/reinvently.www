# Blog Audit Report

**Audit date:** 19 July 2026
**Total posts:** 26
**Average score:** 77 / 100
**Method:** Deterministic structural pass (schema parse via JSON-LD, link graph, meta lengths, og:image values) plus five parallel agents covering content quality, link health, schema/freshness, and cannibalization. Scored on 25/20/20/15/20 (content / SEO / E-E-A-T / technical / AI citation).

> **Scale note:** these are 100-point scores and are **not comparable** to the 18 July 60-point audit or the 3 July 100-point one. The previous report is preserved in git history (`git show HEAD:blog-audit-report.md`).

## Progress since 18 July

Two of yesterday's priorities are **done**, verified directly:

| Yesterday's finding | Status |
|---|---|
| 19 posts declaring `author: Organization` | **Fixed** — all 26 now `Person \| Ed Yau`, `worksFor: Kerv` |
| 13 posts with no visible byline | **Fixed** — 0 posts missing a byline |
| P0: "Claude ~40% of US enterprise AI spend" | **Removed** |

Five of the seven P0 statistics remain live, including the most conspicuous one — see P0 below.

## Health overview

| Metric | Count |
|---|---|
| Posts scoring 90+ (excellent) | 0 |
| Posts scoring 70–89 (good) | 21 |
| Posts scoring 50–69 (needs work) | 5 |
| Posts scoring under 50 (poor) | 0 |
| Orphan pages | 0 |
| Dead-end pages | 0 |
| Broken internal links | 0 |
| Cannibalization issues | 5 (1 high) |
| Stale by `dateModified` | 0 (but see Freshness) |

The corpus is structurally healthy and editorially uneven. Nothing is broken; nothing is excellent. The gap between the median post and the best is almost entirely **sourcing** — the top scorers cite primary research, the bottom five assert numbers.

## P0 — unsourced statistics still live

Carried forward from 18 July. Each is a precise number stated as fact with no citation, and in most cases carried into schema or meta where it becomes quotable.

| Post | Claim | Status |
|---|---|---|
| enterprise-ai-adoption-reality-check-2026 | "OpenAI raised $122 billion" — link points at openai.com homepage, not a source | **Still live.** An order of magnitude above any precedent |
| uk-sovereign-ai-programme | "Five companies control 70 percent of global AI compute" (8 occurrences) | **Still live**, still carried in meta/og/FAQ schema |
| ai-dev-workflow-frameworks-… | "our benchmarking": 31,600 tokens/run, $800–2,000/dev/month, 12 min vs 5.5 hrs | **Still live.** Your strongest original-data asset, unusable with no harness, model or date stated |
| top-10-uk-ai-companies | Stable Diffusion attributed to UK lineage | **Still live.** Appears factually wrong (CompVis / LMU Munich) |
| uk-ai-skills-gap-education-opportunity | 73%, 21%, £400bn, £27m, £187m, 10 million by 2030 | **Still live.** Every headline number in a stats-led post is uncited |

Newly surfaced in this pass:

| Post | Claim |
|---|---|
| claude-memory-dream-enterprise-agents | 97% error-reduction headline + Wisedocs/Harvey figures — vendor numbers, links resolve to company homepages |
| generative-ai-adoption-by-industry | $3.70 ROI, 36.8% CAGR, 26%/95% legal, six charity stats — all named surveys, none linked. Body "more than 90%" contradicts FAQ "92 percent" |
| global-ai-adoption-attitudes | "73% of UK adults", "$100 billion in 2024", "$40bn PIF" — all bare. Post-meta date (13 Feb) contradicts schema `datePublished` (20 Apr) |
| microvm-sandbox-options | "10 to 30 percent overhead", the Docker security quote, the Matt Pocock quote — all uncited |

## P1 — sitewide, fix once

Verified directly rather than agent-reported:

1. **`og:image` is the generic `/images/hero.jpg` on 24 of 26 posts** despite the recent commit adding bespoke per-post heroes. The heroes render in-body but the social meta was never repointed, so every share, Slack unfurl and AI preview card shows the same image. Highest-leverage single fix in this audit, and it makes work you have already paid for actually visible.
2. **`mainEntityOfPage` missing from 24 of 26** BlogPosting blocks. Templated one-line fix.
3. **Nav is split 19/7.** Nineteen posts use Home/News/Guides/About/Contact; seven newer ones use Home/Blog/About — which drops the `/contact/` link those posts' own CTAs depend on. That silently breaks the blog-signup CTA on seven posts.
4. **`dateModified` is uniform.** The 1–2 July batch edit reset all 26 to the same date, so freshness now carries no signal: a Nov 2025 post looks as current as last week's.
5. **Hero `<img>` lacks `width`/`height`, `srcset`, `fetchpriority="high"`.** LCP and CLS both suffer. (Correctly not lazy-loaded.)

**Deploy risk:** `tools/ed-o-meter/` is listed in `sitemap.xml` and exists on disk but is **untracked in git**. Ships a 404 unless committed.

## Per-post scores

| Post | /100 | Content /25 | SEO /20 | E-E-A-T /20 | Tech /15 | AI cite /20 |
|---|---|---|---|---|---|---|
| microvm-sandbox-options-firecracker-… | 89 | 23 | 18 | 17 | 12 | 19 |
| multi-agent-orchestration-frameworks-compared | 89 | 22 | 18 | 17 | 13 | 19 |
| building-the-ed-o-meter-llm-eval-harness | 87 | 22 | 16 | 19 | 13 | 17 |
| glm-5-2-fable-5-gpt-5-5-eval-results | 86 | 23 | 15 | 19 | 12 | 17 |
| ai-agent-governance-gap | 86 | 21 | 17 | 18 | 13 | 17 |
| uk-ai-regulation-ico-employment-2026 | 86 | 20 | 18 | 17 | 13 | 18 |
| uk-government-ai-institutes | 83 | 20 | 17 | 15 | 13 | 18 |
| uk-sovereign-ai-programme | 83 | 19 | 17 | 16 | 13 | 18 |
| glm-5-2-vs-claude-opus-vs-gpt-5-5-coding | 82 | 21 | 16 | 17 | 12 | 16 |
| github-copilot-vs-claude-code-vs-cursor | 80 | 21 | 17 | 14 | 12 | 16 |
| uk-ai-growth-labs-regulatory-sandboxes | 80 | 18 | 17 | 15 | 12 | 18 |
| top-10-uk-ai-companies | 79 | 20 | 17 | 11 | 13 | 18 |
| uk-ai-policy-landscape-enterprise-2026 | 79 | 18 | 18 | 13 | 12 | 18 |
| the-rise-of-ai-in-web-development | 77 | 17 | 16 | 15 | 13 | 16 |
| uk-ai-skills-gap-education-opportunity | 77 | 17 | 16 | 14 | 13 | 17 |
| enterprise-ai-adoption-reality-check-2026 | 77 | 19 | 16 | 15 | 11 | 16 |
| microsoft-foundry-deep-dive | 76 | 19 | 16 | 11 | 13 | 17 |
| rag-vs-graphrag | 75 | 17 | 16 | 12 | 13 | 17 |
| ai-dev-workflow-frameworks-gsd-bmad-… | 73 | 20 | 16 | 12 | 10 | 15 |
| gpt-5-5-autonomous-task-completion | 73 | 17 | 15 | 13 | 12 | 16 |
| ai-agent-interoperability-a2a-protocol | 70 | 17 | 15 | 12 | 11 | 15 |
| generative-ai-adoption-by-industry | 67 | 18 | 15 | 9 | 11 | 14 |
| copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock | 65 | 16 | 14 | 10 | 11 | 14 |
| claude-memory-dream-enterprise-agents | 65 | 16 | 14 | 10 | 11 | 14 |
| global-ai-adoption-attitudes | 60 | 16 | 13 | 8 | 10 | 13 |
| claude-mythos-anthropic-opportunity-for-companies | 58 | 13 | 13 | 9 | 10 | 13 |

## Prioritized action queue

| # | Action | Scope | Effort |
|---|---|---|---|
| 1 | Repoint `og:image` to each post's committed hero | 24 posts | 30 min, mechanical |
| 2 | Commit `tools/ed-o-meter/` before next deploy | 1 dir | 5 min |
| 3 | Cite or cut the five remaining P0 statistics | 5 posts | 2–3 hrs |
| 4 | Add `mainEntityOfPage` to schema | 24 posts | 20 min, mechanical |
| 5 | Reconcile nav to one variant; restore `/contact/` | 7 posts | 30 min |
| 6 | Resolve the GLM title/slug collision | 2 posts | 1 hr |
| 7 | Rewrite or retire `claude-mythos` (58) | 1 post | 3–4 hrs |
| 8 | Source `global-ai-adoption-attitudes`; fix date mismatch | 1 post | 3 hrs |
| 9 | Refresh model catalogues in the vendor-comparison posts | 3 posts | 2 hrs |
| 10 | Reconcile `uk-ai-skills-gap` FAQ ↔ JSON-LD mismatch | 1 post | 15 min |
| 11 | Split the seven 150w+ paragraphs in microvm | 1 post | 45 min |

## Topic cannibalization

Yesterday's audit found no true cannibalization. This pass agrees **on content** but flags a **title-level** collision that yesterday's intent-based reading missed:

| Severity | Keyword | Posts | Recommendation |
|---|---|---|---|
| **High** | glm-5.2 vs fable 5 vs gpt-5.5 | glm-5-2-fable-5-gpt-5-5-eval-results, glm-5-2-vs-claude-opus-vs-gpt-5-5-coding | Retitle the `-coding` post |
| Med | microsoft foundry | microsoft-foundry-deep-dive, copilot-studio-vs-… | Compress Foundry section in the comparison; link to the deep dive |
| Med | ai adoption statistics 2026 | enterprise-ai-adoption-reality-check, generative-ai-adoption-by-industry | Make the industry post strictly sector-vertical |
| Med | llm eval harness | building-the-ed-o-meter, glm-5-2-…-eval-results | Methodology in the build post; scores in results |
| Low-Med | uk ai policy 2026 | uk-ai-policy-landscape (hub) + 3 spokes | Cap pillar sections at ~150 words + link out |

**On the high-severity one:** the two posts *are* complementary in intent, as yesterday concluded — argument vs data. The problem is presentational. The titles differ only by "Our 28-Task Eval Results" vs "for Enterprise Coding" and name the same three models in the same order, so Google will collapse them and pick one. Compounding it, the `-coding` slug still says `claude-opus` while the content says Fable 5 — that URL costs you the term either way. Fixing the title and slug resolves this without touching the content split.

**Explicitly not conflicts:** the AI coding trio (products vs models vs process frameworks), the four-post agents cluster, and the UK institutes / skills-gap / companies set all target distinct intents. Leave them.

## Link graph

Clean, and better than yesterday. No orphans, no dead-ends, no broken links. All 26 posts are in `sitemap.xml` and every sitemap URL exists on disk. The two deleted posts (`glm-5-2-china-data-residency-…`, `open-weight-frontier-models-…`) have **zero remaining references** anywhere in the repo — that cleanup is complete.

Two posts sit at the bottom of the connectivity range (3 inbound / 2 outbound), linked only by each other and one shared neighbour. Both are the newest, so this is expected rather than wrong:

| Post | In/Out | Suggested additional linkers |
|---|---|---|
| building-the-ed-o-meter-llm-eval-harness | 3/2 | github-copilot-vs-claude-code-vs-cursor, ai-dev-workflow-frameworks, multi-agent-orchestration |
| glm-5-2-fable-5-gpt-5-5-eval-results | 3/2 | gpt-5-5-autonomous-task-completion, enterprise-ai-adoption-reality-check, copilot-studio-vs-… |

*Caveat: extraction was regex over `href` attributes; JS-built navigation would not appear.*

## Schema

All 26 have valid, parsing BlogPosting JSON-LD with the Person/Kerv byline migration now complete. Remaining gaps:

| Issue | Posts |
|---|---|
| Missing `mainEntityOfPage` | 24 of 26 |
| Missing schema `image` | ai-dev-workflow-frameworks, microvm-sandbox-options |
| Missing FAQPage | glm-5-2-fable-5-gpt-5-5-eval-results (still — carried from 18 July) |
| FAQ schema with no matching body content | building-the-ed-o-meter (5 Q&As declared, none rendered; Google treats schema-only FAQ as invalid) |
| FAQ body ↔ JSON-LD mismatch | uk-ai-skills-gap (HTML says £27m, JSON-LD omits it) |
| Title over 60 chars | multi-agent-orchestration (117), uk-ai-regulation-ico (105), microvm (101), ai-dev-workflow (97) |
| Meta description over 160 | uk-ai-skills-gap (170) |

Clean: zero images missing alt text across all 26; twitter:card present everywhere.

## Freshness

No post is stale by `dateModified` — but that is an artefact of the 1–2 July batch edit, not a health signal. Ranked by publication date and actual content staleness instead:

| Post | Published | Real staleness |
|---|---|---|
| the-rise-of-ai-in-web-development | 2025-11-12 | High — broadest topic, shortest post (~1,150w), reads as a stub |
| generative-ai-adoption-by-industry | 2026-01-22 | High — 2026 stats, no links |
| uk-government-ai-institutes | 2026-02-10 | Medium — only 2 external citations across ~2,400w |
| microsoft-foundry-deep-dive | 2026-02-18 | High — GPT-4o/o3 as current catalogue, inconsistent with your own 2026 posts |
| uk-ai-skills-gap-education-opportunity | 2026-03-14 | Medium — FAQ mismatch |
| copilot-studio-vs-… | 2026-04-05 | Medium — stale model names; body says "Microsoft Foundry" while title/URL say "Azure AI Foundry" |

## Prose and house style

First-order blocklist is largely clean — no "delve", "tapestry", "seamless", "in conclusion". Two literal hits: "Before diving into sectors" (generative-ai, line 116) and "cutting-edge technologies" (uk-sovereign, line 119).

The **structural** tells are the real problem:

- **"X is not Y. It is Z."** closing construction — claude-memory, claude-mythos, a2a-protocol, copilot-studio, generative-ai. The strongest single signature site-wide.
- **Symmetric list bloat** — multi-agent's five identically-skeletoned subsections; generative-ai's per-sector and global-ai's per-country "What is working / Tensions and risks" scaffolding.
- **Numbered capsule headings** — "Development 1/2/3" (uk-ai-regulation, also keyword-dead), "1.–6." (microsoft-foundry).
- **Question-cadence H3s** — gpt-5-5 governance section is 4/4 questions.
- **Bolded lead-in runs** — gpt-5-5 lines 118–124 (four consecutive).
- **Intensifier crutches** — "significant(ly)" 11× in claude-memory, 9× in claude-mythos; "genuinely" 4–5× each in gpt-5-5, top-10-uk, uk-government-ai-institutes.
- **Epigram overrun** (house cap 1–2) — the-rise-of-ai repeats "AI compresses production. It does not compress judgement." three times (body, closing, FAQ).

**Paragraphs over 150 words:** 25 across the corpus. Worst concentration is microvm-sandbox with seven (lines 194 and 200 at ~215w each).

## Notes on two posts

**claude-mythos (58/100)** — now the weakest on the site. ~950 words, almost entirely assertion, four numbered sections of pure speculation with no falsifiable content, and "thousands of high-severity vulnerabilities" carrying no link to primary research. An April post about an unreleased model with a July `dateModified` and no revision note. Recommend rewrite or retire rather than a fix pass.

**glm-5-2-fable-5-gpt-5-5-eval-results (86/100)** — strongest E-E-A-T on the site alongside the Ed-o-meter build post, on the strength of original data. Still the only post with no FAQPage schema despite heavily Q&A-shaped content, and related links elsewhere on the site refer to it by a headline that differs from its actual H1 — inconsistent entity naming works against exactly the AI-citation surface this post is best positioned to win.

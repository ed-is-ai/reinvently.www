## Context

Reinvently is a static HTML site. Guide articles are hand-authored HTML pages physically located at `blog/<slug>/index.html`, sharing `blog/blog.css`, a standard nav/footer, GA snippet, and `BlogPosting`(+often `FAQPage`) JSON-LD. They are surfaced as post-cards on multiple index pages. There is no build step or CMS — pages are edited directly and committed.

The content for this guide is already researched and captured in `guides/multi-agent-orchestration-frameworks-compared/OUTLINE.md` (landscape-map framing; verified GitHub data; cited community feedback). What remains is turning the outline into a publish-ready HTML article and wiring it into the site's listings.

An existing guide slug (e.g. `github-copilot-vs-claude-code-vs-cursor`) is referenced in: `blog/<slug>/index.html` (the article), `blog/index.html` (blog hub), `guides/index.html` (guides index), `index.html` (homepage), and `sitemap.xml`. The new article must be wired into the same surfaces.

## Goals / Non-Goals

**Goals:**
- Publish a credible, EEAT-strong comparison guide that matches the house template and SEO conventions.
- Organise the five tools by category (landscape map), and present popularity honestly using recent-vs-lifetime star velocity.
- Make the article discoverable everywhere existing guides appear (guides index, blog hub, homepage if applicable, sitemap).

**Non-Goals:**
- No independent benchmarking or hands-on testing of the five tools — we report verified GitHub metrics and cited third-party feedback only.
- No live/auto-updating star counts — figures are a point-in-time snapshot labelled with a verification date.
- No new build tooling, components, or dependencies; no interactive widgets.
- No changes to the five upstream projects or any backend.

## Decisions

**1. Article lives at `blog/multi-agent-orchestration-frameworks-compared/index.html`, not under `guides/`.**
Rationale: every existing guide article physically lives under `/blog/<slug>/` and the `/guides/` index merely links to those URLs (confirmed in `guides-section` spec and `guides/index.html`). Following the convention keeps URL structure, related-post links, and SEO consistent. Alternative (publish under `/guides/<slug>/`) rejected: it would diverge from all 7 existing guides and the guides-section spec.

**2. Slug = `multi-agent-orchestration-frameworks-compared`.**
Descriptive and category-accurate. A `ruflo-vs-aperant-vs-...` slug was rejected as unwieldy for five tools and because one (Aperant) is positioned as a cautionary tale rather than a co-equal contender.

**3. Hand-author HTML by copying an existing comparison post as the template.**
Use `blog/copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock/index.html` (or the closest current comparison guide) as the structural template — same `<head>` metadata block, JSON-LD shape, nav/footer, and `blog.css` classes — then replace content. Ensures visual/SEO parity with no new patterns.

**4. Structured data: `BlogPosting` + `FAQPage` JSON-LD.**
Author = Reinvently (Organization), `inLanguage` en-GB, `datePublished` = publish date, `dateModified` = same initially. The `FAQPage` block is generated from the final visible FAQ section so the two cannot drift.

**5. Honesty / freshness handling for time-sensitive data.**
Include an in-article "GitHub data verified as of <date>" note next to the metrics, attribute every reliability/experience claim to a named source with a link, and state ruflo's criticisms and Aperant's stall factually. This protects EEAT and fairness. Star counts and community links are re-confirmed immediately before publish (they drift fast — ruflo is climbing ~hundreds/day).

**6. Listing surfaces updated, newest-first.**
Add a post-card to `guides/index.html` and `blog/index.html`, add the URL to `sitemap.xml`, and add a homepage card to `index.html` only if the homepage currently features latest guide/blog posts (verify before editing). Each insertion goes at the top of its list to preserve newest-first ordering.

**7. Drafting via the writing skill, then wrapped in the template.**
Prose is drafted from `OUTLINE.md` using the project's blog/guides writer skill, then placed into the HTML template (Decision 3). The outline is the single source of structure and verified facts.

**8. `OUTLINE.md` is a planning artifact, not a published page.**
It will be left as a working reference. Optionally relocate it into the change directory to avoid a stray `/guides/multi-agent-orchestration-frameworks-compared/` path with no `index.html`; treated as a minor cleanup task, not a blocker.

## Risks / Trade-offs

- **Time-sensitive figures go stale (stars, velocity, "last commit").** → Re-verify via GitHub API at publish time; label metrics with a verification date; frame momentum qualitatively (accelerating / stalled) so small drift doesn't invalidate claims.
- **Fairness/reputation risk in calling ruflo unreliable and Aperant stalled.** → Attribute to identifiable sources (GitHub discussion #1666, Augment Code, commit history), use factual/measured language, link the evidence; avoid editorialising beyond what sources support.
- **FAQ JSON-LD drifting from visible FAQ.** → Author the visible FAQ first, then derive the JSON-LD from it; verify a 1:1 match before commit.
- **Missing a listing surface (article published but not discoverable, or sitemap omission).** → Use the existing-slug reference set (guides index, blog hub, homepage, sitemap) as a checklist; grep for the new slug across the repo after wiring to confirm all surfaces updated.
- **Licensing claims (AGPL vs MIT) or feature claims inaccurate.** → Cross-check each against the repo's actual `license` field and README at publish time.

## Open Questions

- Does the homepage (`index.html`) currently surface latest guides/blog posts, and if so does it cap the count (i.e. does adding this one bump an older card off)? Resolve by inspecting `index.html` during implementation.
- Should `OUTLINE.md` be relocated into the change directory or deleted after publish? Default: leave it; revisit at archive time.
- Publish date to stamp in JSON-LD — use actual publish day (decide at apply time).

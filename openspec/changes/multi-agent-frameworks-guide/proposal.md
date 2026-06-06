## Why

Developers are evaluating a wave of "multi-agent" orchestration tools, but the label hides four very different product shapes (library, desktop coding orchestrator, fleet-ops dashboard, swarm meta-harness) — so naive comparisons mislead. Reinvently has an established niche of practical, EEAT-strong comparison guides (e.g. Copilot vs Claude Code vs Cursor); a well-researched, honestly-framed guide on multi-agent frameworks fills a current content gap and captures high-intent "X vs Y" search traffic. Research is already done and captured in the outline.

## What Changes

- Add a new long-form technical guide article comparing five multi-agent orchestration projects: **ruflo, Aperant, sandcastle, mission-control, Maestro**.
- Frame it as a **landscape map by category** (not a flat ranking), with the through-line "**stars ≠ usefulness**" — backed by verified GitHub data (recent vs lifetime star velocity) and cited community feedback.
- Publish the article HTML at `blog/multi-agent-orchestration-frameworks-compared/index.html` (matching the existing guide convention where guide articles live under `/blog/<slug>/`).
- Surface the article as a post-card on the `/guides/` index page (newest-first), and on the blog hub index if guides appear there.
- Include correct on-page SEO and structured data (BlogPosting + FAQPage JSON-LD), matching the house style of existing comparison posts.

## Capabilities

### New Capabilities
- `multi-agent-frameworks-guide`: A published guide article at `blog/multi-agent-orchestration-frameworks-compared/` that compares the five frameworks across popularity, use cases, differentiators, hosting, and community verdict — with verified data, a landscape-map structure, FAQ, and valid SEO/structured-data metadata, discoverable from the `/guides/` index.

### Modified Capabilities
<!-- None. The existing `guides-section` requirement ("list all articles classified as Guides, newest-first") already covers surfacing this new article; adding its post-card is implementation, not a requirement change. -->

## Impact

- **New file**: `blog/multi-agent-orchestration-frameworks-compared/index.html` (the article).
- **Edited file**: `guides/index.html` (new post-card, newest-first).
- **Possibly edited**: blog hub index (`blog/index.html` or equivalent) and `sitemap.xml` if present, to include the new URL.
- **Planning note**: `guides/multi-agent-orchestration-frameworks-compared/OUTLINE.md` is the source outline (working doc); the article slug differs from its current folder location and the published HTML lives under `blog/` per convention.
- **No code/runtime impact**: static HTML/CSS only; reuses `blog/blog.css`, existing nav/footer, and GA snippet. No new dependencies.
- **External data**: star counts and community-feedback links are time-sensitive and should be re-confirmed at draft/publish time.

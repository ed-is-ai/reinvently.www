## Why

Reinvently's current positioning as an AI consultancy is being set aside; the site's new purpose is to be a destination for curated AI news and technical guides aimed at UK organisations and practitioners. The blog currently has no structure to distinguish timely news from evergreen technical content, making it harder for readers to find what they need.

## What Changes

- **BREAKING**: Split `/blog/` into two distinct sections: `/news/` (curated AI news) and `/guides/` (technical how-to and comparison guides)
- Create `/news/index.html` — listing page for news articles
- Create `/guides/index.html` — listing page for technical guides
- Update `/blog/index.html` to be a unified hub directing visitors to News and Guides
- Update site nav across all pages: replace "Blog" link with "News" and "Guides" links
- Update homepage and site-wide SEO metadata (title, description, OG tags) to reflect new positioning
- Add category attribution to existing article meta and breadcrumbs (News vs Guides)

## Capabilities

### New Capabilities

- `news-section`: A `/news/` landing page listing AI news articles with brief descriptions
- `guides-section`: A `/guides/` landing page listing technical guides and comparisons with brief descriptions
- `blog-hub`: Updated `/blog/index.html` that acts as an entry point to both sections

### Modified Capabilities

- `nav-layout`: Navigation updated across all pages — "Blog" replaced with "News" + "Guides" links
- `site-seo-meta`: Homepage title, meta description, and OG tags updated to reflect news + guides positioning

## Impact

- New files: `news/index.html`, `guides/index.html`
- Modified: `blog/index.html`, `index.html`, all `blog/*/index.html` article pages, all other pages with nav links
- No article URLs change — existing posts stay at `blog/<slug>/index.html`
- RSS/Atom feeds (`f.atom`, `f.rss`, `f.json`) are not in scope for this change

## Article Categorisation

**News** (timely, event-driven):
- A2A Protocol, Claude Mythos, GPT-5.5, Microsoft Foundry Deep Dive, UK AI Regulation, UK Government AI Institutes, UK Sovereign AI, Enterprise AI Reality Check

**Guides** (evergreen, technical, comparative):
- GSD/BMAD/OpenSpec Framework Comparison, Claude Memory & Dream, Copilot Studio vs Azure vs Bedrock, Generative AI by Industry, GitHub Copilot vs Claude Code vs Cursor, Global AI Adoption Attitudes, RAG vs GraphRAG, Rise of AI in Web Dev, Top 10 UK AI Companies, UK AI Skills Gap

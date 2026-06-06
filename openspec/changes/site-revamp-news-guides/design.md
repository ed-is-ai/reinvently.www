## Context

The site has 18 hand-crafted blog articles under `blog/<slug>/index.html` with a unified index at `blog/index.html`. The blog index already has JavaScript filter buttons (Enterprise Adoption, Technology Strategy, UK AI News) using `data-tags` on each card. All pages share `blog/blog.css`. The homepage is GoDaddy-generated minified HTML with a separate custom `<nav>` injected above the GoDaddy block. Article URLs are established and must not change.

## Goals / Non-Goals

**Goals:**
- Create `/news/` and `/guides/` as first-class section landing pages
- Update `/blog/index.html` to be a hub page linking to both sections
- Replace the "Blog" nav link with "News" and "Guides" across all pages
- Update homepage SEO metadata to reflect news + guides positioning
- Update article breadcrumbs to reflect their section (News or Guides)

**Non-Goals:**
- Moving articles — all posts stay at `blog/<slug>/index.html`
- Redesigning the visual style — reuse existing `blog.css` and card patterns
- Automating the RSS/Atom feeds or adding a CMS
- Updating the GoDaddy homepage widget content (too risky to edit minified HTML beyond the nav)

## Decisions

**Reuse `blog.css` for section pages via `../blog/blog.css`**
`news/index.html` and `guides/index.html` sit one directory below root; `../blog/blog.css` resolves correctly from there — same pattern the service pages already use for `../blog/blog.css`. No new CSS files needed.

**`/blog/` becomes a hub, not a redirect**
Keeping `blog/index.html` as a discovery hub (showing both sections) preserves any inbound links to `/blog/` and keeps the existing RSS feed link valid. A 301 redirect was considered but would break the feed `<link rel="alternate">` references in the HTML.

**Static article listing in section pages**
Section pages are static HTML listing the articles in each category — same card pattern as `blog/index.html`. No JS filter bar needed since each page is already scoped to one category. This is the simplest pattern consistent with the existing site.

**Article categorisation** (drives breadcrumb updates and section page listings):

| Section | Articles |
|---|---|
| **News** | A2A Protocol, GPT-5.5, UK AI Regulation, Enterprise AI Reality Check, UK Sovereign AI, Claude Mythos, Top 10 UK AI Companies, UK Government AI Institutes, UK AI Skills Gap, Global AI Adoption Attitudes |
| **Guides** | GSD/BMAD/OpenSpec/Spec Kit, Claude Memory & Dream, Copilot Studio vs Azure vs Bedrock, GitHub Copilot vs Claude Code vs Cursor, RAG vs GraphRAG, Rise of AI in Web Dev, Microsoft Foundry Deep Dive, Generative AI by Industry |

## Risks / Trade-offs

- **Blog breadcrumbs in article pages reference old category labels** → Update `post-meta` breadcrumb in each article from `Blog` to `News` or `Guides`
- **Nav link count increases** → Two links ("News" + "Guides") replace one ("Blog") — adds one item; acceptable given the content split
- **Homepage meta is in minified GoDaddy HTML** → The homepage `<meta>` tags in the `<head>` are inside the readable section before the minified GoDaddy block; they can be edited safely

## Migration Plan

1. Create `news/index.html` (news section landing page)
2. Create `guides/index.html` (guides section landing page)
3. Update `blog/index.html` — replace filter UI with two-section hub layout
4. Update nav in all pages — add News + Guides, remove Blog
5. Update homepage `<meta>` title and description
6. Update article breadcrumbs (`post-meta` line in each article's `<header>`)
7. Commit and push

Rollback: revert the commit.

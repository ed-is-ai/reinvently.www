## 1. Create News section landing page

- [ ] 1.1 Create `news/index.html` — listing page for all 10 news articles (A2A Protocol, GPT-5.5, UK AI Regulation, Enterprise AI Reality Check, UK Sovereign AI, Claude Mythos, Top 10 UK AI Companies, UK Government AI Institutes, UK AI Skills Gap, Global AI Adoption Attitudes), reusing `../blog/blog.css`, with correct SEO meta and `aria-current="page"` on the News nav link

## 2. Create Guides section landing page

- [ ] 2.1 Create `guides/index.html` — listing page for all 8 guide articles (GSD/BMAD/OpenSpec/Spec Kit, Claude Memory & Dream, Copilot Studio vs Azure vs Bedrock, GitHub Copilot vs Claude Code vs Cursor, RAG vs GraphRAG, Rise of AI in Web Dev, Microsoft Foundry Deep Dive, Generative AI by Industry), reusing `../blog/blog.css`, with correct SEO meta and `aria-current="page"` on the Guides nav link

## 3. Update blog index to hub page

- [ ] 3.1 Update `blog/index.html` — remove JS filter bar and filter buttons, add two-section hub layout with intro text and links to `/news/` and `/guides/`, retain feed `<link rel="alternate">` tags, update page title and description, update nav to News + Guides

## 4. Update site nav across all pages

- [ ] 4.1 Update nav in all `blog/*/index.html` article pages — replace `<a href="/blog/">Blog</a>` with `<a href="/news/">News</a>` and `<a href="/guides/">Guides</a>`
- [ ] 4.2 Update nav in `contact/index.html` — same nav change
- [ ] 4.3 Update nav in `index.html` (homepage) — same nav change

## 5. Update homepage SEO metadata

- [ ] 5.1 Update `index.html` `<title>`, `<meta name="description">`, `og:title`, `og:description`, `twitter:title`, `twitter:description` to reflect Reinvently as a curated AI news + technical guides destination

## 6. Update article breadcrumbs

- [ ] 6.1 Update breadcrumb `post-meta` line in all **News** articles to show "News" label and link to `/news/` (articles: A2A Protocol, GPT-5.5, UK AI Regulation, Enterprise AI Reality Check, UK Sovereign AI, Claude Mythos, Top 10 UK AI Companies, UK Government AI Institutes, UK AI Skills Gap, Global AI Adoption Attitudes)
- [ ] 6.2 Update breadcrumb `post-meta` line in all **Guides** articles to show "Guides" label and link to `/guides/` (articles: GSD/BMAD/OpenSpec/Spec Kit, Claude Memory & Dream, Copilot Studio vs Azure vs Bedrock, GitHub Copilot vs Claude Code vs Cursor, RAG vs GraphRAG, Rise of AI in Web Dev, Microsoft Foundry Deep Dive, Generative AI by Industry)

## 7. Verify and commit

- [ ] 7.1 Check no remaining `/blog/` nav links exist across the site
- [ ] 7.2 Commit and push changes

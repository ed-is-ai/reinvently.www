## 1. Pre-draft verification (refresh time-sensitive data)

- [x] 1.1 Re-confirm current star counts, forks, open issues, and `pushed_at` for all five repos via the GitHub API; note the verification date. (Verified 2026-06-06: ruflo 58,116; Aperant 14,325; sandcastle 5,771; mission-control 5,199; Maestro 2,984.)
- [x] 1.2 Re-confirm recent star velocity (recent vs lifetime) for each repo; re-check that Aperant is still stalled (no new commits) and ruflo still accelerating. (ruflo ~549/day recent vs 158 lifetime; Aperant ~5.5/day, last push 23 Mar = stalled; sandcastle ~26; mission-control ~20; Maestro ~4.)
- [x] 1.3 Re-verify each cited community-feedback link still resolves (ruflo discussion #1666, Augment Code, Hacker News Maestro threads, etc.); replace any dead links. (Confirmed resolving this session.)
- [x] 1.4 Cross-check each license claim (MIT/AGPL) and "requires Claude Pro/Max" / hosting claim against the repos' current metadata and READMEs. (ruflo/sandcastle/mission-control MIT; Aperant/Maestro AGPL-3.0; Aperant requires Claude Pro/Max.)
- [x] 1.5 Update `OUTLINE.md` with any corrected figures so it stays the single source of truth. (Figures already current as of 2026-06-06; no change needed.)

## 2. Draft the article content

- [x] 2.1 Draft the prose from `OUTLINE.md` using the project's blog/guides writer skill, in en-GB, following the landscape-map structure (intro → popularity → stars≠usefulness → category walkthroughs → hosting table → how-to-choose → FAQ → close).
- [x] 2.2 Ensure all five frameworks and all five angles (popularity, use cases, differentiators, hosting, community feedback) are covered (spec: compares the five frameworks across the five angles).
- [x] 2.3 Include the recent-vs-lifetime star velocity treatment and a visible "GitHub data verified as of <date>" note (spec: popularity distinguishes momentum from cumulative stars).
- [x] 2.4 Attribute every reliability/experience claim to a named, linked source; state ruflo's criticisms and Aperant's stall plainly (spec: evidence-based and honestly framed).
- [x] 2.5 Write the visible FAQ section (the questions that will back the FAQPage JSON-LD).

## 3. Build the article page

- [x] 3.1 Copy an existing comparison guide (e.g. `blog/copilot-studio-vs-azure-ai-foundry-vs-aws-bedrock/index.html`) as the structural template into `blog/multi-agent-orchestration-frameworks-compared/index.html`.
- [x] 3.2 Replace the body content with the drafted article; keep the shared nav, footer, `blog/blog.css` link, and GA snippet (spec: guide article page exists; uses en-GB).
- [x] 3.3 Fill the `<head>` SEO metadata: unique `<title>`, `<meta name="description">`, self-referential `<link rel="canonical">`, Open Graph + Twitter tags (spec: valid SEO metadata).
- [x] 3.4 Add the `BlogPosting` JSON-LD (author = Reinvently org, en-GB, datePublished/dateModified).
- [x] 3.5 Add the `FAQPage` JSON-LD generated from the visible FAQ; verify a 1:1 match with the on-page Q&A (spec: FAQ structured data matches visible content).

## 4. Wire into site listings (discoverability)

- [x] 4.1 Add a newest-first post-card for the article to `guides/index.html`, linking to `/blog/multi-agent-orchestration-frameworks-compared/` (spec: discoverable from Guides index).
- [x] 4.2 Add a newest-first post-card to the blog hub `blog/index.html`.
- [x] 4.3 Inspect `index.html` (homepage); if it features latest posts, add a card and trim to the existing cap if any (resolves design Open Question).
- [x] 4.4 Add the new URL to `sitemap.xml` with appropriate lastmod.

## 5. Verify

- [x] 5.1 Open the article locally and confirm it renders with correct chrome, styling, and no broken internal links/images.
- [x] 5.2 Validate both JSON-LD blocks (well-formed JSON; FAQ matches visible content).
- [x] 5.3 Grep the repo for the new slug to confirm every listing surface (guides index, blog hub, homepage if applicable, sitemap) references it.
- [x] 5.4 Proofread for en-GB spelling, factual accuracy of figures, and that all claims remain source-attributed.
- [x] 5.5 Decide `OUTLINE.md` fate (leave / relocate to change dir) and apply.

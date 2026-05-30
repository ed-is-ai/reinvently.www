# UI Review — reinvently.co.uk
**Audit date:** 30 May 2026
**Scope:** Blog system (blog.css + all post templates) + homepage blog grid
**Overall score:** 15 / 24

---

## Pillar 1: Copywriting — 2 / 4

### Critical

**Typo in production copy.**
`blog/claude-memory-dream-enterprise-agents/index.html` line 65:
> "Together they **relly** simplify work on enterprise-scale deployments."
`relly` → `really`. Fix immediately.

### Moderate

**"Read more" is a weak CTA label across all 18 post cards.**
Every card ends with the same generic "Read more". Since the card heading already describes the post, the CTA has no incremental value. Consider removing it entirely (the entire card is a link) or replacing it with a short, post-specific hook on key posts.

**Homepage tagline uses prohibited language.**
"Transforming Ideas into **Impactful** AI Solutions" — "impactful" is weak filler. The style guide flags similar terms. The tagline is locked in the GoDaddy builder; flag for next site rebuild.

### Minor

**Article summary/deck text is inconsistent in tone.**
Some summaries are active and specific ("AI funding hit $300 billion in Q1 2026…"); others are vague ("…the UK's AI ecosystem is deeper than most people realise"). The vague ones reduce click intent from the grid.

---

## Pillar 2: Visuals — 2 / 4

### Critical

**Every post uses the same OG image (`/images/hero.jpg`).**
All 18 posts share a single hero image. Social shares and AI answer previews show the same image regardless of post content. This is a significant missed differentiation opportunity and reduces social sharing effectiveness.

### Critical

**Post cards are text-only with no visual category differentiation.**
The blog grid is 18 identical dark rectangles. There is no visual cue to distinguish a UK policy post from a tool comparison or a company profile. Category colour dots, icon badges, or a left-border accent would make the grid scannable.

### Moderate

**No per-post featured image in article headers.**
The article header background is a flat `#161616` colour. A lightweight per-category illustration or header illustration would significantly raise perceived quality, particularly for comparison posts that are shared professionally.

---

## Pillar 3: Color — 3 / 4

The grayscale palette is intentional and executed consistently. No hue violations or inconsistent hex usage found.

### Moderate

**No semantic colour for category labels.**
"UK AI News", "Enterprise Adoption", and "Technology Strategy" all render in identical `rgb(150,150,150)` gray. A subtle hue per category (or even a single accent hue for one high-priority category) would aid scannability without breaking the aesthetic.

**`--accent` and `--text-muted` are the same value (`rgb(150,150,150)`).**
The CSS defines `--accent` separately but assigns it the same value as `--text-muted`. This means there is functionally no accent colour — all interactive affordances (hover states, links, read-more labels, card borders) use the same gray. The site lacks a focal colour.

### Minor

**Link colour barely distinguishes from surrounding body text.**
Inline links use `color:rgb(150,150,150);border-bottom:1px solid #1b1b1b` — the border is the same as the background, making it nearly invisible. The link colour is correct but the underline colour makes links harder to spot in dense paragraphs.

---

## Pillar 4: Typography — 3 / 4

Three-typeface system (Playfair Display / Source Sans Pro / Montserrat) is coherent and well-executed. Hierarchy is clear.

### Moderate

**H3 (21px) and H2 (28px) are too close in size.**
The 7px gap between H2 (28px) and H3 (21px) is tighter than the 12px gap between H1 (40px) and H2 (28px). Under a modular scale, H3 should be around 20px but the visual weight also needs supporting differentiation — consider adding `letter-spacing: 0.02em` or a slight colour shift for H3 to reinforce hierarchy.

**H2 in article body has no letter-spacing.**
Navigation labels and post-meta use `letter-spacing: 2px–4px` for typographic character. Article H2s (`font-family: var(--font-head)`) have none. Adding `letter-spacing: 0.01em` to `.article-body h2` would sharpen the editorial tone.

### Minor

**Bold weight (`font-weight: 700`) is not loaded for Source Sans Pro.**
The `@font-face` declarations only load Playfair Display (400 and 700) and Source Sans Pro (400 only). If any body text uses `font-weight: bold` it will fall back to system bold, which may differ from the intended weight. Verify no bold is used in article bodies.

---

## Pillar 5: Spacing — 3 / 4

Spacing is largely consistent and the 48px horizontal gutter is respected across nav, headers, and footer.

### Moderate

**No responsive breakpoint between 640px and 900px.**
The single breakpoint at 640px means tablets (641–900px) get desktop spacing (48px gutters, 40px H1) without the mobile adjustments. On a 768px tablet, the article header has 48px side padding with an H1 that can comfortably be 32–36px rather than 40px. A mid-range breakpoint at ~768px would improve tablet rendering.

**Article body (max-width: 720px) inside container (max-width: 900px) creates uneven negative space.**
The article body is 180px narrower than the `.container` it sits in, but the container has no visual treatment (no sidebar, no secondary content) to justify the extra space. On screens wider than 900px, the container centres correctly; but between 720–900px, the article feels narrowly placed with blank space to the right/left.

### Minor

**Inline table padding is inconsistent across posts.**
Tables in newer posts use `padding: 10px 14px`; tables in the Copilot/Antigravity post use `padding: 12px 16px`. All tables should use the blog.css default or a single documented value.

---

## Pillar 6: Experience Design — 2 / 4

### Critical

**Mobile navigation is completely hidden.**
`.nav-links { display: none }` at ≤640px. Mobile users see the Reinvently logo and nothing else. There is no hamburger menu, no visible nav. The logo links home but "Blog" is unreachable without typing the URL. This is a significant UX failure for mobile visitors landing on a post.

### Critical

**No related posts or reading continuation at article end.**
All posts end with `← All posts`. Users who finish an article have no guided path to continue — no related posts, no category links, no "you might also like". Exit rate at this point is likely near 100%.

### Moderate

**Category filter does not update the URL.**
The filter buttons on both blog index and homepage use client-side JS to show/hide cards. Filtered views (e.g., "show only UK AI News") are not bookmarkable or shareable — refreshing the page resets to "All". URL-based filtering (`/blog/?category=uk-ecosystem`) would fix this and also make category pages indexable.

**No keyboard focus styles.**
The CSS defines `:hover` states for nav links and filter buttons but no `:focus` or `:focus-visible` styles. Keyboard and screen reader navigation has no visible affordance.

**Feed discovery is invisible.**
Three feed formats exist (`f.atom`, `f.rss`, `f.json`) but there are no `<link rel="alternate">` tags in individual blog post heads, no visible RSS link, and no discovery from the blog index page. The feeds are unreachable without direct knowledge of the URLs.

### Minor

**No pagination or "load more" for the blog grid.**
18 posts currently renders fine. Beyond 30–40 posts, a single-page grid will affect initial load time and scrollability. Plan pagination before adding more posts.

**The back-link appears twice (top and bottom of article body) — this is intentional and correct.** ✓

---

## Top 5 Fixes (Priority Order)

1. **Fix "relly" typo** in claude-memory-dream post — 2-minute fix, production copy error.
2. **Add mobile navigation** — hidden nav is a functional failure on mobile (≈50% of traffic).
3. **Add related posts** at article end — highest impact on engagement and time-on-site.
4. **Differentiate OG images** per post (or at minimum per category) — directly affects social share quality.
5. **Add `:focus-visible` styles** to nav and filter buttons — accessibility baseline.

---

## Quick Wins (< 30 min total)

- Fix typo in claude-memory post
- Add `letter-spacing: 0.01em` to `.article-body h2` in blog.css
- Change inline link border-bottom colour from `#1b1b1b` to something slightly lighter (e.g., `#444`) to make links visible in article body
- Add `<link rel="alternate">` tags pointing to feeds in blog post `<head>` elements

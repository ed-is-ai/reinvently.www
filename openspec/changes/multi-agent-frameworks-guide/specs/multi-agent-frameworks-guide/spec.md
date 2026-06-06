## ADDED Requirements

### Requirement: Guide article page exists
A static HTML article SHALL exist at `blog/multi-agent-orchestration-frameworks-compared/index.html`, accessible at `https://reinvently.co.uk/blog/multi-agent-orchestration-frameworks-compared/`. It SHALL reuse the existing site chrome: the shared `blog/blog.css` stylesheet, the standard `<nav>` (Home / News / Guides / Contact) and `<footer>`, and the Google Analytics snippet — matching existing guide articles.

#### Scenario: Visitor opens the article
- **WHEN** a visitor navigates to `/blog/multi-agent-orchestration-frameworks-compared/`
- **THEN** they see the article rendered with the site nav, footer, and blog styling consistent with other guide posts

#### Scenario: Article uses British English
- **WHEN** the article copy is reviewed
- **THEN** it uses en-GB spelling and the `<html lang="en-GB">` attribute, consistent with the rest of the site

### Requirement: Article compares the five frameworks across the five angles
The article SHALL cover all five projects — ruflo, Aperant, sandcastle, mission-control, and Maestro — and SHALL address each of the five comparison angles: popularity (GitHub star trajectory), key use cases, differentiators, hosting requirements, and real-world community feedback.

#### Scenario: All frameworks and angles present
- **WHEN** a reader reads the article end-to-end
- **THEN** each of the five frameworks is described, and each of the five angles (popularity, use cases, differentiators, hosting, community feedback) is addressed for them

#### Scenario: Landscape-map framing, not a flat ranking
- **WHEN** a reader reaches the comparison
- **THEN** the tools are organised into their distinct categories (library / desktop coding orchestrator / fleet-ops dashboard / swarm meta-harness) rather than ranked on a single flat scale

### Requirement: Claims are evidence-based and honestly framed
The article SHALL present verified GitHub data (including recent star velocity versus lifetime average, not lifetime average alone) and SHALL attribute community-feedback claims to identifiable sources. It SHALL reflect the honest findings from research: that the most-starred tool (ruflo) draws significant reliability criticism, and that Aperant's development is stalled.

#### Scenario: Popularity section distinguishes momentum from cumulative stars
- **WHEN** a reader reads the popularity section
- **THEN** it shows recent star velocity alongside cumulative stars and explains that lifetime averages can mislead (e.g. Aperant's collapsed velocity)

#### Scenario: Community feedback is sourced
- **WHEN** a reader encounters a claim about real-world experience or reliability
- **THEN** it is attributable to a cited source (e.g. a GitHub discussion, Hacker News thread, or named article)

#### Scenario: Honest treatment of stalled or criticised tools
- **WHEN** a reader reads about ruflo and Aperant
- **THEN** ruflo's reliability criticisms and Aperant's stalled development are stated plainly rather than omitted

### Requirement: Article has valid SEO and structured-data metadata
The page SHALL include a descriptive `<title>`, `<meta name="description">`, a self-referential `<link rel="canonical">`, Open Graph and Twitter card tags, and two valid JSON-LD blocks: `BlogPosting` and `FAQPage` — matching the metadata pattern of existing comparison guides.

#### Scenario: Search engine crawls the article
- **WHEN** a search engine crawls the page
- **THEN** it finds a unique descriptive title and meta description, a canonical URL pointing to the article's own URL, and valid `BlogPosting` and `FAQPage` JSON-LD

#### Scenario: FAQ structured data matches visible content
- **WHEN** the `FAQPage` JSON-LD is compared to the on-page FAQ section
- **THEN** the questions and answers in the structured data match the questions and answers visible to readers

### Requirement: Article is discoverable from the Guides index
The article SHALL be listed on the `/guides/` index page as a post-card following the existing pattern (date, "Guide" category label, title, excerpt), inserted newest-first, and linking to the article's `/blog/<slug>/` URL.

#### Scenario: Guides index lists the new article
- **WHEN** a visitor views `/guides/`
- **THEN** a post-card for this article appears at the top of the list (newest-first) and links to `/blog/multi-agent-orchestration-frameworks-compared/`

## ADDED Requirements

### Requirement: Guides section landing page exists at /guides/
A static HTML page SHALL exist at `guides/index.html`, accessible at `https://reinvently.co.uk/guides/`. It SHALL list all articles classified as Guides, ordered newest-first, using the same post-card pattern as the blog index.

#### Scenario: Visitor navigates to /guides/
- **WHEN** a visitor navigates to `/guides/`
- **THEN** they see a page titled "Technical Guides" (or similar) listing all 8 guide articles as post-cards with date, category label, title, and excerpt

#### Scenario: Guides page has correct SEO metadata
- **WHEN** a search engine crawls `/guides/`
- **THEN** the page has a descriptive `<title>` and `<meta name="description">` specific to technical guides

#### Scenario: Guides page links to article pages
- **WHEN** a visitor clicks a post card on the guides page
- **THEN** they are taken to the article at its existing `blog/<slug>/` URL

# news-section

## Purpose

A dedicated landing page at `/news/` listing all AI news articles, providing a focused entry point for visitors seeking curated news coverage.

## Requirements

### Requirement: News section landing page exists at /news/
A static HTML page SHALL exist at `news/index.html`, accessible at `https://reinvently.co.uk/news/`. It SHALL list all articles classified as News, ordered newest-first, using the same post-card pattern as the blog index.

#### Scenario: Visitor navigates to /news/
- **WHEN** a visitor navigates to `/news/`
- **THEN** they see a page titled "AI News" (or similar) listing all 10 news articles as post-cards with date, category label, title, and excerpt

#### Scenario: News page has correct SEO metadata
- **WHEN** a search engine crawls `/news/`
- **THEN** the page has a descriptive `<title>` and `<meta name="description">` specific to AI news coverage

#### Scenario: News page links to article pages
- **WHEN** a visitor clicks a post card on the news page
- **THEN** they are taken to the article at its existing `blog/<slug>/` URL

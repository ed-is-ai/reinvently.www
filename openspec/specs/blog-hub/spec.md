# blog-hub

## Purpose

The `/blog/` page serves as a content hub that directs visitors to the News and Guides sections, replacing the old tag-filtered blog index.

## Requirements

### Requirement: Blog index is a content hub directing to News and Guides
`blog/index.html` SHALL be updated to serve as a hub page that prominently directs visitors to the News and Guides sections. The JS filter bar (Enterprise Adoption / Technology Strategy / UK AI News buttons) SHALL be removed. The page SHALL include a brief intro, two section callout blocks (News and Guides) with links, and a combined recent articles listing.

#### Scenario: Visitor lands on /blog/
- **WHEN** a visitor navigates to `/blog/`
- **THEN** they see the blog hub with clear links to `/news/` and `/guides/` sections, followed by a listing of recent articles across both categories

#### Scenario: Filter bar is removed
- **WHEN** a visitor views `/blog/`
- **THEN** there are no filter buttons (the old Enterprise Adoption / Technology Strategy / UK AI News buttons are gone)

#### Scenario: Hub page retains RSS/Atom feed links
- **WHEN** the blog hub page is rendered
- **THEN** the `<head>` still contains the `<link rel="alternate">` elements for the Atom, RSS, and JSON feeds

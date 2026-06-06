## MODIFIED Requirements

### Requirement: Homepage SEO metadata reflects news and guides positioning
The homepage `index.html` `<meta name="description">` and `<title>` SHALL be updated to reflect the site's new purpose as a curated AI news and technical guides destination. The existing consulting-focused messaging SHALL be replaced.

#### Scenario: Homepage title reflects new positioning
- **WHEN** a search engine or browser tab renders the homepage
- **THEN** the `<title>` reflects the new positioning (e.g. "Reinvently — Curated AI News &amp; Technical Guides")

#### Scenario: Homepage meta description reflects new positioning
- **WHEN** a search engine crawls the homepage
- **THEN** `<meta name="description">` describes Reinvently as a source of curated AI news and technical guides, not as an AI consultancy

#### Scenario: OG tags updated on homepage
- **WHEN** the homepage URL is shared on social media
- **THEN** the `og:title` and `og:description` reflect the curated news + guides positioning

# services-hidden

## Purpose

Ensures all services pages are excluded from search engine indexing, preventing them from appearing in search results while the services offering is not publicly promoted.

## Requirements

### Requirement: Services pages are excluded from search engine indexing
All services pages SHALL include a `<meta name="robots" content="noindex, nofollow">` tag in `<head>` so search engines do not index or follow links on these pages.

#### Scenario: Services index page has noindex tag
- **WHEN** a search engine crawler visits `/services/`
- **THEN** the page response SHALL contain `<meta name="robots" content="noindex, nofollow">` in `<head>`

#### Scenario: Each services sub-page has noindex tag
- **WHEN** a search engine crawler visits any services sub-page (`/services/strategy/`, `/services/pilot/`, `/services/accelerate/`, `/services/build/`, `/services/first-aid/`, `/services/scale/`, `/services/sdlc-enablement/`)
- **THEN** the page response SHALL contain `<meta name="robots" content="noindex, nofollow">` in `<head>`

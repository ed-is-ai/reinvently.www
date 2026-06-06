## MODIFIED Requirements

### Requirement: Blog page navs include a Services link
**This requirement is superseded.** The nav SHALL contain: logo, Home, News, Guides, Contact. The "Blog" link SHALL be replaced with "News" (linking to `/news/`) and "Guides" (linking to `/guides/`).

#### Scenario: Nav contains News and Guides links
- **WHEN** a visitor views any page (homepage, blog, news, guides, articles, contact)
- **THEN** the nav contains "News" linking to `/news/` and "Guides" linking to `/guides/`

#### Scenario: Blog link is removed from nav
- **WHEN** a visitor views any page
- **THEN** the nav does NOT contain a standalone "Blog" link

#### Scenario: Active state on section pages
- **WHEN** a visitor is on the `/news/` page
- **THEN** the "News" nav link has `aria-current="page"` applied

#### Scenario: Active state on guides page
- **WHEN** a visitor is on the `/guides/` page
- **THEN** the "Guides" nav link has `aria-current="page"` applied

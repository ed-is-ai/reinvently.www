## ADDED Requirements

### Requirement: Blog page navs include a Services link
Every hand-crafted blog page (all `blog/*/index.html` files and `blog/index.html`) SHALL include a "Services" link in the nav pointing to `/services/`.

#### Scenario: Services link is present in blog nav
- **WHEN** a visitor views any blog page
- **THEN** the nav contains a "Services" link alongside the existing "Home" and "Blog" links

#### Scenario: Services link navigates correctly
- **WHEN** a visitor clicks the Services link in the blog nav
- **THEN** they are taken to `/services/`

### Requirement: Service pages include consistent nav
All six service pages SHALL use a nav containing: Reinvently logo (linking to `/`), Home, Blog, and Services links. The Services link SHALL be visually consistent with the Home and Blog links.

#### Scenario: Service page nav is complete
- **WHEN** a visitor views any service page
- **THEN** the nav contains: Reinvently logo, Home, Blog, and Services

### Requirement: Homepage nav includes a Services link (best-effort)
The homepage `index.html` SHALL have a Services link added to the nav where structurally possible given the minified website-builder HTML.

#### Scenario: Services link is reachable from homepage
- **WHEN** a visitor views the homepage
- **THEN** a Services link is visible in the nav or header area

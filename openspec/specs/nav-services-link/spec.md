# nav-services-link

## Purpose

Defines which pages include or exclude a "Services" link in the nav. With services pages being hidden, the Services link is removed from all navs site-wide.

## Requirements

### Requirement: Blog page navs include a Services link
Every hand-crafted blog page (all `blog/*/index.html` files and `blog/index.html`) SHALL NOT include a "Services" link in the nav. The nav SHALL contain only "Home" and "Blog" links.

#### Scenario: Services link is absent from blog nav
- **WHEN** a visitor views any blog page
- **THEN** the nav does NOT contain a "Services" link

### Requirement: Service pages include consistent nav
All service pages SHALL use a nav containing: Reinvently logo (linking to `/`), Home, and Blog links only. The Services link SHALL be removed.

#### Scenario: Service page nav does not include a Services link
- **WHEN** a visitor views any service page
- **THEN** the nav contains: Reinvently logo, Home, Blog — but NOT a Services link

### Requirement: Homepage nav includes a Services link (best-effort)
**REMOVED** — The Services link SHALL be removed from the homepage nav.

#### Scenario: Services link is absent from homepage
- **WHEN** a visitor views the homepage
- **THEN** no Services link is visible in the nav or header area

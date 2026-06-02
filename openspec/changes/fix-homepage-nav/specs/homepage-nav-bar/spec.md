## ADDED Requirements

### Requirement: Fixed nav bar present on homepage
The homepage SHALL have a `position: fixed` nav bar at the top of the viewport, visible at all scroll positions, containing the Reinvently logo and navigation links.

#### Scenario: Nav bar is visible on page load
- **WHEN** a visitor opens the homepage
- **THEN** a nav bar is visible at the top of the viewport containing "Reinvently", "Blog", and "Services"

#### Scenario: Nav bar remains visible on scroll
- **WHEN** a visitor scrolls down the homepage
- **THEN** the nav bar remains fixed at the top of the viewport

### Requirement: Nav bar links navigate correctly
The nav bar SHALL contain three links: Reinvently logo to `/`, Blog to `/blog/`, Services to `/services/`.

#### Scenario: Blog link navigates to blog
- **WHEN** a visitor clicks "Blog"
- **THEN** they are taken to `/blog/`

#### Scenario: Services link navigates to services
- **WHEN** a visitor clicks "Services"
- **THEN** they are taken to `/services/`

### Requirement: Nav bar is visually consistent with blog nav
The homepage nav bar SHALL use the same visual design as the blog page nav: dark background (`#000`), Montserrat font, uppercase letter-spaced links in muted grey, bottom border separator.

#### Scenario: Nav matches blog nav appearance
- **WHEN** a visitor views the homepage nav and a blog page nav side by side
- **THEN** the styling (colour, font, spacing, link treatment) is indistinguishable

### Requirement: Page content is not obscured by fixed nav
The homepage content SHALL not be hidden behind the fixed nav bar. A `padding-top` SHALL be applied to push content below the nav height.

#### Scenario: Hero content starts below nav
- **WHEN** a visitor views the homepage
- **THEN** the website-builder hero content begins below the nav bar, not behind it

## MODIFIED Requirements

### Requirement: Nav Services link delivered via fixed nav, not script injection
The homepage Services link SHALL be delivered by the fixed `<nav>` element rather than by the previous script injection into `navBarId-18199`. The injection script SHALL be removed.

#### Scenario: No floating Services label in hero
- **WHEN** a visitor views the homepage
- **THEN** "Services" does not appear as a floating label in the top-left corner of the hero image

#### Scenario: Services link renders in nav bar
- **WHEN** a visitor views the homepage
- **THEN** "Services" appears in the top nav bar alongside "Blog", correctly positioned

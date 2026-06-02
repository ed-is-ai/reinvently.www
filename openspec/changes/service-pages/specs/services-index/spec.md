## ADDED Requirements

### Requirement: Services index page exists at /services/
The site SHALL provide a page at `/services/index.html` (served as `/services/`) that presents the full Reinvently service offering and allows visitors to self-select a relevant service.

#### Scenario: Page loads successfully
- **WHEN** a visitor navigates to `/services/`
- **THEN** the page renders with the site nav, a journey diagram, service cards, and a First Aid section

### Requirement: Journey diagram shows progressive services
The services index SHALL display Strategy, Pilot, Accelerate, and Productionise as a connected horizontal sequence conveying a left-to-right progression.

#### Scenario: Journey sequence is visible
- **WHEN** a visitor views the services index on desktop
- **THEN** four labelled steps appear in order: Strategy → Pilot → Accelerate → Productionise, connected by a visual line

#### Scenario: Journey is readable on mobile
- **WHEN** a visitor views the services index on a screen narrower than 640px
- **THEN** the journey diagram stacks vertically and remains legible

### Requirement: First Aid appears as a separate entry point
The services index SHALL present First Aid below a visual divider, distinct from the progressive journey, with copy that identifies it as a route for organisations whose AI projects have already failed.

#### Scenario: First Aid is visually separated
- **WHEN** a visitor views the services index
- **THEN** First Aid appears below a horizontal rule with a label such as "Already have an AI project that isn't working?"

### Requirement: Each service links to its individual page
Every service shown on the index SHALL be a link to its respective service page.

#### Scenario: Clicking a service card navigates correctly
- **WHEN** a visitor clicks any service card or link on the index
- **THEN** they are taken to the corresponding `/services/<service>/` page

## ADDED Requirements

### Requirement: Strategy service page exists at /services/strategy/
The site SHALL provide a page at `/services/strategy/` that describes the Strategy engagement for organisations that have not yet committed to an AI use case.

#### Scenario: Page loads with correct structure
- **WHEN** a visitor navigates to `/services/strategy/`
- **THEN** the page renders with: site nav, article header naming the buyer's situation, problem section, what-we-do section, output section, and a contact form

### Requirement: Strategy page addresses the C-suite buyer
The Strategy page copy SHALL speak to a Board, CDO, or C-suite audience facing the question "where does AI fit for us?" The tone SHALL be authoritative and strategic, not technical.

#### Scenario: Header names the buyer's situation
- **WHEN** a visitor reads the page header
- **THEN** the headline and summary reflect the uncertainty of an organisation that has seen what AI can do but hasn't decided how to proceed

### Requirement: Strategy page states the engagement output
The Strategy page SHALL clearly state the tangible outputs: an AI readiness assessment, a prioritised opportunity map, and a business case for the highest-value use case.

#### Scenario: Outputs are listed explicitly
- **WHEN** a visitor reads the output section
- **THEN** three deliverables are named: AI readiness assessment, prioritised opportunity map, business case

### Requirement: Strategy page includes a contact form
The Strategy page SHALL embed a Formspree contact form with a hidden field `service` set to `strategy` and `_subject` set to `Strategy enquiry — Reinvently`.

#### Scenario: Form submits with correct metadata
- **WHEN** a visitor submits the form on the Strategy page
- **THEN** the Formspree submission includes `service=strategy` and the correct subject line

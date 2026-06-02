## ADDED Requirements

### Requirement: Accelerate service page exists at /services/accelerate/
The site SHALL provide a page at `/services/accelerate/` describing the Accelerate engagement for organisations whose pilot succeeded and who need to move faster, broader, and without dropping quality.

#### Scenario: Page loads with correct structure
- **WHEN** a visitor navigates to `/services/accelerate/`
- **THEN** the page renders with: site nav, article header, problem section, what-we-do section, output section, and a contact form

### Requirement: Accelerate page addresses the delivery lead or CTO buyer
The Accelerate page copy SHALL speak to a delivery lead, CTO, or technical programme owner who needs to scale delivery beyond the pilot. The tone SHALL be execution-focused.

#### Scenario: Header names the buyer's situation
- **WHEN** a visitor reads the page header
- **THEN** the headline and summary reflect the situation of having a working pilot but needing to go faster and broader

### Requirement: Accelerate page states the engagement output
The Accelerate page SHALL state the tangible outputs: delivery acceleration, expanded use case coverage, and team capability transfer.

#### Scenario: Outputs are listed explicitly
- **WHEN** a visitor reads the output section
- **THEN** three deliverables are named: delivery acceleration, expanded use case coverage, team capability transfer

### Requirement: Accelerate page includes a contact form
The Accelerate page SHALL embed a Formspree contact form with a hidden field `service` set to `accelerate` and `_subject` set to `Accelerate enquiry — Reinvently`.

#### Scenario: Form submits with correct metadata
- **WHEN** a visitor submits the form on the Accelerate page
- **THEN** the Formspree submission includes `service=accelerate` and the correct subject line

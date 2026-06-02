## ADDED Requirements

### Requirement: Pilot service page exists at /services/pilot/
The site SHALL provide a page at `/services/pilot/` describing the Pilot engagement for organisations that have a use case and need to prove it works before committing further budget.

#### Scenario: Page loads with correct structure
- **WHEN** a visitor navigates to `/services/pilot/`
- **THEN** the page renders with: site nav, article header, problem section, what-we-do section, output section, and a contact form

### Requirement: Pilot page addresses the programme sponsor buyer
The Pilot page copy SHALL speak to a programme sponsor or equivalent decision-maker who needs evidence to justify further investment. The tone SHALL be pragmatic and evidence-focused.

#### Scenario: Header names the buyer's situation
- **WHEN** a visitor reads the page header
- **THEN** the headline and summary reflect the need to prove a use case works before committing further budget

### Requirement: Pilot page states the engagement output
The Pilot page SHALL state the tangible outputs: a working prototype, evaluation results, and a go/no-go recommendation.

#### Scenario: Outputs are listed explicitly
- **WHEN** a visitor reads the output section
- **THEN** three deliverables are named: working prototype, evaluation results, go/no-go recommendation

### Requirement: Pilot page includes a contact form
The Pilot page SHALL embed a Formspree contact form with a hidden field `service` set to `pilot` and `_subject` set to `Pilot enquiry — Reinvently`.

#### Scenario: Form submits with correct metadata
- **WHEN** a visitor submits the form on the Pilot page
- **THEN** the Formspree submission includes `service=pilot` and the correct subject line

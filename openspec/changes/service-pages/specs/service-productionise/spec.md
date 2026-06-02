## ADDED Requirements

### Requirement: Productionise service page exists at /services/productionise/
The site SHALL provide a page at `/services/productionise/` describing the Productionise engagement for organisations ready to take their AI system live, covering security, governance, monitoring, and operationalisation.

#### Scenario: Page loads with correct structure
- **WHEN** a visitor navigates to `/services/productionise/`
- **THEN** the page renders with: site nav, article header, problem section, what-we-do section, output section, and a contact form

### Requirement: Productionise page addresses the engineering and CISO buyer
The Productionise page copy SHALL speak to engineering leads, CISOs, or technical owners responsible for making AI systems safe, compliant, and operationally sound. The tone SHALL be precise and risk-aware.

#### Scenario: Header names the buyer's situation
- **WHEN** a visitor reads the page header
- **THEN** the headline and summary reflect that the hard part of AI in production is security, governance, monitoring, and making it stick — not the model itself

### Requirement: Productionise page states the engagement output
The Productionise page SHALL state the tangible outputs: a production-ready system, a governance framework, and an operational runbook.

#### Scenario: Outputs are listed explicitly
- **WHEN** a visitor reads the output section
- **THEN** three deliverables are named: production-ready system, governance framework, operational runbook

### Requirement: Productionise page includes a contact form
The Productionise page SHALL embed a Formspree contact form with a hidden field `service` set to `productionise` and `_subject` set to `Productionise enquiry — Reinvently`.

#### Scenario: Form submits with correct metadata
- **WHEN** a visitor submits the form on the Productionise page
- **THEN** the Formspree submission includes `service=productionise` and the correct subject line

## ADDED Requirements

### Requirement: First Aid service page exists at /services/first-aid/
The site SHALL provide a page at `/services/first-aid/` describing a diagnostic engagement for organisations whose AI project has failed or stalled, producing a written report and presentation with a plan of action.

#### Scenario: Page loads with correct structure
- **WHEN** a visitor navigates to `/services/first-aid/`
- **THEN** the page renders with: site nav, article header, problem section, what-we-do section, output section, and a contact form

### Requirement: First Aid page uses a no-judgment tone
The First Aid page copy SHALL acknowledge that AI project failure is common and that the buyer may feel pressure or embarrassment. The tone SHALL be direct, empathetic, and free of blame. The copy SHALL not require the visitor to characterise their situation before making contact.

#### Scenario: Header names the buyer's situation without judgment
- **WHEN** a visitor reads the page header
- **THEN** the headline and summary reflect that their AI project is in trouble and they need clarity on whether to fix it or start over — without implying they made poor decisions

### Requirement: First Aid diagnostic covers four failure dimensions
The First Aid what-we-do section SHALL describe a diagnostic that examines all four common AI project failure modes: technical, architectural, organisational, and strategic.

#### Scenario: Diagnostic scope is described
- **WHEN** a visitor reads the what-we-do section
- **THEN** the four dimensions (technical, architectural, organisational, strategic) are referenced explicitly or through clear description

### Requirement: First Aid output is a written report and presentation
The First Aid page SHALL state that the engagement output is a written diagnostic report and a presentation, both containing a plan of action with a clear verdict: fix-it or reboot.

#### Scenario: Output format is stated explicitly
- **WHEN** a visitor reads the output section
- **THEN** both a written report and a presentation are named as deliverables, with the fix-it/reboot framing present

### Requirement: First Aid page explains where the engagement leads
The First Aid page SHALL indicate that the plan of action leads into one of the other Reinvently services depending on the verdict: Pilot (reboot), Accelerate (fix), or Productionise (governance gap).

#### Scenario: Onward journey is signposted
- **WHEN** a visitor reads the First Aid page
- **THEN** the page makes clear that the diagnostic produces a next step, not just a report, and that Reinvently can execute it

### Requirement: First Aid page includes a contact form
The First Aid page SHALL embed a Formspree contact form with a hidden field `service` set to `first-aid` and `_subject` set to `First Aid enquiry — Reinvently`.

#### Scenario: Form submits with correct metadata
- **WHEN** a visitor submits the form on the First Aid page
- **THEN** the Formspree submission includes `service=first-aid` and the correct subject line

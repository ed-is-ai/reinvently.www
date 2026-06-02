## ADDED Requirements

### Requirement: Contact page exists at /contact/
The site SHALL provide a page at `/contact/index.html` (served as `/contact/`) containing the Formspree contact form.

#### Scenario: Page loads with correct structure
- **WHEN** a visitor navigates to `/contact/`
- **THEN** the page renders with: site nav, page header, contact form, and footer

### Requirement: Contact form contains required fields
The contact page form SHALL contain: Name (text, required), Email (email, required), Message (textarea, required), GDPR consent checkbox (required), and a submit button.

#### Scenario: Form submits correctly
- **WHEN** a visitor fills all fields and submits
- **THEN** the form posts to the Formspree endpoint

### Requirement: Contact page sets response expectation
The contact page SHALL include copy stating that Reinvently responds within one business day.

#### Scenario: Response time is visible
- **WHEN** a visitor reads the contact page header
- **THEN** the page states a response time expectation

### Requirement: Contact nav link is marked active on contact page
The "Contact" link in the nav on the contact page SHALL carry `aria-current="page"`.

#### Scenario: Active nav state on contact page
- **WHEN** a visitor is on `/contact/`
- **THEN** the Contact nav link has `aria-current="page"` and renders visually as active

## MODIFIED Requirements

### Requirement: All Contact nav links point to /contact/
Every "Contact" link in every nav bar across the site SHALL link to `/contact/` rather than `/#contact`.

#### Scenario: Nav Contact link destination
- **WHEN** a visitor clicks "Contact" in any nav bar
- **THEN** they are taken to `/contact/`

### Requirement: Service page CTAs point to /contact/
All `.contact-cta` buttons on service pages SHALL link to `/contact/`.

#### Scenario: Service page CTA destination
- **WHEN** a visitor clicks a service page CTA button (e.g. "Start the conversation →")
- **THEN** they are taken to `/contact/`

### Requirement: Homepage contact section shows a CTA card
The homepage contact section (`id="contact"`) SHALL show a brief CTA card with a link to `/contact/` rather than an embedded form.

#### Scenario: Homepage contact section
- **WHEN** a visitor scrolls to the contact section on the homepage
- **THEN** they see a "Get in touch" card with a link to the contact page, not a form

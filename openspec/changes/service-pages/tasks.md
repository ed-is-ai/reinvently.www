## 1. Scaffolding

- [x] 1.1 Create `services/` directory at repo root
- [x] 1.2 Create `services/services.css` with journey diagram styles, service card grid, and First Aid divider section styles (dark theme, consistent with blog.css tokens)
- [x] 1.3 Verify `blog/blog.css` is reachable from `services/` pages at path `../blog/blog.css`

## 2. Services Index Page

- [x] 2.1 Create `services/index.html` with site nav (Home, Blog, Services), page header, and footer
- [x] 2.2 Add journey diagram section: four connected steps (Strategy → Pilot → Accelerate → Productionise) linking to their respective service pages
- [x] 2.3 Add First Aid section below a `<hr>` divider with copy that identifies it as the entry point for failed AI projects, linking to `/services/first-aid/`
- [x] 2.4 Verify index page renders correctly on desktop and mobile (stacked layout at <640px)

## 3. Strategy Service Page

- [x] 3.1 Create `services/strategy/index.html` with full page structure: nav, article header, problem section, what-we-do section, output section, contact form, footer
- [x] 3.2 Write copy addressing the C-suite/CDO buyer; headline names the situation ("where does AI fit for us?")
- [x] 3.3 Output section lists: AI readiness assessment, prioritised opportunity map, business case
- [x] 3.4 Embed Formspree form with `service=strategy` hidden field and `_subject=Strategy enquiry — Reinvently`

## 4. Pilot Service Page

- [x] 4.1 Create `services/pilot/index.html` with full page structure
- [x] 4.2 Write copy addressing the programme sponsor buyer; headline names the situation ("prove it works before committing further budget")
- [x] 4.3 Output section lists: working prototype, evaluation results, go/no-go recommendation
- [x] 4.4 Embed Formspree form with `service=pilot` hidden field and `_subject=Pilot enquiry — Reinvently`

## 5. Accelerate Service Page

- [x] 5.1 Create `services/accelerate/index.html` with full page structure
- [x] 5.2 Write copy addressing the delivery lead/CTO buyer; headline names the situation ("your pilot worked — now go faster and broader")
- [x] 5.3 Output section lists: delivery acceleration, expanded use case coverage, team capability transfer
- [x] 5.4 Embed Formspree form with `service=accelerate` hidden field and `_subject=Accelerate enquiry — Reinvently`

## 6. Scale Service Page (renamed from Productionise)

- [x] 6.1 Create `services/scale/index.html` with full page structure
- [x] 6.2 Write copy addressing the engineering/CISO buyer; headline names the situation ("the hard part isn't the model — it's making it safe and operational")
- [x] 6.3 Output section lists: production-ready system, governance framework, operational runbook
- [x] 6.4 Embed Formspree form with `service=scale` hidden field and `_subject=Scale enquiry — Reinvently`

## 7. First Aid Service Page

- [x] 7.1 Create `services/first-aid/index.html` with full page structure
- [x] 7.2 Write copy in no-judgment tone; headline names the situation without blame ("your AI project is in trouble — fix it or reboot?")
- [x] 7.3 What-we-do section describes the diagnostic covering: technical, architectural, organisational, and strategic failure modes
- [x] 7.4 Output section states: written diagnostic report + presentation with fix-it or reboot plan of action
- [x] 7.5 Add signpost showing the onward journey: Pilot (reboot), Accelerate (fix), or Scale (governance gap)
- [x] 7.6 Embed Formspree form with `service=first-aid` hidden field and `_subject=First Aid enquiry — Reinvently`

## 8. Nav Updates

- [x] 8.1 Update all blog page navs to add `<a href="/services/">Services</a>` after the Blog link — applies to `blog/index.html` and all `blog/*/index.html` files (~15 pages)
- [x] 8.2 Update homepage `index.html` nav: injected Services link via script targeting `navBarId-18199`
- [x] 8.3 Verify nav Services link is visible and functional across: homepage, blog index, a sample blog post, and all service pages

## 9. Deployment Prerequisites

- [ ] 9.1 Register a Formspree account (or use existing) and create a form; substitute `YOUR_FORMSPREE_ID` with the real form ID in all service pages and in `index.html`
- [x] 9.2 Add `services/` pages to `sitemap.xml` (including Build and SDLC Enablement)
- [x] 9.3 Verify all internal links resolve (no 404s): services index → each service page; service pages → back to services index; nav links across all pages

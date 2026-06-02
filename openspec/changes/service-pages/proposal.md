## Why

Reinvently has no service pages. The site currently presents as a content/blog destination, but there is no clear path for a prospective client to understand what Reinvently offers, self-identify their situation, and make contact. Five services form a coherent client journey — from initial AI strategy through to production — with a separate rescue entry point for organisations whose AI projects have failed.

## What Changes

- New `/services/` directory with 6 HTML pages (index + 5 service pages)
- New `/services/services.css` for service-specific styles (journey diagram, service cards)
- Nav updated across all blog pages and the homepage to add a "Services" link
- Formspree contact form embedded on each service page, with a hidden field tagging the enquiry source

## Capabilities

### New Capabilities

- `services-index`: Landing page at `/services/` showing the client journey (Strategy → Pilot → Accelerate → Productionise) with First Aid as a separate entry point below a divider
- `service-strategy`: Page at `/services/strategy/` — AI readiness assessment, opportunity map, and business case for organisations that haven't yet committed to a use case
- `service-pilot`: Page at `/services/pilot/` — scoped proof-of-concept engagement with a go/no-go recommendation output
- `service-accelerate`: Page at `/services/accelerate/` — delivery acceleration, expanded use case coverage, and team capability transfer for organisations whose pilot succeeded
- `service-productionise`: Page at `/services/productionise/` — production-ready delivery covering security, governance, monitoring, and operational runbooks
- `service-first-aid`: Page at `/services/first-aid/` — diagnostic engagement for failed AI projects, producing a written report and presentation with a fix-it or reboot plan of action
- `nav-services-link`: "Services" link added to the shared nav across all site pages

### Modified Capabilities

## Impact

- New directory: `services/` with 6 HTML files and 1 CSS file
- Modified nav HTML in: `blog/blog.css` (nav is HTML not CSS, so changes to all ~15 blog page `index.html` files and `blog/index.html`)
- Homepage `index.html` nav section updated (the nav is embedded in the minified website-builder HTML)
- No build system changes — static HTML only
- Formspree endpoint: existing `YOUR_FORMSPREE_ID` placeholder used; a real ID will need to be substituted before the form is live

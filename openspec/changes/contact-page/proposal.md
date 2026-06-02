## Why

The contact form currently lives embedded inside the homepage, built by the website-builder. It is not directly linkable, not independently crawlable by search engines, and shares a page with blog content and hero imagery — a poor experience for a visitor who has already decided they want to get in touch. A dedicated `/contact/` page gives the form its own URL, a clean focused layout, and the right structural context for a high-intent visitor.

## What Changes

- New `/contact/index.html` — a standalone contact page using the same blog.css design system, containing the Formspree form, a brief "Get in touch" header, and a response-time expectation
- Homepage: the embedded contact form section is replaced with a simple "Get in touch" CTA card that links to `/contact/` — the website-builder's contact section is retained structurally but its form is removed in favour of a link
- All nav "Contact" links updated from `/#contact` to `/contact/` across the homepage fixed nav, all blog pages, and all service pages
- All service page CTA buttons (`.contact-cta`) updated from `/#contact` to `/contact/`
- Schema.org `contactPoint.url` on homepage updated to `https://reinvently.co.uk/contact/`
- Sitemap updated with `/contact/`

## Capabilities

### New Capabilities

- `contact-page`: Dedicated page at `/contact/` containing the Formspree contact form with Name, Email, Message, and GDPR consent fields — styled consistently with blog and service pages

### Modified Capabilities

- `nav-contact-link`: All nav "Contact" links updated from `/#contact` to `/contact/`
- `service-page-cta`: All service page `.contact-cta` button `href` values updated from `/#contact` to `/contact/`
- `homepage-contact-section`: Homepage contact section simplified to a CTA card linking to `/contact/` — the embedded form removed

## Impact

- New file: `contact/index.html`
- Modified: `index.html` — contact section form replaced with CTA link, schema.org contactPoint URL updated, nav unchanged (already done)
- Modified: all 19 blog pages — nav Contact href `/#contact` → `/contact/`
- Modified: all 8 service pages — nav Contact href + CTA button href `/#contact` → `/contact/`
- Modified: `sitemap.xml` — add `/contact/` entry

## 1. Create contact page

- [x] 1.1 Create `contact/index.html` — full page structure: site nav (Home · Blog · Services · Contact with `aria-current="page"`), `.page-header` with "Get in touch" heading and response-time copy, `.container` with `.contact-form` (Name, Email, Message, GDPR, Submit), footer
- [x] 1.2 Link stylesheets: `../blog/blog.css` and `../services/services.css` for form styles
- [x] 1.3 Add canonical, OG, Twitter Card, and Schema.org `ContactPage` structured data to `<head>`
- [x] 1.4 Add `/contact/` to `sitemap.xml`

## 2. Update links sitewide

- [x] 2.1 Replace `/#contact` with `/contact/` in the homepage fixed nav (`index.html` — `sn-links` div)
- [x] 2.2 Replace `href="/#contact">Contact</a>` with `href="/contact/">Contact</a>` across all 19 blog pages and blog/index.html (sed pass)
- [x] 2.3 Replace `href="/#contact">Contact</a>` with `href="/contact/">Contact</a>` across all 8 service pages (sed pass)
- [x] 2.4 Replace `href="/#contact"` on all `.contact-cta` buttons across 7 service pages (sed pass)

## 3. Update homepage contact section

- [x] 3.1 Locate the `<form>` element inside the homepage `id="contact"` section and replace it with a styled CTA paragraph and link to `/contact/`
- [x] 3.2 Update schema.org `contactPoint.url` in `index.html` from `https://reinvently.co.uk/#contact` to `https://reinvently.co.uk/contact/`

## 4. Verify

- [x] 4.1 Confirm `/contact/` page loads with form, header, and nav
- [x] 4.2 Confirm all nav Contact links across homepage, blog, and service pages point to `/contact/`
- [x] 4.3 Confirm service page CTA buttons point to `/contact/`
- [x] 4.4 Confirm homepage contact section shows CTA card, not a form

## Context

The site has three page families: the homepage (website-builder export), blog pages (hand-crafted HTML using `blog/blog.css`), and service pages (hand-crafted HTML using `blog/blog.css` + `services/services.css`). The contact form currently lives in the homepage's website-builder section at `id="contact"`, using Formspree (`action="https://formspree.io/f/YOUR_FORMSPREE_ID"`).

All nav bars and service page CTAs currently link to `/#contact`. These were added in the `service-pages` and `fix-homepage-nav` changes.

## Goals / Non-Goals

**Goals:**
- A standalone `/contact/` page with the Formspree form, clean layout, response-time expectation, and full nav
- All links pointing to the contact form updated to `/contact/`
- The homepage contact section simplified to a CTA link rather than an embedded form

**Non-Goals:**
- Replacing Formspree with a different form backend
- Adding new form fields beyond the current set (Name, Email, Message, GDPR consent)
- Removing the website-builder's contact section structural HTML (only replacing its content)

## Decisions

**D1: Contact page follows blog/service page pattern exactly**

`contact/index.html` uses `../blog/blog.css`, the same nav (Home · Blog · Services · Contact), and the `.article-header` / `.container` / `.article-body` structure. The form is styled with `services/services.css` `.contact-section` and `.contact-form` classes (already defined — no new CSS needed).

The Contact nav link on the contact page itself gets `aria-current="page"` to mark it as active.

**D2: Homepage contact section — replace form with a CTA card**

The website-builder's contact section (`id="contact"`) is retained structurally (removing it risks breaking the builder's JS). Its inner content (the `<form>` element) is replaced with a brief paragraph and a styled `<a>` button linking to `/contact/`. This keeps the anchor `id="contact"` intact for any existing bookmarks, while the visual output is a simple "Get in touch" card rather than a full form.

**D3: All `/#contact` hrefs become `/contact/`**

Two types of link need updating:
1. Nav "Contact" links — `<a href="/#contact">Contact</a>` → `<a href="/contact/">Contact</a>` — across homepage fixed nav, 19 blog pages, 8 service pages
2. Service page CTA buttons — `<a class="contact-cta" href="/#contact">` → `href="/contact/"` — across 7 service pages

Both are mechanical find-replace operations.

**D4: Schema.org contactPoint updated**

`index.html` line ~679: `"url": "https://reinvently.co.uk/#contact"` → `"url": "https://reinvently.co.uk/contact/"`

**D5: Contact page URL `/contact/` not `/contact.html`**

Consistent with the site's clean URL pattern (`/blog/`, `/services/`, etc.). Implemented as `contact/index.html`.

## Risks / Trade-offs

- **Existing `/#contact` bookmarks or external links** → The homepage `id="contact"` anchor is preserved, so `/#contact` still navigates to the section; it just shows a CTA card rather than the form. Any bookmark lands on the page and sees the link to `/contact/`. Low risk.
- **Form not live until Formspree ID is substituted** → The same `YOUR_FORMSPREE_ID` placeholder is used. Same situation as service pages — a deployment step, not a code change.

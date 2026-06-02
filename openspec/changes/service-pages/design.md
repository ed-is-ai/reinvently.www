## Context

The Reinvently site is a static HTML site hosted on GitHub Pages. There is no build system, no templating engine, and no JavaScript framework. The homepage (`index.html`) is a minified export from a website builder (GoDaddy Airo). All blog pages are hand-crafted HTML using a shared `blog/blog.css` stylesheet.

The nav on blog pages is plain HTML (inside each page's `<body>`). The nav on the homepage is embedded inside a heavily minified class-soup structure from the website builder and cannot easily be edited as HTML.

The contact form uses Formspree (`action="https://formspree.io/f/YOUR_FORMSPREE_ID"`). The Formspree ID is currently a placeholder.

## Goals / Non-Goals

**Goals:**
- 6 new static HTML pages for the services section, consistent with the existing blog visual language
- A shared CSS file for service-specific components (journey diagram, service cards on the index page)
- The contact form embedded on each individual service page, with a hidden field identifying the service
- Nav updated across all blog pages to add a "Services" link
- A homepage nav link to services (best-effort, working within the minified HTML constraint)

**Non-Goals:**
- No server-side logic, CMS, or build pipeline
- No new JavaScript beyond simple, inline enhancements if needed
- No redesign of existing blog pages or the homepage
- Replacing the Formspree placeholder ID — that is a deployment step, not a code change

## Decisions

**D1: Reuse blog.css, extend with services.css**

Service pages link to `../blog/blog.css` (one level up from `services/`) for the shared design tokens and base components, plus a new `services/services.css` for service-specific additions (journey progress diagram on the index page, service card grid).

Alternative considered: copy blog.css into services/. Rejected — duplicating the stylesheet creates a maintenance burden when the design language evolves.

**D2: Flat file structure under /services/**

```
services/
  index.html               ← services index
  services.css             ← service-specific styles
  strategy/index.html
  pilot/index.html
  accelerate/index.html
  productionise/index.html
  first-aid/index.html
```

This mirrors the blog directory structure and keeps URLs clean (`/services/strategy/`).

**D3: Per-page Formspree form with hidden service field**

Each service page embeds the Formspree form directly (rather than linking to a contact page) with a hidden input: `<input type="hidden" name="service" value="[service-name]" />`. This tags every inbound enquiry with its source at the point of submission, which is more reliable than a referrer-based approach.

The `_subject` hidden field is also customised per service: "Strategy enquiry — Reinvently", "First Aid enquiry — Reinvently", etc.

**D4: Homepage nav — best-effort edit inside minified HTML**

The homepage nav is embedded inside minified website-builder markup. Rather than attempting a structural edit, we locate the nav link block (which contains the "Blog" link) and append a "Services" link immediately after it using the same inline style pattern. If the minified structure makes this too brittle, a fallback is to leave the homepage nav unchanged and rely on the services index page being reachable via blog nav and direct links.

**D5: Services index uses a visual journey diagram in HTML/CSS**

The index page shows the four progressive services as a horizontal step diagram (Strategy → Pilot → Accelerate → Productionise), with First Aid below a divider as a separate entry point. This is implemented in pure HTML/CSS — no SVG, no JS — using flexbox and a connecting line technique consistent with the dark theme.

## Risks / Trade-offs

- **Homepage nav fragility** → The minified HTML makes surgical edits risky. Mitigation: locate the nav block by the presence of the "Blog" anchor text and add the Services link in the same pattern. Test visually before committing.
- **Blog page nav updates are manual** → There are ~15 blog pages each with their own nav HTML. Mitigation: use a targeted find-and-replace on the nav block pattern (`<a href="/blog/">Blog</a>`) to append `<a href="/services/">Services</a>` consistently.
- **Formspree ID not wired** → Forms will not submit until the real Formspree ID is substituted. Mitigation: note this clearly in tasks.md as a deployment prerequisite; the placeholder is already present in the codebase.
- **services.css path from nested pages** → Individual service pages are one level deeper than the services root. They must reference `../services.css` and `../../blog/blog.css`. Mitigation: define CSS paths carefully in each page's `<head>` and verify during implementation.

## Open Questions

- Should the services index page also be linked from the homepage hero or body section (not just the nav)? This could be a future enhancement once the pages are live.
- Does the Formspree account need a separate form per service (for separate notification routing), or is a single form with a `service` field sufficient? Current design assumes one shared endpoint with the hidden field. If separate routing is needed, five Formspree form IDs will be required.

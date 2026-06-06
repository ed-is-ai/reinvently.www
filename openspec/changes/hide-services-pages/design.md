## Context

The services pages (`/services/` and all sub-pages) were built as part of the `service-pages` change but are not ready for public release. They are currently live static HTML files with canonical URLs, OG tags, and no indexing restrictions. The site nav includes a "Services" link that routes visitors directly to them.

## Goals / Non-Goals

**Goals:**
- Remove the Services nav link so visitors cannot navigate to services pages
- Add `noindex, nofollow` to all services pages so search engines do not index them
- Remove any in-page links from other pages (e.g. homepage) pointing to `/services/`

**Non-Goals:**
- Deleting the services page files (kept for future re-launch)
- Password-protecting or 403-ing the pages (direct URL access is acceptable)
- Modifying page content or structure beyond the meta tag addition

## Decisions

**`noindex, nofollow` meta tag over robots.txt disallow**
Adding `<meta name="robots" content="noindex, nofollow">` to each HTML file is the most targeted approach — it affects only services pages without touching site-wide crawl rules. A `robots.txt` `Disallow` would also work but is a hint, not an instruction; meta `noindex` is the definitive signal to search engines.

**Remove nav link, not redirect**
The pages remain at their URLs (no redirect to homepage). The goal is to stop accidental discovery and indexing — not to break any bookmarked URLs. A redirect would be more disruptive and is unnecessary while the pages are just being temporarily hidden.

## Risks / Trade-offs

- **Indexed pages may remain in Google Search temporarily** → Google re-crawls on its own schedule; `noindex` will take effect on next crawl (typically days to weeks). No further action needed.
- **Direct URL still accessible** → Acceptable; no sensitive information is on these pages and the requirement is only to hide them from navigation and search.

## Migration Plan

1. Edit `index.html` — remove the `<a href="/services/">Services</a>` nav link
2. Edit each services HTML file — add `<meta name="robots" content="noindex, nofollow">` inside `<head>`
3. Verify no other pages link to `/services/`
4. Deploy (git commit + push)

Rollback: revert the commit.

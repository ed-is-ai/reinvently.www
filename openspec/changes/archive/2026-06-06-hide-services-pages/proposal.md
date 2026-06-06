## Why

The services pages are not ready for public release and must not be visible to site visitors or indexed by search engines. Removing them from navigation and blocking indexing ensures no unfinished content reaches the audience.

## What Changes

- Remove the "Services" link from the main site navigation
- Add `noindex, nofollow` meta tags to all services pages (`/services/`, `/services/strategy/`, `/services/pilot/`, `/services/accelerate/`, `/services/build/`, `/services/first-aid/`, `/services/scale/`, `/services/sdlc-enablement/`)
- Remove any homepage or other in-page links pointing to `/services/`

## Capabilities

### New Capabilities

- `services-hidden`: Services pages are de-linked from navigation and marked noindex so they are inaccessible via normal browsing and excluded from search engine indexes

### Modified Capabilities

- `nav-services-link`: The nav link to services is removed (previously added in the service-pages change)

## Impact

- [index.html](index.html): Remove Services nav link
- [services/index.html](services/index.html) and all sub-pages: Add noindex meta tag
- No dependencies, APIs, or build tools affected — all changes are static HTML edits

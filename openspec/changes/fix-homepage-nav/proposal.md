## Why

The Services nav link added to the homepage via script injection renders in the wrong position — it appears as a floating label in the top-left corner of the hero image rather than alongside other navigation links. The root cause is that `navBarId-18199` (the injection target) sits inside the website-builder's full-bleed hero overlay, not in a conventional nav bar position. The script approach cannot reliably place links in this structure.

## What Changes

- Remove the existing script injection from `index.html` that appends a Services link to `navBarId-18199`
- Add a `position: fixed` custom nav bar to the homepage, inserted at the top of `<body>` with a high `z-index`, styled to match the blog page nav (dark background, Reinvently logo left, links right)
- The fixed nav overlays the website-builder header cleanly without touching its internal structure
- Nav contains: Reinvently (logo, links to `/`), Blog (links to `/blog/`), Services (links to `/services/`)

## Capabilities

### New Capabilities

- `homepage-nav-bar`: A fixed custom nav bar on the homepage at `position: fixed; top: 0; z-index: 9999` — visually identical to the blog page nav, inserted as the first child of `<body>`

### Modified Capabilities

- `nav-services-link`: Homepage now delivers the Services link via the fixed nav bar rather than via script injection into `navBarId-18199`

## Impact

- Modified: `index.html` — remove injection script block, add inline `<style>` for nav, add `<nav>` element at top of `<body>`, add `padding-top` to push website-builder content below the fixed bar
- No changes to blog pages or service pages (their nav is already correct)
- The website-builder's own "REINVENTLY" logo in the hero remains intact — it becomes a decorative hero element; the fixed nav provides the functional navigation layer

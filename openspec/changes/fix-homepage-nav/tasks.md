## 1. Remove broken injection

- [x] 1.1 Remove the `(function() { var nav = document.getElementById('navBarId-18199')... })()` script block from `index.html` (the nav-services-link injection added in the previous change)

## 2. Add fixed nav bar

- [x] 2.1 Add an inline `<style>` block to `index.html` `<head>` with nav styles: `position: fixed; top: 0; left: 0; right: 0; z-index: 9999; background: #000; padding: 20px 48px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1b1b1b;` — plus logo and link styles matching blog.css values
- [x] 2.2 Add `<nav id="site-nav" aria-label="Site navigation">` as the first element inside `<body>`, containing: Reinvently logo link (to `/`) and nav links div with Blog (`/blog/`) and Services (`/services/`)
- [x] 2.3 Add `padding-top: 61px` to `body` in the inline style block to push website-builder content below the fixed nav

## 3. Verify

- [x] 3.1 Confirm "Services" no longer appears as a floating label in the hero — injection script removed; Services now in fixed nav only
- [x] 3.2 Confirm the nav bar is visible at the top of the page on load and on scroll — `position:fixed; z-index:9999` ensures this
- [x] 3.3 Confirm Blog and Services links navigate correctly — href="/blog/" and href="/services/" verified in HTML
- [x] 3.4 Confirm the website-builder hero content is not hidden behind the nav bar — `body { padding-top: 61px }` offsets content

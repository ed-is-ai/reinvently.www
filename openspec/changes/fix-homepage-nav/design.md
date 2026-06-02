## Context

The homepage (`index.html`) is a minified GoDaddy Airo website-builder export. Its header is a full-bleed hero section rendered by the website-builder's JavaScript. The website-builder's own nav only shows a centered "REINVENTLY" logo — it has no nav links. A previous attempt to inject a "Services" link via script into `navBarId-18199` failed because that container sits inside the hero overlay, rendering the link as a floating label in the top-left corner.

All blog and service pages use a hand-crafted `<nav class="nav">` element styled by `blog/blog.css`, which works correctly. The homepage has no equivalent.

## Goals / Non-Goals

**Goals:**
- A correctly positioned nav bar on the homepage with links to Blog and Services
- Visual consistency with the blog/services nav (same dark theme, Montserrat caps, spacing)
- No structural changes to the website-builder's HTML

**Non-Goals:**
- Redesigning the homepage hero or website-builder layout
- Adding the nav to the website-builder's internal structure
- Making the website-builder nav responsive or interactive beyond what the custom nav provides

## Decisions

**D1: Fixed-position nav bar overlaid on the homepage**

Insert a `<nav id="site-nav">` as the first child of `<body>`, styled `position: fixed; top: 0; left: 0; right: 0; z-index: 9999`. A `padding-top` equal to the nav height (61px — matching blog.css `padding: 20px 48px` with 21px line-height for the logo text) is applied to the `<body>` or the first layout div to push content below the fixed bar.

The fixed approach is the only reliable method for a website-builder page where we cannot surgically edit the header structure. It is also the correct pattern for this site — the hero is decorative and full-bleed, so a fixed nav that overlays it matches the visual intent.

Alternative considered: absolutely positioned nav inside the hero. Rejected — the hero has a complex z-index stack from the website-builder; an absolute element inside it may be obscured by the builder's JavaScript-managed layers.

**D2: Inline `<style>` block in `<head>`, not a new CSS file**

The nav styles are inlined directly in `index.html` rather than linked to a new file, for two reasons:
1. The homepage already carries all its styles inline or via the website-builder JS; adding another HTTP request for a tiny nav stylesheet is unnecessary
2. The nav styles are a verbatim copy of the `.nav`, `.nav-logo`, and `.nav-links` rules from `blog/blog.css` — duplicating them inline is cleaner than importing all of `blog.css` (which would risk conflicting with the website-builder's own CSS)

The inline style block uses the same CSS variable values hardcoded (not `var()`) since `blog.css` is not loaded on the homepage.

**D3: Remove the injection script entirely**

The `(function() { var nav = document.getElementById('navBarId-18199')... })()` script block is removed. It produced a visible defect and has been superseded by the fixed nav approach.

**D4: Nav contents — Reinvently · Blog · Services**

Matching the blog nav pattern exactly:
- Left: `.nav-logo` — "Reinvently" in Montserrat 700, letter-spacing 4px, uppercase, links to `/`
- Right: `.nav-links` — "Blog" links to `/blog/`, "Services" links to `/services/`
- No "Home" link (redundant on the homepage itself)

## Risks / Trade-offs

- **Website-builder JS may render after our nav** → Fixed-position with `z-index: 9999` ensures our nav stays above all website-builder layers regardless of render order
- **Padding-top on body may interact with website-builder's fixed-position elements** → The website-builder header is not `position: fixed` (it's part of normal flow); `padding-top: 61px` on `body` will push all content down by the nav height without affecting the fixed nav itself
- **Font not loaded on homepage** → The nav uses Montserrat. The homepage already loads Montserrat via the website-builder's own font loading (confirmed by `x-fonts-montserrat` class on `<body>`). The inline style falls back to `sans-serif` if needed.

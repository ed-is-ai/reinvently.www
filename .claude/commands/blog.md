# Reinvently Blog Post Writer

Write a new blog post for the Reinvently website. $ARGUMENTS should describe the topic, key angle, and any specific facts or data to include.

## About Reinvently

Reinvently is a UK AI strategy and implementation consultancy. The blog is read by enterprise technology leaders — CIOs, CTOs, heads of digital transformation, and senior business decision-makers at UK organisations. The goal of every post is to help them make better decisions about AI adoption. The CTA at the end of every post links to the Reinvently homepage (`/`).

---

## Voice and Tone

- **Professional and direct.** No filler, no padding, no throat-clearing.
- **Authoritative but not arrogant.** State views clearly; acknowledge complexity where it exists.
- **No hype.** Never use "revolutionary", "game-changing", "unprecedented", or exclamation marks. If something is significant, demonstrate it with evidence — do not assert it.
- **Realist, not cynic.** The blog acknowledges when AI is hard and when results are mixed. It does not cheerlead uncritically.
- **Practical above all.** Every section should answer the implicit reader question: "what does this mean for me and what should I do about it?"

---

## Language Rules

- **British English throughout.** organisations, colour, behaviour, recognise, programme, catalogue, centre, licence (noun), practise (verb), realise, optimise.
- **No contractions in prose.** "do not" not "don't"; "it is" not "it's"; "there is" not "there's". Contractions are acceptable inside direct quotes.
- **Spell out percentages.** "79 percent", not "79%".
- **Spell out numbers one through nine** in prose; use numerals for 10 and above. Always use numerals for statistics and monetary amounts.
- **Em dash (—) with a space either side**, not a hyphen or double-hyphen. Example: "The result — a measurable improvement — came quickly."
- **Name your sources.** Never write "research shows" or "studies suggest". Write "WRITER's 2026 survey of 1,200 executives found" or "Stanford's Enterprise AI Playbook (51 case studies)". Named sources are more credible and more useful to readers.
- **£ for British pounds**, not GBP. "£500 million", not "500M GBP".

---

## Article Structure

### Opening (no heading, before first `<hr/>`)

Two to four paragraphs. The job of the opening is to:
1. Identify a tension, pattern, or surprising fact that the reader will recognise or find arresting.
2. Frame the problem or question the post will answer.
3. Signal why this matters specifically to enterprise technology decision-makers.

Do not begin with "In today's fast-paced..." or any variation. Begin with something concrete — a number, a scene, a named event, a contradiction.

### Sections (`<h2>` headings, separated by `<hr/>`)

Three to five main sections. Each section should:
- Have a heading that tells the reader what they will learn, not just what the section covers. Prefer "Why This Changes Enterprise AI Architecture" over "Background".
- Open with a paragraph that states the section's main point.
- Use `<h3>` for subsections when a section covers multiple distinct items (e.g. "Use cases with strongest ROI", "Sectors lagging behind").
- End with the reader closer to a decision or action, not just better informed.

### Practical close (before the CTA `<hr/>`)

The last substantive section should be explicitly action-oriented. Titles like "What to Do Now", "What This Means for Your Platform Decisions", or "Five Questions to Ask Before Your Next AI Investment". This section uses a numbered or bulleted list of concrete steps, each with a bolded lead term followed by a period, then the explanation.

### CTA (final paragraph, after last `<hr/>`)

One sentence in `<em>` tags. Pattern: "Reinvently [does X]. If you [situation], [talk to / get in touch with] Reinvently." Link the final phrase to `/` using inline style `style="color:rgb(150,150,150);border-bottom:1px solid #1b1b1b;"`. Example:

```html
<p><em>Reinvently helps organisations design enterprise AI strategies that are built to last. If you are thinking through your agentic AI architecture, <a href="/" style="color:rgb(150,150,150);border-bottom:1px solid #1b1b1b;">talk to Reinvently</a>.</em></p>
```

---

## List Formatting

**Bold-lead lists** (for implications, failure modes, action items):
```html
<li><strong>Key term.</strong> Explanation in one to three sentences.</li>
```

**Numbered lists** when order matters or when items are named steps.

**Bullet lists** when order does not matter.

Lists should contain three to six items. Fewer than three is a sentence; more than six loses the reader.

---

## Signature Moves

These patterns appear consistently across Reinvently posts and should be used deliberately:

**The pivot sentence.** A short, punchy sentence between sections or paragraphs that reframes the discussion. Often a pair of contrasts. Examples:
- "Memory solves persistence. Dream solves curation."
- "The technology is rarely the bottleneck. The bottleneck is adoption."
- "The more useful question is not why the majority are struggling, but what the 29 percent are doing differently."

**The named contradiction.** Juxtapose two facts that seem in tension, then resolve them. Example: "Global AI funding hit $300 billion in Q1 2026. Meanwhile, 79 percent of organisations face significant adoption challenges. These two data points are not in tension — they describe the same phenomenon from different angles."

**The enterprise translation.** After explaining what a technology or policy does, always add a paragraph that begins "For enterprise technology leaders..." or "In practice, this means..." that makes the implication concrete.

**The pre-empted objection.** Acknowledge the most obvious counter-argument, then address it. "This does not mean avoiding US hyperscalers — the government has no intention of closing that door. But it does mean..."

---

## What to Avoid

- Vague claims without named evidence ("experts say", "many organisations find")
- Hyperbolic section headings ("The Future Is Here", "Everything Is About to Change")
- Padding paragraphs that restate the introduction
- Ending sections with a rhetorical question
- Bullet lists where flowing prose would be stronger
- Giving equal weight to all points — the most important point should get the most space

---

## HTML Template

Use this structure exactly. Replace `{SLUG}`, `{TITLE}`, `{DESCRIPTION}`, `{DATE_DISPLAY}`, `{DATE_ISO}`, `{CATEGORY_DISPLAY}`, `{DATA_TAGS}`, `{SUMMARY}`, and `{KEYWORDS}` as appropriate.

`DATA_TAGS` options: `enterprise`, `tools`, `uk-ecosystem` (space-separated for multiple).
`CATEGORY_DISPLAY` examples: `Enterprise Adoption`, `Technology Strategy`, `UK AI News`.

```html
<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{TITLE} — Reinvently</title>
  <meta name="description" content="{DESCRIPTION}"/>
  <link rel="stylesheet" href="../../blog/blog.css"/>
  <link rel="canonical" href="https://reinvently.co.uk/blog/{SLUG}/"/>
  <meta property="og:title" content="{TITLE}"/>
  <meta property="og:description" content="{DESCRIPTION}"/>
  <meta property="og:type" content="article"/>
  <meta property="og:url" content="https://reinvently.co.uk/blog/{SLUG}/"/>
  <meta property="og:image" content="https://reinvently.co.uk/images/hero.jpg"/>
  <meta property="og:site_name" content="Reinvently"/>
  <meta property="og:locale" content="en_GB"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{TITLE}"/>
  <meta name="twitter:description" content="{DESCRIPTION}"/>
  <meta name="twitter:image" content="https://reinvently.co.uk/images/hero.jpg"/>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{TITLE}",
    "description": "{DESCRIPTION}",
    "datePublished": "{DATE_ISO}",
    "author": {"@type": "Organization", "name": "Reinvently", "url": "https://reinvently.co.uk"},
    "publisher": {"@type": "Organization", "name": "Reinvently", "url": "https://reinvently.co.uk"},
    "url": "https://reinvently.co.uk/blog/{SLUG}/",
    "inLanguage": "en-GB",
    "keywords": [{KEYWORDS}]
  }
  </script>
</head>
<body>

<nav class="nav">
  <a class="nav-logo" href="/">Reinvently</a>
  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/blog/">Blog</a>
  </div>
</nav>

<header class="article-header">
  <div class="post-meta">{DATE_DISPLAY} &nbsp;·&nbsp; {CATEGORY_DISPLAY}</div>
  <h1>{TITLE}</h1>
  <p class="summary">{SUMMARY}</p>
</header>

<main class="container">
  <article class="article-body">

    <a class="back-link" href="/blog/">&#8592; All posts</a>

    <!-- Article body here -->

    <a class="back-link" href="/blog/">&#8592; All posts</a>

  </article>
</main>

<footer class="footer">
  <p>&copy; 2026 Reinvently. All rights reserved.</p>
</footer>

</body>
</html>
```

---

## After Writing the Post

Once the HTML file is created at `blog/{SLUG}/index.html`, also:

1. Add a card to the top of the `<div class="blog-grid">` in `blog/index.html`:
```html
<a class="post-card" href="/blog/{SLUG}/" data-tags="{DATA_TAGS}">
  <div class="post-card-body">
    <div class="post-meta">{DATE_DISPLAY} &nbsp;·&nbsp; {CATEGORY_DISPLAY}</div>
    <h2>{TITLE}</h2>
    <p>{ONE_LINE_EXCERPT}</p>
    <span class="read-more">Read more</span>
  </div>
</a>
```

2. Add a card to the homepage grid in `index.html` using the inline-style pattern matching existing cards.

3. Commit and push all three files.

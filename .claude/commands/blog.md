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

## Article Structures

Choose the structure that best fits the topic. Do not default to the same one every time — vary across posts so the blog does not feel formulaic.

---

### Structure A: The Explainer (for new technology or concepts)

Best for: protocol announcements, new model releases, feature launches the reader needs to understand before they can evaluate.

1. **Opening** — A concrete hook: what changed, when, and why a busy executive should care. Two to three paragraphs.
2. **What it is / how it works** — Clear, jargon-free explanation. Use an analogy if helpful. Avoid over-technicalising.
3. **Why it matters for enterprise** — The "so what" section. Explicit translation from technical fact to business implication.
4. **What changes about how you make decisions** — Practical consequences: procurement, architecture, governance, team structure.
5. **What to do now** — Three to five concrete steps, bold-lead list format.
6. **CTA**

---

### Structure B: The Evidence Review (for research findings, survey data, market analysis)

Best for: adoption surveys, ROI studies, sector analyses, benchmark reports.

1. **Opening** — Lead with the most arresting data point. Frame the tension between the headline number and what it means in practice.
2. **What the data says** — Summarise the research with named sources. Do not paraphrase vaguely — quote specific figures and attribute them precisely.
3. **What it does not say** — Acknowledge limitations, counterpoints, or what the data cannot tell us. This builds credibility.
4. **What separates the leaders from the laggards** — The actionable insight extracted from the evidence.
5. **A framework for decision-makers** — A structured set of questions, criteria, or steps derived from the evidence. Can be a numbered list or `<h3>`-led subsections.
6. **CTA**

---

### Structure C: The Policy Brief (for regulation, government announcements, legal developments)

Best for: ICO guidance, parliamentary inquiries, government investment programmes, regulatory consultations.

1. **Opening** — Name the development, date it, and explain in plain terms what changed. Assume the reader has not read the source document.
2. **What was actually announced / decided** — Factual summary. Bullet list if multiple distinct elements. No editorialising yet.
3. **Who it affects and how** — Segment by organisation type, sector, or role where relevant. Use `<h3>` for each segment if the implications differ significantly.
4. **What "compliance" actually looks like** — Practical translation: not "you must ensure meaningful human involvement" but "this means your CV-screening tool needs a human reviewer who can see the underlying data, not just the AI's output."
5. **What to do before this becomes enforcement** — Audit steps and preparation checklist.
6. **CTA**

---

### Structure D: The Contrarian Take (for challenging received wisdom or reframing a debate)

Best for: "the real reason X is failing", "why everyone is thinking about Y wrong", sceptical takes on hype.

1. **Opening** — State the conventional wisdom clearly, then signal you are going to challenge it. Do not bury the lede.
2. **Why the conventional view is understandable** — Steel-man the position you are pushing back on. This signals intellectual honesty and makes the argument more persuasive.
3. **What the evidence actually shows** — The counter-argument, with named evidence.
4. **The more useful frame** — Offer a replacement mental model, not just a critique of the existing one.
5. **Implications if you adopt this frame** — Concrete consequences for decisions, priorities, or strategy.
6. **CTA**

---

### Structure E: The Decision Guide (for "should we do X?" questions)

Best for: platform comparisons, build-vs-buy decisions, vendor evaluation, "is this the right time?" questions.

1. **Opening** — Frame the decision. Who is making it, what are the stakes, why is it genuinely difficult.
2. **What you are really choosing between** — Clarify the decision space. Often the stated question ("should we use X or Y?") conceals a more fundamental question ("are we optimising for speed or control?").
3. **The case for each option** — `<h3>` per option. Evidence-led, honest about downsides.
4. **The factors that should drive your decision** — Not a recommendation, but a framework: "if A is true for your organisation, lean toward X; if B, lean toward Y."
5. **Common mistakes** — Two to three things organisations get wrong when making this decision.
6. **CTA**

---

### All structures share these rules for opening and sections:

**Opening:** Do not begin with "In today's fast-paced..." or any variation. Begin with something concrete — a number, a scene, a named event, a named contradiction. Two to four paragraphs before the first `<hr/>`.

**Section headings (`<h2>`):** Tell the reader what they will learn, not just what the section covers. Prefer "Why This Changes Enterprise AI Architecture" over "Background". Prefer "The Three Reasons Deployments Fail" over "Challenges".

**Each section:** Opens with a paragraph that states the main point. Uses `<h3>` for subsections when covering multiple distinct items. Ends with the reader closer to a decision, not just better informed.

### CTA (final paragraph, after last `<hr/>`)

One short italic paragraph. It should feel like a natural continuation of the post — a quiet offer, not a sales pitch. The goal is to give a reader who found the post useful a frictionless way to continue the conversation. It must not sound like an advert.

**Rules:**
- Do not use "leading", "cutting-edge", "best-in-class", or any superlative about Reinvently.
- Do not promise outcomes ("we'll help you achieve X", "transform your AI strategy").
- Do not use the word "leverage".
- The sentence should read as if written by a thoughtful person, not a marketing team.
- Vary the phrasing across posts — do not use the same sentence structure every time.

**The link** goes to `/` with inline style `style="color:rgb(150,150,150);border-bottom:1px solid #1b1b1b;"`.

**Tones to rotate between:**

*Contextual offer* — connects directly to the post's subject:
```html
<p><em>If you are working through what agentic AI governance looks like in practice, <a href="/" style="color:rgb(150,150,150);border-bottom:1px solid #1b1b1b;">Reinvently</a> is worth a conversation.</em></p>
```

*Understated credential* — states what Reinvently does without overselling:
```html
<p><em>Reinvently works with UK organisations on the strategy and implementation side of AI adoption — the parts that determine whether a deployment actually delivers. <a href="/" style="color:rgb(150,150,150);border-bottom:1px solid #1b1b1b;">Get in touch</a> if that is useful.</em></p>
```

*Reader-first* — frames the offer around the reader's situation, not Reinvently's services:
```html
<p><em>Most of the organisations we speak to are somewhere in the middle of this — past the pilot stage but not yet seeing the returns they expected. If that sounds familiar, <a href="/" style="color:rgb(150,150,150);border-bottom:1px solid #1b1b1b;">we are happy to talk it through</a>.</em></p>
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

## Avoiding AI Writing Patterns

These are the most recognisable tells of AI-generated text. Treat this list as a hard blacklist — if any of these appear in a draft, rewrite the sentence.

### Banned words and phrases

Never use these words in Reinvently posts:

**Significance inflation:** "pivotal", "testament to", "stands as", "indelible mark", "milestone", "landmark", "game-changer", "transformative" (unless quoting someone else using it ironically)

**Vague intensifiers:** "crucial", "vital", "key" (as a standalone adjective — "key takeaway", "key challenge"), "essential" (when not literally meaning required for survival)

**AI-era filler:** "delve", "delve into", "intricate", "meticulous", "groundbreaking", "cutting-edge", "state-of-the-art", "robust" (in the sense of "strong"), "leverage" (as a verb)

**Marketing register:** "vibrant", "nestled", "showcasing", "fostering", "commitment to", "rich heritage", "tapestry", "dynamic", "bespoke" (unless literally meaning made-to-measure)

**Hollow transition words:** "Additionally," at the start of a paragraph, "Furthermore,", "Moreover," — these pad word count and signal AI. Use them only mid-sentence when they add genuine meaning.

**Copula avoidance:** Do not replace "is" or "are" with "serves as", "marks", "represents", "features", "boasts", or "maintains" just to avoid repeating a verb. If something *is* something, say it is.

### Banned sentence structures

**"Not just X, but Y"** — Almost always padding. Either X is sufficient or it is not. Cut the hedge.
> ❌ "This is not just a technical change, but a fundamental shift in how enterprises think about AI."
> ✅ "This changes how enterprises think about AI."

**"It is worth noting that..."** — If it is worth noting, note it. Do not announce that you are noting it.

**The rule of three for its own sake** — "fast, reliable, and scalable" / "clear, concise, and actionable" — only use three-part constructions when the three parts are genuinely distinct and all necessary.

**Unearned significance openers** — Do not begin a section by announcing that something is significant, important, or worth paying attention to. Demonstrate significance; do not declare it.
> ❌ "This is a significant development for enterprise technology leaders."
> ✅ [State what it actually changes, specifically.]

**Vague future optimism** — Do not end sections with "as AI continues to evolve...", "in the coming months and years...", or "the future looks promising for...". End with something specific or do not speculate.

**"Sparked debate" / "generated discussion"** — Name the debate and the specific parties to it, or remove the claim.

### Structural patterns to avoid

- Do not open every section with a sentence that restates the section heading in different words.
- Do not use bold text for every instance of a key term — bold is for things the reader must not miss, not for decoration or the appearance of structure.
- Do not use `<h3>` subsections for every section — reserve them for sections genuinely covering multiple distinct sub-topics. A single h3 under an h2 is almost always unnecessary.
- The "challenges and opportunities" section structure — listing obstacles and then pivoting to vague optimism — reads as AI-generated boilerplate. Replace it with a specific, evidenced analysis of what actually makes something difficult and what specifically reduces that difficulty.

### On em dashes

The blog uses em dashes (—) for genuine parenthetical asides. Do not use them as a mechanical habit. A paragraph with more than one em dash pair is a sign of over-reliance. If you find yourself reaching for an em dash, check whether a comma, a full stop, or a colon would be more precise.

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

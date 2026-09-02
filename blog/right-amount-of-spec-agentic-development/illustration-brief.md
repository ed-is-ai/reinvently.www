# Illustration brief: How Much Specification Do Coding Agents Need?

**Article:** *How Much Specification Do Coding Agents Need? What the Research Actually Supports*
**Draft:** `draft.md`
**Visual system:** One editorial hero plus three explanatory diagrams. The visuals should clarify the argument, not imply that an unmeasured relationship has been quantified.

## Shared art direction

- Match Reinvently’s restrained editorial style: charcoal or near-black background, fine grey structures, off-white type and one controlled green accent for verified or production-ready states.
- Use amber for unresolved ambiguity and muted red only for rework, failure or risk.
- Avoid humanoid robots, glowing brains, chat bubbles, circuit-board clichés and screenshots of branded tools.
- Keep diagrams flat and precise. Use generated raster artwork only for the hero; build labelled inline diagrams as SVG so text remains sharp, accessible and editable.
- Design for mobile first. Every diagram must remain intelligible at approximately 360 pixels wide.
- Do not encode meaning by colour alone. Pair every colour change with a label, shape or line treatment.
- Prefer sentence case. Keep labels short and use the article’s terminology exactly.
- The hero should work without text so the title can remain HTML. Inline diagrams may contain the labels specified below.

## Visual 1: Ambiguity expands; verification constrains

### Purpose

Establish the central tension before the reader reaches the evidence: agents can expand a small instruction into a large implementation quickly, but that output must still pass through a constrained verification and release system.

### Placement and format

- Hero image, immediately after the standfirst.
- Master size: 1200 × 630 pixels.
- Also allow a centre-safe 1:1 crop and a 4:3 crop.
- Deliver WebP and high-quality JPEG; preserve the layered source.

### Composition

Use a left-to-right flow with three visually distinct states:

1. On the left, a small amber, slightly blurred instruction block represents unresolved intent.
2. In the centre, that block expands rapidly into many fine wireframe branches, modules or connected code-like structures. The expansion should feel fast and impressive, but not chaotic.
3. On the right, the branches converge through a narrow gate made of checks, boundaries and alignment marks. Only a smaller, coherent green structure emerges towards production.

The gate is the focal point. It should suggest tests and verification without using literal tick-box clip art. A few branches may loop back from the gate towards the centre to imply correction and rework.

### Text inside image

None. The visual must support the HTML title rather than duplicate it.

### Caption

Coding agents can expand ambiguous intent into implementation faster than a delivery system can verify it. Specification and executable checks make the narrowing step cheaper and more reliable.

### Alt text

A vague instruction expands into many branches of generated code, which narrow through a verification gate into one production-ready release.

### Generation prompt

> Abstract editorial technology illustration for a serious research article, 1200 by 630 landscape. On the left, one small softly blurred amber instruction block. It rapidly expands across the centre into a complex but elegant network of fine wireframe software modules and branching structures. On the right, the network converges through a narrow precise verification gate made from geometric alignment marks and test-like boundaries. A smaller coherent green structure emerges beyond the gate. A few muted red paths loop back to suggest rework. Charcoal background, off-white and grey line work, restrained amber and green accents, sophisticated data-visualisation aesthetic, generous negative space, crisp geometry, no words, no logos, no people, no robots, no glowing brain, no photorealism.

### Production cautions

- The emerging production structure should be smaller and more coherent, not visually inferior.
- Do not imply that most generated code is necessarily rejected; the narrowing represents delivery stages, not a measured rejection percentage.
- Keep the important gate and output inside the centre-safe crop.

## Visual 2: The minimum-total-cost curve

### Purpose

Make the article’s optimisation argument immediately legible: too little specification creates ambiguity and correction cost, while too much creates ceremony and stale-context cost. The preferred region minimises their total, but its position varies by task.

### Placement and format

- Place after “What the evidence establishes—and what it does not,” once the four evidence conclusions have been presented.
- Build as an accessible inline SVG with a 760 × 470 viewBox.
- Use a white or very pale plotting area on the site’s dark article background.

### Diagram

Plot three conceptual curves against a shared horizontal axis:

- A descending amber dashed curve: **Ambiguity, review and rework**.
- A rising grey dashed curve: **Upfront effort, ceremony and staleness**.
- A solid dark U-shaped curve: **Total delivery cost**.

At the bottom of the U, show a soft green vertical band rather than one exact point. Label it **Minimum sufficient contract**. Add a subtle double-headed arrow over the green band labelled **Moves with task risk and uncertainty**.

### Exact axis and annotation labels

- Chart title: **The useful optimum minimises total delivery cost**
- X-axis: **Specification effort and formality →**
- Y-axis: **Relative total cost →**
- Left region: **Correction loops dominate**
- Centre band: **Minimum sufficient contract**
- Right region: **Specification overhead dominates**
- Footnote inside the figure: **Conceptual model—not an experimentally estimated curve.**

Do not add numerical ticks, percentages or a fitted-looking confidence interval.

### Caption

Write enough specification to prevent expensive misunderstandings, but stop when more detail adds more work than it removes. The chart illustrates that trade-off; research has not measured a universal sweet spot.

### Alt text

A conceptual U-shaped curve shows total delivery cost falling as specification reduces ambiguity, then rising as documentation effort and staleness increase. A variable middle band is labelled minimum sufficient contract.

### Production cautions

- The disclaimer must remain visible at mobile size.
- Use a band, not a precise dot, so the image does not imply false measurement.
- The component curves are explanatory, not independently measured evidence.

## Visual 3: Project conditions determine the contract

### Purpose

Make the decision rule explicit: production risk increases rigour, while exploratory uncertainty changes the form of the specification.

### Placement and format

- Place immediately after the four-variable table.
- Build as an accessible inline SVG with a 760 × 520 viewBox.
- Provide a separate 1080 × 1080 export for social use.

### Composition

Use two spacious left-to-right **When → Then** rows beneath the heading **Match the contract to the project**.

The first **When** card groups three production-risk conditions:

- errors are costly;
- work crosses more handoffs; and
- failures are hard to detect.

Label the connecting arrow **More rigour**. It leads to the **Then** card, **Write a stronger contract**, containing tighter constraints, executable acceptance checks, and named owners and approval gates.

The second **When** card starts with **The outcome is uncertain**. Label its arrow **Clear boundaries**. It leads to **Write a boundary-led contract**, containing non-goals and constraints, evidence requirements, and stop-and-ask points.

End with a single dark-green bar: **Both belong in the minimum sufficient contract.**

### Caption

Costly, distributed or hard-to-check work needs stronger controls. Exploratory work needs clear boundaries if your agent is to know when it has finished the loop.

### Alt text

Costly errors, more handoffs and hard-to-detect failures point to a stronger contract. Uncertain outcomes point to a boundary-led contract. Together they define the minimum sufficient contract.

### Production cautions

- Keep the two rules visually separate. Do not imply that uncertainty simply means more detail.
- Avoid scales, dials or scientific instrumentation that imply a calculable score.
- Keep all body copy large enough to read when the article column is displayed at mobile width.

## Visual 4: From missing control to workflow framework

### Purpose

Create a useful transition into the existing framework comparison without reproducing its entire recommendation matrix. The diagram should place the options against two decisions: the rigour the specification requires and the breadth of control the team wants.

### Placement and format

- Place in “From principle to operating model,” immediately before the paragraph linking to the framework comparison.
- Build as an accessible inline SVG with a 760 × 520 viewBox.
- Make the whole figure or a clearly styled text link below it clickable in the final HTML.

### Composition

Use a two-axis matrix:

- Vertical: **Required specification rigour**, from **Targeted** to **Comprehensive**.
- Horizontal: **Desired scope of control**, from **One part of the workflow** to **Requirements to release**.

Place the frameworks as editorial orientations:

- **OpenSpec:** focused control and a targeted, formal change record.
- **GSD:** more rigorous planning and execution within the coding workflow.
- **GitHub Spec Kit:** a broader, portable specification workflow across coding tools.
- **BMAD:** comprehensive artefacts, roles and control across the lifecycle.

End the four branches in one green call-to-action bar:

**Compare the frameworks, trade-offs and project fit →**

Link destination:

`/blog/ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit/`

### Caption

Move up the chart as project risk demands more rigorous specifications; move right as the desired control expands from one part of the coding workflow towards the full delivery lifecycle.

### Alt text

Four workflow needs route to different specification frameworks: execution and context to GSD, lifecycle and roles to BMAD, governed change to OpenSpec, and a portable workflow to GitHub Spec Kit.

### Production cautions

- Present these as orientations for further comparison, not universal product recommendations.
- Give every route equal visual weight. Do not render one framework as the winner.
- Do not add volatile details such as star counts, prices or integration totals to the image.
- Preserve the exact framework names and capitalisation.

## Recommended production order

1. Build the cost curve first; it defines the article’s central conceptual language.
2. Build the four-variable model and test it at mobile width.
3. Build the framework bridge using the same card and arrow system.
4. Produce the hero last so its geometry echoes the finished inline diagrams.

This sequence will make the set feel like one visual argument rather than four unrelated assets.

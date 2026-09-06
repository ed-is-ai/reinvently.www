# How Much Specification Do Coding Agents Need? What the Research Actually Supports

**Draft status:** Editorial draft, not yet published
**Purpose:** A research-grounded companion to O’Reilly’s *The Right Amount of Spec for Agentic Development*, designed to lead readers into Reinvently’s practical framework comparison.
**Suggested standfirst:** Coding agents can write software quickly, but ambiguity comes back as review and rework. The evidence favours bounded tasks, clear acceptance criteria and verification that increases with risk.

<!-- HERO ILLUSTRATION: See illustration-brief.md, Visual 1. -->

## At a glance

- There is no evidence for an ideal specification length. The right amount depends on what could go wrong and how easily you would detect it.
- Give the agent enough direction to finish the work, and give the reviewer enough evidence to judge it.
- As work gets closer to production—or crosses more people, agents and systems—the specification needs stronger constraints, checks and ownership.

Coding agents can turn a loose goal into plausible code within minutes. That is not the same as delivering software faster. Reviewers still have to reconstruct the intended behaviour, find the missing cases and decide whether the result is safe to release.

A longer specification does not automatically solve this. It can contain contradictions, stale decisions and details already expressed more accurately in the code.

The question is:

> What does the agent need to finish the work, and what evidence will let us verify it?

The practical target is a **minimum sufficient contract**: enough information for the agent to finish the job and enough evidence for you to decide whether it succeeded. It also tells the agent when to stop and ask.

“Minimum” does not mean short. A reversible prototype may need only a goal, boundaries and a few criteria. Production work involving money, personal data or several agents may need schemas, failure behaviour, rollback and named approval. Every extra requirement should earn its place.

## What the evidence establishes—and what it does not

No controlled study tells us how many requirements, examples or acceptance criteria a coding agent needs. The “right amount” is still engineering judgement, not a measured formula.

The evidence does support four narrower conclusions.

### 1. AI accelerates code production more reliably than delivery

Reinvently’s [systematic review of 116 empirical studies](/blog/ai-coding-productivity-evidence/) found that controlled studies of conventional coding assistance generally report roughly 20–30% gains at the coding stage. Larger gains appear in bounded spec-driven and agent-native cases, but those lower-weight estimates bundle the model with changes to requirements, repositories, testing and team practice.

The strongest direct delivery study followed more than 100,000 developers. Its largest observed increase—180% more commits—became 30% more releases and no measured increase in application usage ([NBER working paper](https://www.nber.org/papers/w35275)). The study was observational, not randomised. It shows why specifications should give verification a stable target, but it does not isolate specification as the cause of higher output.

### 2. Clear tests can improve human judgement of generated code

The most direct evidence concerns executable clarification rather than long prose. In a 15-programmer study, TiCoder generated tests to clarify intent. Participants became better at judging whether generated code was correct and reported lower mental effort ([IEEE Transactions on Software Engineering](https://doi.org/10.1109/TSE.2024.3428972)). The study did not measure delivery throughput.

“Handle failed payments gracefully” sounds like a requirement, but it leaves the important decisions to the reviewer. Which failures? What should the customer see? Should the payment be retried? Tests, examples and named failure states turn those decisions into something that can be checked repeatedly.

Use executable criteria for behaviour that is stable and important. Leave questions that genuinely require judgement with a named person.

### 3. Bounded delegation can outperform conversational assistance

In a 24-developer brownfield-onboarding experiment, Copilot Agent reduced mean completion time by 61.7% relative to Copilot Ask and reduced reported workload, without a statistically significant correctness improvement ([PACIS 2026 paper](https://aisel.aisnet.org/pacis2026/ai_fow/ai_fow/13/)).

An expert-led workflow on the 1.52-million-line PicoScenes system reported 68.3% less implementation time, lower mean cyclomatic complexity and fewer defects ([ICSE 2026](https://doi.org/10.1145/3786583.3786872)). This single-system comparison used a bundled method. Together, the studies support bounded delegation—not longer specifications or a particular template.

### 4. Verification must scale with generation

More autonomous systems produce larger changes and more review work. Of 567 Claude Code pull requests, 83.8% were merged, but 45.1% of those changes still required human revision ([On the Use of Agentic Coding](https://doi.org/10.1145/3798166)). In another 12,433 agent-authored pull requests, specification mismatch and logic defects were the leading visible functional reasons for rejection ([Coding Agents in the Wild](https://doi.org/10.1109/access.2026.3696573)). Both studies were observational.

Automated review can help. A year-long Atlassian evaluation across more than 1,900 repositories associated an integrated review agent with a 30.8% reduction in pull-request cycle time, although the tool’s developer conducted the observational study ([ICSE 2026 paper](https://arxiv.org/abs/2601.01129)). It is still not an oracle.

Use machines for checks they can repeat. Bring people in as the consequences or need for judgement increase:

**Tests and static analysis** → **Automated review** → **Accountable human review**

- Reject defects that can be checked the same way every time.
- Catch routine issues before they consume a person’s attention.
- Keep a named human responsible where the consequences are serious or the answer depends on interpretation.

The minimum sufficient contract is not a fixed point. It varies with the needs and risks of the project.

<!-- INLINE ILLUSTRATION: See illustration-brief.md, Visual 2 — specification cost curve. -->

## The right amount of spec is a risk allocation decision

An agent does not need every fact about the product. It needs the facts that would otherwise cause an expensive or dangerous misunderstanding.

Four variables determine what the contract needs to contain:

| Variable | Less specification can work when… | More specification is justified when… |
|---|---|---|
| **Uncertainty** | The task is exploratory and the desired outcome is still being discovered. | The expected behaviour is stable and disagreement would create rework. |
| **Consequence of error** | The output is disposable, isolated and easy to reverse. | The change touches money, personal data, security, safety or regulated decisions. |
| **Delegation distance** | One engineer works with one agent in a tight feedback loop. | Work crosses sessions, people, agents, repositories or service boundaries. |
| **Observability** | A human can inspect the result cheaply and failures are obvious. | Correct-looking output can conceal logic, integration, performance or security defects. |

<!-- INLINE ILLUSTRATION: See illustration-brief.md, Visual 3 — project conditions to contract. -->

Specification should rise with project risk. An exploratory spike can be a one-shot exercise. Production work in a regulated domain such as financial services may need specifications and approvals that form part of the audit trail. A solo developer working with one agent sits at the opposite end of the spectrum from a medical-device company using an agentic swarm.

## A minimum sufficient contract

For most bounded feature work, a useful agent-facing specification has seven parts:

1. **Outcome.** What observable change should exist when the work is done?
2. **Context.** Which current behaviour, domain terms and repository conventions matter?
3. **Constraints.** What must remain true, including security, compatibility and performance boundaries?
4. **Non-goals.** What plausible adjacent work is deliberately outside scope?
5. **Acceptance criteria.** Which outcomes can be tested or inspected repeatably?
6. **Failure behaviour.** What should happen on invalid input, partial failure, timeout, retry or rollback?
7. **Open decisions.** Where must the agent stop and ask rather than infer?

The contract fixes the outcome and its boundaries, not the implementation.

Put each requirement where the agent can use it and the team can maintain it. Stable behaviour belongs in tests, types and schemas. Rationale and non-goals usually belong in prose. Do not copy an interface into three documents when the code already expresses it clearly; the copies will drift.

## Scale the specification by task type

### Exploratory work: specify boundaries and evidence

Do not ask an exploratory agent to deliver an answer you have not yet discovered. Tell it what question to investigate, which directions are out of bounds, what evidence to collect and when to stop.

The output is learning. Any code it produces is a probe until it passes a separate production review.

### Bounded feature work: specify outcomes and acceptance criteria

For a small feature or familiar integration, the product requirements document (PRD) just needs to define the visible outcome, important constraints, non-functional requirements and acceptance criteria. Include examples wherever two engineers could reasonably interpret the requirement differently.

Keep the change small enough for a person to understand and review.

### Deterministic or consequential work: make the contract executable

Financial transactions, migrations, security controls and data transformations justify more precision in the PRD. Specify invariants, failure handling and rollback. Alongside the PRD, start with a set of fixtures, integration tests and unit tests.

### Multi-agent work: specify the handoffs

Once several agents are working in parallel, vague boundaries become overlapping edits, incompatible assumptions and merge conflicts.

Define each handoff using SIPOC: supplier, input, process, output and customer. State who provides the input, what the agent receives and does, what it returns and who consumes the result. Then define how the output will be checked and what “good” looks like, so each handoff has a strong quality gate.

## Review the specification before implementation

Treat the specification as a quality gate. Confirm that it describes the intended outcome, resolves material ambiguity and uses acceptance criteria that test the right thing. An agent can identify gaps, but a person should approve any decision that changes the outcome or risk.

<!-- INLINE ILLUSTRATION: See diagram/error-compounding.svg. -->

An error introduced in the specification can compound into multiple errors in the code. Review the specification before implementation.

## The answer is spec-driven frameworks

Spec-driven frameworks help teams create the minimum sufficient contract. They also support engineers through the different stages of development. To choose one, match the rigour your specification needs with how your team prefers to work: on rails, or through a more ad hoc, individual approach. The more of the workflow you put on rails, the more repeatable the work becomes.

That places the four frameworks in different parts of the landscape:

- **OpenSpec** focuses on governing proposed changes without trying to run the whole lifecycle.
- **GSD** puts planning, execution and verification on rails while engineers retain the key decisions.
- **GitHub Spec Kit** standardises the path from principles and requirements through planning and implementation.
- **BMAD** provides the broadest lifecycle control across product, architecture, UX, development and testing.

The question is not which framework is most comprehensive. It is which missing control you need it to provide.

<!-- INLINE ILLUSTRATION: See illustration-brief.md, Visual 4 — framework bridge. -->

For the practical choice, see the full [comparison of GSD, BMAD, OpenSpec and GitHub Spec Kit](/blog/ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit/). It covers where these starting points overlap, how much ceremony they introduce, and which project settings suit each one.

## The practical rule

Coding agents have made software cheaper. The surrounding processes have not become cheaper by the same amount. You still need to specify the software, and the more complex the domain, the more rigorous the specification needs to be.

The agent needs enough direction to run and finish the loop. You need enough evidence to trust the result. That’s the sweet spot.

---

## Editorial/source notes

- Conceptual starting point: Markus Eisele, [“The Right Amount of Spec for Agentic Development”](https://www.oreilly.com/radar/the-right-amount-of-spec-for-agentic-development/), O’Reilly Radar, 17 July 2026. This draft develops an independent synthesis and does not reproduce its wording or structure.
- Evidence synthesis: Ed Yau, [“How Much Does AI Improve Software Development Productivity?”](/blog/ai-coding-productivity-evidence/), Reinvently, version 1.28.2. Numerical claims above retain the review’s distinctions among controlled effects, observational associations and low-weight case estimates.
- Intended next article: [“GSD, BMAD, OpenSpec, or GitHub Spec Kit: Choosing the Right AI Development Framework”](/blog/ai-dev-workflow-frameworks-gsd-bmad-openspec-speckit/).
- Before publication: add final publication metadata, select or commission a hero image, run site SEO/link/prose checks, and confirm that the evidence review version and study count have not changed.

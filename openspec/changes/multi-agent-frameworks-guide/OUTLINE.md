# Article Outline — Multi-Agent Orchestration Frameworks Compared

> Status: **DRAFT OUTLINE** (captured from `/opsx:explore`, 2026-06-06). Not yet written.
> Location: lives under `/guides` (decided 2026-06-06).
> Framing decision: **Landscape map by category**, not a flat ranking. The
> through-line is "**stars ≠ usefulness**" — the most-starred tool is the most criticised.
> Data gaps now closed (2026-06-06): recent star velocity computed, Aperant stall confirmed.
> Two findings reshaped the piece: (1) **ruflo is accelerating hard right now** (~549 stars/day
> recently vs 158 lifetime) even as its swarm features are panned — sharpens the thesis;
> (2) **Aperant has collapsed/stalled** (~5.5/day, no commits ~2.5 months) → reposition as a
> cautionary tale, and use it to demonstrate *why you read the curve, not the lifetime average*.

---

## Working metadata (for the eventual index.html)

- **Slug:** `multi-agent-orchestration-frameworks-compared`
- **Title (working):** "Multi-Agent Orchestration Frameworks Compared: ruflo, Aperant, Sandcastle, Mission Control & Maestro"
- **Meta description (working):** "Five 'multi-agent' tools, four different shapes. A practical map of ruflo, Aperant, Sandcastle, Mission Control and Maestro — by popularity, use case, hosting, and what the community actually says."
- **Keywords:** multi-agent orchestration, AI coding agents, agent swarm, ruflo, Aperant, sandcastle, mission-control, Maestro, Claude Code orchestration
- **Schema:** BlogPosting + FAQPage (match existing comparison posts)
- **Locale:** en-GB

---

## Core thesis

"Multi-agent" is doing a lot of work as a label. These five tools share the word but
occupy **four different categories**. Comparing them flat (one feature table) misleads
readers. The useful move is a **landscape map** so readers self-select — then an honest
read on momentum and real-world reliability, where **GitHub stars turn out to be a poor
proxy for usefulness.**

---

## The landscape map (lead visual)

```
                    FLEET OPS / GOVERNANCE / SCALE
                              ▲
              ruflo ●         │         ● mission-control
        (swarms, memory,      │      (dashboard, spend,
         federation, CLI)     │       RBAC, monitoring)
   CODE / LIBRARY ───────────┼──────────── APP / GUI ─────▶
   FIRST                      │                    FIRST
           sandcastle ●       │      ● Maestro   ● Aperant
        (embed in your code,  │   (keyboard      (autonomous
         programmatic API)    │    command       coding,
                              ▼    center)        Kanban)
                   HANDS-ON CODING (SOLO / PARALLEL DEV)
```

Four categories:
1. **Library / primitive** — sandcastle
2. **Desktop coding orchestrators** — Maestro, Aperant
3. **Fleet ops / governance dashboard** — mission-control
4. **Swarm meta-harness / platform** — ruflo

Honest caveat to state up front: sandcastle vs Maestro vs Aperant is a *real* bake-off;
mission-control vs ruflo is a *different* conversation; library-vs-swarm is category error.

---

## Data table (verified 2026-06-06, GitHub API)

| Project | Stars | Age | Lifetime/day | **Recent/day** | Momentum | Forks (ratio) | Open issues | Last commit | License |
|---|---|---|---|---|---|---|---|---|---|
| ruvnet/ruflo | 58,116 | 368d | 158 | **~549** | 🚀 accelerating | 6,654 (11%) | 618 | today | MIT |
| AndyMik90/Aperant | 14,325 | 183d | 78 | **~5.5** | 💀 stalled | 1,930 (13%) | 359 | **Mar 23 (74d)** | AGPL-3.0 |
| mattpocock/sandcastle | 5,771 | 80d | 72 | ~26 | settling (healthy) | 575 (10%) | 64 | today | MIT |
| builderz-labs/mission-control | 5,199 | 113d | 46 | ~20 | settling | 900 (17%) | 16 | Jun 2 | MIT |
| RunMaestro/Maestro | 2,984 | 195d | 15 | ~4 | cooled, active dev | 317 (10%) | 112 | today | AGPL-3.0 |

How "recent/day" was derived (method note for credibility): GitHub stargazer-timestamp API,
last accessible page → most recent stars' dates → stars ÷ days span. ruflo's last page is
capped at the 40,000th star (2026-05-04); recent rate inferred from 18k stars gained in the
33 days since = ~549/day. All others read directly from their final stargazer page.

> RESOLVED: lifetime-average proxy was misleading (Aperant looked like the #2 riser at 78/day
> but is actually flatlined at ~5.5/day). Recent-vs-lifetime now captures curve shape. A
> star-history.com image embed (`api.star-history.com/svg?repos=...`) remains an optional
> *production visual*, not a data gap.

---

## Section-by-section structure

### 1. Hook / intro
- "Multi-agent" means five different things. Set up the map.
- Promise: by the end, reader knows which *category* they need, then which tool.

### 2. The popularity picture (your "rise in stars" angle)
- Open with the trap: lifetime stars/day lies. Aperant *looks* like the #2 riser (78/day
  average) but is actually flatlined at ~5.5/day — the average is just remembering a dead spike.
- **ruflo is the real rocket right now**: ~549 stars/day recently (18k in the 33 days since it
  crossed 40k on May 4) vs 158 lifetime → genuinely accelerating, not just an old incumbent.
- **sandcastle & mission-control**: classic launch hockey-stick now settling to a healthy
  cruise (~26 and ~20/day) — Matt Pocock's reputation and builderz's 17% fork ratio explain
  the early spikes.
- **Maestro**: small and cooled (~4/day) but shipping daily — a slow burn, not dead.
- **Aperant**: the cautionary curve — high cumulative stars, velocity collapsed, repo silent.
- Visual: recent-vs-lifetime bars (above), optionally a star-history.com embed.
- Key message: **read the curve, not the average.**

### 3. The honest headline: stars ≠ usefulness
- **ruflo** discussion #1666: "100% failure rate for swarm coordination," "agents
  self-report success when 89% actually fail," sync-DB blocking, users removing it.
  Augment Code's "wrapping the wrapper" critique. Ambition >> current reliability.
- Counterpoint: quieter tools (sandcastle, Maestro) earn trust by doing less, well.
- This is the EEAT spine of the piece — be fair, cite, don't dunk.

### 4. Category walkthroughs (the four buckets)
For each: what it is · who it's for · differentiator · hosting · community verdict.

- **Library/primitive — sandcastle**: `sandcastle.run()`, Docker/Podman/Vercel, offline,
  MIT. Embed orchestration in your own product/pipeline. Trusted, low-drama.
- **Desktop coding orchestrators — Maestro & Aperant**:
  - Maestro: keyboard-first, long unattended runs (claims 80% @ 12h), group chat, BYO-agent, AGPL. HN traction.
  - Aperant: most autonomous (plan→build→validate Kanban), requires Claude Pro/Max, setup friction ("Claude Code not found"), AGPL. **Stall confirmed** — no commits on any branch since Mar 23 (develop) / Feb 20 (main, = latest release), 359 open issues. Treat as cautionary tale / "evaluate liveness before adopting," not an active contender.
- **Fleet ops / governance — mission-control**: spend/RBAC/audit, framework-agnostic
  adapters (CrewAI, LangGraph, AutoGen, Claude SDK), SQLite `pnpm start`, only one with a
  managed business tier ($29/mo). Young, unproven at scale.
- **Swarm meta-harness — ruflo**: 100+ agent swarms, HNSW memory, self-learning,
  federation, plugin marketplace, multi-provider. Biggest mindshare, reliability questioned.

### 5. Hosting & operational requirements (your angle, consolidated table)
| Tool | Form | Runs where | Notable requirement |
|---|---|---|---|
| sandcastle | TS library | your containers (Docker/Podman/Vercel) | embed in code; offline-capable |
| Maestro | Desktop app | local | bring-your-own agent CLI |
| Aperant | Desktop app | local | **Claude Pro/Max subscription** |
| mission-control | Self-hosted dashboard | your server | SQLite only — no Redis/PG/Docker; optional managed |
| ruflo | CLI meta-harness | local + optional federation | vector memory; heaviest footprint |

### 6. "How to choose" (buyer's guide payoff — matches house style)
- *Embedding orchestration in a product?* → sandcastle
- *Solo dev parallelising many local projects?* → Maestro
- *Want hands-off autonomous feature delivery on a Claude sub?* → Aperant's *design* fits, but it's stalled — check repo liveness first, or treat as a reference design
- *Team needing to govern spend/access across a fleet?* → mission-control
- *Chasing swarm scale + cross-agent memory, tolerant of rough edges?* → ruflo (pilot, don't bet)

### 7. FAQ (FAQPage schema)
- "What's the difference between a multi-agent *library* and a *platform*?"
- "Which multi-agent framework has the most GitHub stars — and does it matter?"
- "Do these require a Claude subscription?"
- "Which is best for a team vs a solo developer?"
- "Is ruflo production-ready?" (answer honestly, with the caveats)

### 8. Close
- Restate: pick the category first, the tool second. Stars are mindshare, not merit.
- Reinvently CTA (match other posts).

---

## Sources to cite (collected during explore)

- GitHub API repo data (stars/forks/dates) — all five repos, fetched 2026-06-06
- ruflo discussion #1666 — community reliability critique
- Augment Code: "Ruflo ships multi-agent orchestration… wrapping the wrapper"
- SitePoint: "Deploying Multi-Agent Swarms with Ruflo"
- Hacker News: Maestro threads (id=46307563, id=46471376)
- Medium (Jeff X. Li): Maestro RoAI interview (80% @ 12h claim)
- mc.builderz.dev + mission-control docs/wiki (pricing, adapters)
- sandcastle README / AgentConn / EveryDev.ai
- Aperant README + issues (#582 "Claude Code not found")

## TODOs

Resolved during explore (2026-06-06):
- [x] Star trajectory — recent-vs-lifetime velocity computed (replaces the misleading
      lifetime-avg proxy). ruflo accelerating ~549/day; Aperant collapsed ~5.5/day.
- [x] Aperant stall — CONFIRMED (no commits since Mar 23 develop / Feb 20 main).
- [x] Latest star counts — confirmed current via GitHub API (ruflo 58,116, etc.).
- [x] Location — lives under `/guides`; slug `multi-agent-orchestration-frameworks-compared`.

Remaining before/at drafting:
- [ ] (Optional production asset) star-history.com SVG embed for the popularity section.
- [ ] Re-confirm star counts at *draft time* (they drift; ruflo climbing fast).
- [ ] Light community-quote verification pass at draft time (links may move).
- [ ] Hand to the blog/guides writer skill to draft prose (exit explore mode first).

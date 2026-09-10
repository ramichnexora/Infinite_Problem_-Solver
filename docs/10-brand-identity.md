# Brand Identity

## Name

**Infinite Problem Solver.** Not a tagline about ambition — a description of the
mechanism. The system in this repo doesn't close tickets and stop; every action feeds
an audit log, every incident updates an SOP, every SOP update changes what the next
cycle does (`docs/03-governance-and-escalation.md`, Incident Handling). The loop never
terminates. That's the "infinite": not infinite scope, infinite iteration.

## Positioning

Most companies bolt AI onto existing jobs — a copilot next to a human, an assistant
that drafts and waits. This system puts AI **on the org chart**: seven seats
(`docs/02-org-chart.md`), each with a mandate, KPIs, an audit trail, and an explicit
approval tier per action (`docs/03-governance-and-escalation.md`) — not a blanket
autonomy level. A human still owns strategy, exceptions, and anything irreversible.

**One-line version:** An AI company operating system where agents own real seats —
mandate, SOPs, KPIs, escalation triggers — not just tools that assist humans.

## Tagline

**"Autonomy is earned, not assumed."** — Principle 5 (`docs/01-principles.md`),
used as the brand line because it's the actual governing rule, not marketing copy
written after the fact. A new seat always starts at draft-and-review; it moves up a
tier only after a defined run of clean output against its KPIs.

## Voice

Direct, systems-first, allergic to hype. Every claim traces to a doc, a metric, or a
number — never "revolutionary" or "seamless." Concrete over abstract: say "Tier 3,
human sign-off" not "human-in-the-loop." When describing autonomy, always name the
boundary in the same sentence (what the agent can do *and* what still requires a
human) — the system's credibility is the boundary, not the automation.

## Visual system

Reference implementation: `docs/10-brand-identity.md` companion artifact (brand board
+ landing page draft), built around a **split-flap operations board** — the visual
world of a departure board or shift-status board, chosen because the product's real
mechanism (seats, phases, tiers, a status line that's always current) already looks
like one. Not a generic "AI startup" gradient-hero look.

**Palette**
| Token | Light | Dark | Use |
|---|---|---|---|
| `bg` / `ink` | `#ECEAE1` / `#1B1F26` | `#12161C` / `#ECEAE1` | page ground / text |
| `accent` (signal amber) | `#A66A16` | `#E2A33B` | brand accent, phase chips, tagline |
| `ok` (status green) | `#3C6E4D` | `#5FBE84` | Tier 1 / operational status |
| `alert` (status red-orange) | `#9A3B25` | `#E2694A` | Tier 3 / escalation |
| board surface (fixed, both themes) | `#12161C` bg / `#EBE6D6` ink / `#E2A33B` accent | — | roster tiles, flap headline, loop diagram — a physical board reads the same regardless of page theme |

**Type**
- Display (section headers, big numerals): **Big Shoulders Display**, 800/900 —
  condensed, industrial, signage-like.
- Body: **IBM Plex Sans** — chosen for its literal "corporate operating system"
  heritage (IBM's own typeface), not a generic default.
- Data / mono (status lines, tier codes, timestamps, the flap headline itself):
  **IBM Plex Mono**.

**Motifs**
- Numbered sections that encode real sequence (rollout order, tier number, principle
  number) — never decorative 01/02/03 on non-sequential content.
- The operating loop (Detect → Act → Log → Escalate-if-uncertain → Learn → repeat) as
  a literal cyclic diagram, not a metaphorical infinity symbol.
- Status-line strip (seats filled, live channels, current phase, last sync) — the
  page always states where the system actually is, matching the honesty standard in
  `README.md`'s Status section.

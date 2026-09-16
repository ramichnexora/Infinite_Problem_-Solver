# The AI Replacement Ladder

Dan Martell's sequencing, adapted for Ramich AI Company / Infinite Problem
Solver: climb it in order. Tokens (AI agents) before hires, and each rung
only gets automated once the rung below it is actually working.

| Rung | Name | Role | Owning lead(s) | What it does |
|---|---|---|---|---|
| 1 | Admin | The Gatekeeper | `coo` | Inbox and calendar to zero. Drafts in the founder's voice — never sends. |
| 2 | Delivery | The Concierge | `cro` / `coo` | Triage support, onboard customers, escalate only the edge cases. |
| 3 | Marketing | The Storyteller | `cmo` | Study what already works online, remix it with the founder's own stories. |
| 4 | Sales | The Deal Maker | `cro` | Sell by chat. Summarize every conversation, forget nothing. |
| 5 | Leadership | The Chief | `chief-ai` | The digital brain (this `knowledge/` folder). The whole team asks it, not the founder. |

## Why this order

Each rung frees up founder time that the next rung's agents then need to be
properly reviewed and trusted before they run with less supervision. Skipping
ahead (e.g. building Sales automation before Admin is actually clean)
produces agents nobody has bandwidth to check — which is how bad output
reaches a real customer.

## Relationship to the existing MILI governance system

This ladder organizes *what* gets built and in what order. The existing
Python MILI framework (`agents/`, `docs/03-governance-and-escalation.md`)
governs *how much autonomy* each piece gets once built — the same Tier
1/2/3 system applies here: Admin and Delivery draft-only by default
(Tier 3-equivalent: founder reviews before anything sends), and nothing on
this ladder auto-publishes, auto-sends, or auto-spends without an explicit,
reviewed founder approval. The `.claude/agents/` subagents in this file are
a second execution surface (Claude Code's native subagent format) sitting
alongside the Python `agents/*.py` seats — they share the same standing
rules in `docs/roles/human-founder.md`, they are not exempt from them.

# Ramich AI Company — Architecture

One founder, a digital brain, and a stack of AI agents built on Dan
Martell's AI Replacement Ladder (see `knowledge/ai-replacement-ladder.md`).
Every rung of the business gets a token (an AI agent) before it gets a hire.

## Two execution layers, one governance model

This repo now runs two parallel agent surfaces that share the same
governance rules (`docs/03-governance-and-escalation.md`,
`docs/roles/human-founder.md`):

1. **Python MILI seats** (`agents/*.py`, registered in `config/agents.yaml`)
   — 9 AI seats + 1 human (founder), each with typed SOPs (`run_sop()`),
   a confidence gate, and an audit log. This is the original, code-level
   agent framework.
2. **Claude Code subagents** (`.claude/agents/*.md`) — 7 department leads +
   36 specialist sub-agents, invoked as native Claude Code subagents and
   driven by the 5 slash commands in `.claude/commands/`. This is the
   department-shaped layer described below.

Neither layer bypasses the founder-approval rule: nothing sends, publishes,
or spends real money without the founder reviewing the exact output first.

## Departments (7 leads → 36 sub-agents = 43 agents total)

| Department | Lead | Ladder rung(s) | Sub-agents |
|---|---|---|---|
| Leadership | `chief-ai` | 5 | 0 (owns `knowledge/` directly) |
| Marketing | `cmo` | 3 | 7 |
| Sales + Success | `cro` | 4 + 2 | 9 (4 sales, 5 success) |
| Admin + Ops | `coo` | 1 + 2 | 4 |
| Product | `cpo` | — (cross-cutting) | 7 |
| Engineering + Automation | `cto` | — (cross-cutting) | 6 |
| Finance | `cfo` | — (cross-cutting) | 3 |

Full agent list, mandates, and RCCF prompt shape: see each file under
`.claude/agents/`.

## Slash commands

| Command | What it does |
|---|---|
| `/daily-marketing` | Build today's time-scheduled post queue across X, LinkedIn, Instagram, YouTube. Draft + queue only, never publishes. |
| `/mark-published <file>` | Move a queued post to `marketing/published/` and log it — run only after a real, founder-done publish. |
| `/calendar-audit` | Sunday Calendar & Energy Audit — DRIP matrix, 2x2 truth grid, next week's Perfect Week. |
| `/weekly-kpi` | One-page weekly KPI scorecard with trends, red flags, and actions. |
| `/deploy-department <dept>` | Run the 4-Part AI Deployment Playbook (Map → SOP-ify → Assign → Verify) against one department. |

## Standing task cadence

| When | Owner | What |
|---|---|---|
| 06:30 daily | `mktg-daily-publisher` | Build the day's social post queue. Founder reviews and publishes each slot. |
| 07:00 daily | `chief-ai` | Founder brief — top 3 priorities, cash snapshot, open exceptions, one thing to automate next. |
| 07:15 daily | `admin-gatekeeper` | Inbox + calendar triage. Draft replies to zero-out, flag calendar conflicts. Draft only. |
| daily | `cto` + `automation-architect` | Ship one automation, or write one Trigger→AI→Automation→Human spec into `automation/`. |
| Fri | `/weekly-kpi` | Weekly KPI scorecard. |
| Sun | `/calendar-audit` | Time + energy audit, design next week's Perfect Week. |

Cloud routines (this session's `create_trigger` Routines — see the 3-hour
dashboard refresh and daily social-post pipeline already running) can drive
the daily rows above once each command/subagent has been verified against
real output at least once, per `/deploy-department`'s Verify step. Not all
of the daily cadence is wired to an actual schedule yet — see "current
status" below.

## Current status (honest, as of this file's creation)

- All 43 `.claude/agents/*.md` files and the 5 `.claude/commands/*.md`
  files exist and are structurally complete.
- **None of these have been run yet against real data.** Per
  `/deploy-department`'s Verify step, each one needs a first real run,
  reviewed by the founder, before it's trusted unsupervised.
- Existing real infrastructure this can build on: the Python `digital_product`
  MILI seat (mirrors `product-strategist`/`product-spec-writer`/
  `digital-product-builder`'s intent), the `marketing` MILI seat's daily
  social pipeline (mirrors `mktg-daily-publisher`), and the 3 Routine
  schedules already running (dashboard refresh, daily social post, weekly
  pipeline health-check).
- `marketing/queue/` and `marketing/published/` don't have content yet —
  they're created empty, ready for the first `/daily-marketing` run.

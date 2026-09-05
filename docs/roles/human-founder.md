# Human Agent — Founder / Final Approver

This is the one human seat in the MILI roster. Unlike the 8 AI seats
(`config/agents.yaml` → `agents:`), this entry does not run SOPs, has no
Python module, and is never invoked by `agents/mili.py`'s delegation logic.
It exists so the registry — and the daily dashboard — can show the full
picture: every decision in the company either resolves inside an AI seat's
Tier 1/2 confidence gate, or it lands here.

## Mandate

Hold final sign-off (Tier 3 — `docs/03-governance-and-escalation.md`) on:

- `finance` seat outputs (always Tier 3)
- `hr_recruiting` seat outputs (always Tier 3)
- Any Tier 2 seat output that fails its confidence gate and escalates up
- Any action that sends real communication to real third parties (live
  email sends, ad spend, public posts) until that channel has a proven
  track record at Tier 2

## What this role does NOT do

- Does not replace a real customer list. A human-in-the-loop approver
  cannot manufacture 100 consenting email recipients — those still have to
  come from real signups (landing page, ads, partnerships).
- Does not get bypassed by "trust the architecture" instructions. Tier 3
  gates exist specifically so no AI seat auto-executes irreversible,
  externally-visible actions.

## Daily update contract

Per the founder's request (2026-09-05), every seat's activity, the current
lead-collection status, and MILI's near-term plan get surfaced once per day
in the live dashboard (see `dashboard/` or the published Artifact link
shared in chat) rather than requiring the founder to ask.

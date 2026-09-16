# Playbook: The AI Replacement Ladder

Promoted from the delivered Shopify AI Operating System artifact (source
framework: Dan Martell's AI Company Operating System Playbook — tokens
first, hire later).

## Objective
Decide, in order, where AI absorbs work before any human hire is considered
— and map each rung to the MILI seat that owns it.

## Trigger
Reviewed whenever considering a new hire, or quarterly as a system check.

## Inputs
Current calendar audit output (`buyback-loop.md`), current agent registry
(`config/agents.yaml`).

## Preconditions
`master-prompt.md` loaded.

## Step-by-step process
Climb in order — do not skip a rung. At every rung, hand off everything AI
can absorb before bringing on a human.

1. **Admin -> The Gatekeeper** (maps to `support`/`operations` seats) —
   inbox/order triage, drafts replies in-voice, protects writing blocks.
2. **Delivery -> The Concierge** (maps to `support` seat) — digital-download
   support, refunds, "where's my file" — resolved without founder involvement.
3. **Marketing -> The Storyteller** (maps to `marketing` seat) — studies
   what's working in the niche, remixes with the founder's own frameworks.
4. **Sales -> The Deal Maker** (maps to `sales` seat) — Sell-by-Chat DM
   support: summarizes, captures objections, flags follow-ups.
5. **Leadership -> The Chief** (maps to `mili` orchestrator +
   `memory/`) — the digital brain: every guide's framework, every answer
   the founder has given, held in `memory/` and read by every seat instead
   of asking the founder directly.

## Tools
`config/agents.yaml` (which seats exist today), `memory/` (the Chief rung).

## Quality standards
A hire is proposed only after the corresponding rung's AI seat has absorbed
everything it can and is still the bottleneck.

## Decision rules
Tokens first, hire later, at every rung, no exceptions without a documented
reason in `memory/decisions/`.

## Failure handling
If a rung is under-performing, first check whether the SOP/playbook or
tooling is the gap (per `docs/01-principles.md` #7) before proposing a hire.

## Definition of Done
Each rung has either an active seat in `config/agents.yaml` or a documented
reason it's still manual in `memory/decisions/`.

## Output format
A one-page rung-by-rung status, refreshed quarterly.

---
**Owner (human):** founder
**Version:** v1 — promoted from Shopify AI OS artifact
**Status:** active

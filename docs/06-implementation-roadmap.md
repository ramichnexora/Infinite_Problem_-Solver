# Implementation Roadmap

Rolling out an AI seat is a phased process, not a switch you flip. Each phase has an
explicit exit criterion — don't advance a seat on a deadline, advance it on evidence.

## Phase 0 — Document the SOP as a human process

Before any agent touches the role, run it as a documented human/manual process for
long enough to surface the real edge cases. Write the SOP from what actually happens,
not from how you assume the work goes. **Exit criterion:** the SOP handles the last
month of real cases without requiring ad hoc exceptions.

## Phase 1 — Draft-and-review (Tier 3 for everything)

The agent runs the SOP and produces output, but every action is Tier 3
(`docs/03-governance-and-escalation.md`) — a human reviews and approves before
anything goes out. This phase is about validating the agent's judgment, not its
throughput. **Exit criterion:** a defined run (e.g. two consecutive weeks) of
approved output with no material corrections needed.

## Phase 2 — Partial autonomy (Tier 1/2 for low-risk actions)

Routine, reversible, low-risk actions move to Tier 1 or 2 per the role file; anything
touching money, legal exposure, or a strategic account stays Tier 3 regardless of how
Phase 1 went. **Exit criterion:** KPIs hit target and system-health metrics
(`docs/05-metrics-dashboard.md`) stay flat or improve for a full review cycle.

## Phase 3 — Full seat ownership

The agent runs its full mandate at the autonomy tiers defined in its role file, with
human involvement limited to KPI review, Tier 3 approvals, and periodic SOP updates.
This is the steady state most seats should reach — it is not "full autonomy with no
human in the loop," since Tier 3 actions remain permanently gated per
`docs/03-governance-and-escalation.md`.

## Rollback

Any phase can be rolled back for a specific seat or specific action type if incidents
or degrading system-health metrics warrant it (`docs/03-governance-and-escalation.md`,
Incident Handling). Rollback is a normal part of operating the system, not a failure
of the framework.

## Suggested rollout order across seats

Start with seats where mistakes are cheap and reversible, so the org builds trust in
the system before touching money or customer relationships:

1. **AI Operations Agent** and **AI Product Research Agent** — no customer-facing or
   money-moving actions; safe to move through phases fastest.
2. **AI Support Agent** and **AI Marketing Agent** — customer/brand-facing but
   individually low-stakes and reversible.
3. **AI Sales Agent** and **AI HR & Recruiting Agent** — involves external
   relationships (prospects, candidates) where tone and judgment matter more.
4. **AI Finance Agent** — highest blast radius; move slowest, and remember that
   payment-initiation actions never leave Tier 3 regardless of phase
   (`docs/roles/ai-finance.md`).

## Adding a new AI seat later

1. Write the four-part contract (mandate, SOPs, KPIs, escalation triggers) as a new
   file in `docs/roles/`, following the existing files as a template.
2. Add it to the org chart and seat inventory (`docs/02-org-chart.md`).
3. Scope its tooling access (`docs/04-tech-stack.md`).
4. Run it through Phases 0–3 above like any other seat.

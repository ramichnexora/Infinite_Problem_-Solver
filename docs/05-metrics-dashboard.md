# Metrics Dashboard

## Company-level view

Leadership should be able to answer these questions weekly without pinging anyone:

| Question | Metric | Source seat |
|---|---|---|
| Is pipeline healthy? | Meetings booked, lead → meeting conversion | AI Sales Agent |
| Is content driving pipeline? | Content-attributed leads/pipeline | AI Marketing Agent |
| Are customers being taken care of? | First-contact resolution rate, CSAT | AI Support Agent |
| Is the business running on schedule? | % recurring workflows on time | AI Operations Agent |
| What's our cash position? | Cash on hand, burn rate, DSO | AI Finance Agent |
| Is hiring on track? | Time-to-fill, onboarding completion rate | AI HR & Recruiting Agent |
| Is the roadmap grounded in real signal? | % roadmap items traceable to a signal theme | AI Product Research Agent |

This table is the top-level dashboard. Each row links to the fuller KPI set defined in
that seat's role file under `docs/roles/`.

## System-health metrics (across all seats)

These aren't about any one function — they're about whether the AI Company OS itself
is working:

- **Escalation rate by seat** — rising escalation rate can mean the seat is hitting
  more edge cases (SOP gap) or a knowledge/data source has gone stale. Investigate,
  don't just monitor.
- **Escalation SLA adherence** — % of Tier 3 items reviewed within SLA
  (`docs/03-governance-and-escalation.md`). Chronic misses mean human leads are the
  bottleneck, which defeats the point of the system.
- **Incident count and recurrence** — incidents per seat per month, and how many are
  repeats of a previously logged failure mode. Repeats mean the incident process
  (`docs/03-governance-and-escalation.md`) isn't closing the loop.
- **Autonomy tier distribution** — how many seats/actions are at Tier 1 vs. requiring
  Tier 3 review, tracked over time as a proxy for how much the system is actually
  reducing human load.

## Review cadence

- **Weekly** — each human lead reviews their seat's KPIs (table above + role file
  detail).
- **Monthly** — CEO reviews the system-health metrics across all seats, not just
  individual KPIs, since a seat can hit its KPI while quietly generating escalation or
  incident debt.

## Anti-pattern to watch for

A seat hitting its primary KPI while escalation rate, incident count, or SLA adherence
quietly degrades is not a healthy seat — it's a seat trading long-term system health
for a short-term number. Weight the system-health metrics as heavily as the primary
KPI when deciding on autonomy-tier promotions.

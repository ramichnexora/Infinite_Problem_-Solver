# Operating Principles

These apply to every AI seat, SOP, and integration in this system. When a role file and
a principle conflict, the principle wins — fix the role file.

## 1. One seat, one owner

Every outcome has exactly one seat accountable for it. If two roles both "help with"
onboarding, onboarding has no owner and will quietly fail. Split the mandate or merge
the seats — never leave it shared.

## 2. Write the SOP before you automate it

An agent should never be the first thing to attempt a process. Run it as a documented
human or semi-manual SOP first, find the edge cases, *then* hand it to an agent. Automating
an undocumented process just automates the confusion.

## 3. Escalate on uncertainty, not just on failure

An agent that only escalates when it errors out will confidently do the wrong thing right
up until it breaks something expensive. Escalation triggers (`docs/03-governance-and-escalation.md`)
must include "I'm not confident," not just "I couldn't."

## 4. Every agent action is logged and attributable

If an agent sent the email, changed the price, or closed the ticket, there must be a
record of which SOP it was running, what inputs it used, and what it decided — findable
by a human without asking the agent to explain itself after the fact.

## 5. Autonomy is earned, not assumed

A new AI seat starts at the lowest autonomy tier (draft-and-review) for its role. It
moves up a tier only after a defined run of clean output against its KPIs — see the
tiers in `docs/06-implementation-roadmap.md`. Autonomy is a privilege the seat earns,
not a default it starts with.

## 6. Humans own judgment calls with irreversible or high-stakes consequences

Money above a threshold, legal commitments, hiring/firing, and anything customer-facing
that can't be un-sent are human sign-off by default, regardless of how well the agent
has performed historically. See the approval tiers in `docs/03-governance-and-escalation.md`.

## 7. Optimize the system, not the seat

If an AI seat is missing its KPI, the first question is whether the SOP, inputs, or
tooling are broken — not whether to quietly lower the bar. Fix the system; don't
redefine success downward.

## 8. Fewer, better-scoped seats beat many overlapping ones

A sprawl of narrow agents ("email drafter," "subject line agent," "follow-up agent")
creates more handoff failures than it saves. Scope a seat to a full outcome (e.g. "AI
Sales Agent" owns the full outbound-to-booked-meeting motion) rather than a single step.

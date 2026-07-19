# Governance & Escalation

## Approval tiers

Every action any AI seat can take falls into one of three tiers. The tier is a
property of the *action*, not the seat's overall autonomy level — a highly autonomous
seat still hits Tier 3 actions constantly, by design.

### Tier 1 — Autonomous

The agent acts without prior review. Examples: sending a routine support reply from
the knowledge base, publishing a calendar-planned blog post, reconciling a matched
transaction. Logged for audit, not reviewed before it happens.

### Tier 2 — Autonomous with notification

The agent acts, then immediately notifies the human owner. Used for actions that are
reversible and low-risk but worth a human's awareness. Examples: booking a sales
meeting, sending an onboarding checklist, running a scheduled dunning reminder.

### Tier 3 — Human sign-off required

The agent drafts/prepares the action and stops. A human must explicitly approve
before it executes. Examples: any outbound payment, a refund above threshold, a
contract or pricing commitment, any communication to a strategic/enterprise account,
hiring decisions, and anything flagged as legal/compliance-sensitive.

## Setting thresholds

Dollar and severity thresholds (refund limits, payment limits, "strategic account"
definitions) are set per company and recorded in each role file's escalation section —
this doc defines the *tier system*, not the specific numbers. Review thresholds
quarterly; if an agent is escalating too much Tier 3 traffic that's consistently
rubber-stamped, consider moving that specific action to Tier 2, not raising the
threshold blindly.

## Escalation handling SLA

- Tier 3 items must be reviewed within the SLA defined for that role (default: 1
  business day). If unreviewed past SLA, the operations agent (`docs/roles/ai-operations.md`)
  escalates further, up to the CEO if needed.
- An agent should never silently drop a Tier 3 item because a human hasn't responded —
  it stays queued and visible until actioned.

## When an agent is uncertain, not just blocked

Uncertainty is itself an escalation trigger (Principle 3, `docs/01-principles.md`).
An agent that isn't confident in a categorization, score, or response should route to
Tier 3 for that instance even if the action type is normally Tier 1 or 2. Confidence
thresholds are defined per-SOP in each role file.

## Incident handling

If an agent takes an action that turns out to be wrong (sent an incorrect refund,
published something off-brand, mis-scored a lead), the human owner:

1. Reverses the action if possible.
2. Logs what happened and why (bad input, SOP gap, tooling bug, or agent error).
3. Updates the SOP, escalation trigger, or tooling so the same failure mode is caught
   next time — every incident should leave the system harder to repeat, not just fixed
   once.
4. Considers whether the seat's autonomy tier should be temporarily rolled back for
   that action type while the fix is validated.

## Reviewing and changing an AI seat's mandate

Changing what an AI seat is responsible for (expanding or narrowing its mandate) is a
Tier 3 decision made by the seat's human lead, documented as an update to the relevant
file in `docs/roles/`.

# Tech Stack

This system is deliberately tool-agnostic — pick specific vendors per company. What
matters is that every AI seat has exactly the access it needs and no more, and that
every system of record is unambiguous.

## Principles for tooling

- **One system of record per data type.** If leads live in two CRMs, no agent can
  reliably act on "the" lead record. Pick one source of truth per data type before
  giving an agent write access to anything.
- **Least privilege by default.** An agent gets read access to what it needs for
  context and write access only to what its mandate requires. The AI Finance Agent
  reading the ATS has no justification; give it exactly what its role file specifies.
- **Every write path is logged.** If a tool doesn't produce an audit trail for agent
  actions, don't grant write access through it until it does.

## Per-role requirements

| Role | System of record | Read access | Write access |
|---|---|---|---|
| AI Sales Agent | CRM | Enrichment data, calendar availability | CRM records, email/social send, calendar bookings |
| AI Marketing Agent | CMS / content calendar | Analytics/attribution, brand style guide | CMS drafts & publishing, social scheduler |
| AI Support Agent | Helpdesk | Knowledge base, account/billing (read-only) | Helpdesk ticket responses/status |
| AI Operations Agent | Project/task tracker | Every AI seat's status digest | Task reminders, digest publishing |
| AI Finance Agent | Accounting platform | Bank/payment processor (read-only) | Invoicing tool, accounting categorization — **no payment-initiation write access** |
| AI HR & Recruiting Agent | ATS | Calendar availability | ATS candidate status, interview scheduling, onboarding checklist |
| AI Product Research Agent | Insight brief doc/wiki | Helpdesk, CRM/call notes, churn survey results | Insight brief only |

## Cross-cutting infrastructure

- **Audit log** — every Tier 1/2/3 action (see `docs/03-governance-and-escalation.md`)
  from every seat is logged with: seat, SOP invoked, inputs, decision, and timestamp.
  This is infrastructure the whole system depends on — build/buy it before turning on
  autonomous seats, not after.
- **Status digest pipeline** — each seat publishes a structured daily digest the
  Operations Agent aggregates. Keep the format consistent across seats so the digest
  is scannable, not seven different report styles.
- **Escalation queue** — a single place Tier 3 items land, regardless of which seat
  raised them, so a human lead isn't checking seven different inboxes.

## Adding a new integration

When a role needs a new tool: confirm it doesn't duplicate an existing system of
record, scope the access to least-privilege per the table above, confirm it can write
to the audit log, then add it to that role's file and this table.

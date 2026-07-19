# AI Support Agent

## Mandate

Resolve customer support tickets to first-contact resolution wherever possible, and
route everything else to the right human with full context attached.

## In scope

- Triaging and categorizing every inbound ticket.
- Answering questions covered by the knowledge base.
- Executing pre-approved account actions (password resets, plan-detail lookups,
  standard refunds under the threshold).
- Escalating and summarizing anything it can't resolve.
- Flagging recurring issues back to product/ops as signal.

## Out of scope

- Refunds or credits above the pre-approved threshold.
- Account cancellations or downgrades for enterprise/strategic accounts.
- Any request that requires a policy exception.

## SOPs

1. **Triage** — categorize every new ticket by type and urgency within 5 minutes of
   arrival.
2. **Resolve** — attempt resolution using the knowledge base and approved actions
   list; cite the KB article used in the response.
3. **Escalate** — if unresolved within the SOP's confidence threshold, summarize the
   issue, prior context, and attempted resolution, then hand off to the right human
   queue.
4. **Close the loop** — confirm resolution with the customer before closing; if no
   response within the defined window, follow up once, then close.
5. **Signal** — tag tickets that reveal a product bug or a knowledge base gap; batch
   these into a weekly signal report for product/ops.

## KPIs

- First-contact resolution rate.
- Median time to first response.
- CSAT on resolved tickets.
- Escalation rate (tracked as a health signal, not purely minimized — a rising rate
  may mean the KB is stale, not that the agent is underperforming).

## Escalation triggers

- Refund/credit request above the pre-approved threshold.
- Customer expresses intent to cancel an enterprise/strategic account.
- Legal, security, or data-privacy language in the ticket (e.g. GDPR request, breach
  report).
- Customer is visibly angry/escalated (repeated contact, explicit threat to churn or
  go public) — route to a human regardless of whether the underlying issue is simple.

## Tools

Helpdesk/ticketing platform, knowledge base, and read access to account/billing data
— see `docs/04-tech-stack.md`.

## Starting autonomy tier

**Assist-only**: agent drafts responses for a human to send for the first cohort of
tickets; moves to autonomous resolution for KB-covered categories once resolution
accuracy is validated, escalation categories stay assist-only indefinitely.

# Playbook: Ops & Finance — keep the numbers honest, weekly

Promoted from the delivered Shopify AI Operating System artifact. Owning
seats: `operations` (`agents/operations_agent.py`) for KPIs/workflow health,
`finance` (`agents/finance_agent.py`) for bookkeeping — split per the
existing org chart's Ops Leader / Finance Leader division
(`docs/02-org-chart.md`).

## Objective
Give the founder an honest, current read on revenue, conversion, and cash —
weekly, without manual pulling.

## Trigger
Weekly (matches `docs/02-org-chart.md` reporting rhythm).

## Inputs
Shopify orders, cart-recovery sequence stats, Stripe/PayPal fees, tool
subscription list.

## Preconditions
`master-prompt.md` loaded.

## Step-by-step process
1. **Weekly KPI pack** (`operations`) — Role: operator-analyst. Context:
   Shopify/Instagram/email sources, targets. Command: one-page scorecard —
   revenue, units by guide, best-converting DM source, list growth, red
   flags. Format: table (KPI, Current, Trend, Target, Note, Action).
2. **Cart-recovery sequence check** (`operations`) — Role: lifecycle-email
   analyst. Context: current 3-email sequence performance. Command:
   diagnose timing/subject/discount gap, propose one test.
3. **Monthly bookkeeping close** (`finance`) — Role: solo-founder
   bookkeeper. Context: payouts, fees, subscriptions. Command: categorize,
   flag duplicates/unused tools, confirm true net profit.

## Tools
`operations`, `finance` agent seats; Shopify Payouts data.

## Quality standards
Every number traceable to a real source (Shopify export, not estimated).

## Decision rules
Any anomaly (duplicate charge, unexplained fee) -> Tier 2 notify. Any
proposed spend change (cancel/add a paid tool) -> Tier 3 sign-off.

## Failure handling
If a data source is unavailable for the week, report the gap explicitly
rather than estimating silently.

## Definition of Done
Weekly scorecard published to `reports/`, month-end close reconciled with no
unexplained anomalies.

## Output format
Tables per prompt above, filed under `reports/`.

---
**Owner (human):** founder (Ops Leader / Finance Leader)
**Version:** v1 — promoted from Shopify AI OS artifact
**Status:** active

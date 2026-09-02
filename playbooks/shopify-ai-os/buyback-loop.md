# Playbook: The AI Buyback Loop

Promoted from the delivered Shopify AI Operating System artifact (source
framework: Dan Martell's AI Company Operating System Playbook — Audit,
Transfer, Fill).

## Objective
Reclaim founder time on a recurring cadence by finding where the week
actually goes, moving low-value work to AI, and reinvesting the freed hours
into writing, selling, and the next guide.

## Trigger
Weekly (Sunday), or whenever the founder feels overloaded/reactive.

## Inputs
Founder's calendar for the last 7-14 days (titles, durations).

## Preconditions
`master-prompt.md` loaded.

## Step-by-step process
1. **Audit** — run the Sunday Calendar & Energy Audit system prompt (below)
   against the last 7-14 days of calendar data.
2. **Transfer** — for every red/low-value block: Camcorder Method (record +
   have AI write the SOP) if it needs a human; otherwise describe the outcome
   and hand it to an agent directly.
3. **Fill** — reinvest freed time into: upgrading AI skills, one new
   automation per week, and writing/selling time.
4. Repeat weekly.

### System prompt — Sunday Calendar & Energy Audit
```
You are my Time & Energy Auditor for Infinite Problem Solver. One belief:
time management is a lie - energy management is the truth. Look at my
actual calendar and tell me the truth about where my week goes, where my
energy leaks, and what I should stop, delegate, or protect. Be direct. No
hedging.

INPUT: I'll paste my calendar for the last 7-14 days. Confirm up front:
(1) this quarter's #1 goal, (2) my Buyback Rate ~= (annual income / 2,000)
/ 4, (3) the work I'm uniquely great at - writing the guides and talking
to customers.

STEP 1 - Categorize every block: Writing/Product, Marketing/Content, Sales
DMs, Customer Support, Store Admin, Deep Work, Recharge, Reactive.
STEP 2 - Energy audit: green/energize, yellow/neutral, red/drain.
STEP 3 - DRIP matrix: Delegate, Replace, Invest, Produce. Target 95%
Produce.
STEP 4 - Insights: 3 biggest leaks with dollar cost.
STEP 5 - Action list: STOP -> AUTOMATE (name the AI fix) -> PROTECT ->
design next week's calendar full of green.
```

## Tools
Any LLM (Claude); founder's calendar export as input.

## Quality standards
Output is a ranked, decision-form action list — not a description of the
week.

## Decision rules
Anything below the Buyback Rate threshold goes on the transfer list by
default.

## Failure handling
If the founder can't produce a calendar export, fall back to a manual
7-day time log for one week before re-running.

## Definition of Done
A named action list (stop/automate/protect) exists and next week's calendar
reflects it.

## Output format
Structured text: summary, bucketed sections, priority action list.

---
**Owner (human):** founder
**Version:** v1 — promoted from Shopify AI OS artifact
**Status:** active

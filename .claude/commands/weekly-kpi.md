---
name: weekly-kpi
description: One-page weekly KPI scorecard with trends, red flags, and actions.
---

Run the `coo` lead agent, delegating to `ops-kpi-analyst` (pull cross-team
numbers from `cfo`'s `analytics-analyst` and `cro`'s pipeline where
available).

1. Pull real numbers only — Shopify customers/orders, real (non-@example.com)
   leads in the lead sheet, published-vs-queued post count, any support
   volume. Never estimate a number that can be checked.
2. One page, four sections: **Trends** (up/down vs last week),
   **Red flags** (anything that should worry the founder), **Wins**, and
   **Actions** (specific, owned by a named sub-agent or the founder).
3. Write to `knowledge/kpi/<date>.md`.
4. If a metric genuinely didn't move, say "no change" — don't pad the report
   to look busier than the week was.

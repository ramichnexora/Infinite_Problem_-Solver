# Business Strategy Audit: Where AI Absorbs Work Before You Hire

A recurring audit for deciding, department by department, what an AI seat should absorb next —
run this before expanding any seat's mandate or adding a new one. It complements
`docs/02-org-chart.md` (who owns what) and `docs/06-implementation-roadmap.md` (how autonomy
is earned over time) with the *method* for finding the next high-leverage seat or SOP.

## The operating loop: Audit → Transfer → Fill

Getting leverage out of AI isn't a one-time rollout, it's a loop leadership runs on a cadence
(quarterly, at minimum — monthly while a function is actively being handed to an agent).

1. **Audit** — find where human time is going to work an agent could do. You can't transfer
   what you haven't measured.
2. **Transfer** — move the work off the human's plate. Two levels, in order:
   - **Document, then hand to a person.** For anything still genuinely people-work, capture the
     steps as an SOP (record yourself doing it once, turn the transcript into a checklist) so a
     teammate — human or AI — can run it without you.
   - **Hand the outcome to an agent.** For anything rules-based, repetitive, or dependent on data
     that already exists, don't write a step-by-step SOP at all — describe the *result* you want
     and let an AI seat own producing it, per `docs/03-governance-and-escalation.md`'s tiering.
     This is the higher-leverage move: every task you can describe by outcome is a task nobody
     has to keep doing by hand.
3. **Fill** — the freed-up human time doesn't stay free by default; reactive work fills a
   vacuum. Redirect it deliberately toward what only a human can do: strategy, judgment calls,
   relationships, and — critically — getting better at running this loop itself (sharper SOPs,
   tighter escalation triggers, faster iteration on the next seat).

Run it again. Each pass should move another slice of low-judgment work off a human's desk and
onto an AI seat, and move that human's time toward higher-leverage work.

## Step 1 — Audit the business and expose the opportunities

Goal: find where AI can reclaim time, cut errors, or multiply output *right now*, not
speculatively.

Before evaluating a single tool, do a full process sweep:

- List every recurring task, per department, currently done by a human.
- Rank each by time cost and dollar cost.
- Flag anything **repetitive, rules-based, or dependent on data that already exists** — these
  are the leverage points. A task that requires new judgment every time is not (yet) one.

Cross-check candidates against the seats already defined in `docs/02-org-chart.md` and
`docs/roles/`:

| Function | Where this system already has an AI seat | What to audit next |
|---|---|---|
| Sales | `docs/roles/ai-sales.md` (qualify) | Call summarization into CRM notes, close prediction |
| Customer success/support | `docs/roles/ai-support.md` | Onboarding sequences, proactive follow-ups |
| Operations | `docs/roles/ai-operations.md` | Schedule/workload generation, demand forecasting |
| Finance | `docs/roles/ai-finance.md` | Anomaly/fraud detection, cash-shortage prediction |
| HR & recruiting | `docs/roles/ai-hr-recruiting.md` | Resume screening at intake, interview scheduling |
| Marketing & content | `docs/roles/ai-marketing.md`, `docs/roles/ai-social-media.md` | Predictive audience targeting, content repurposing |
| Product | `docs/roles/ai-product-research.md` | — |
| Engineering | `docs/roles/ai-developer.md` | PR review triage, release-note drafting |
| Design | `docs/roles/ai-designer.md` | Asset resizing/repurposing across formats |
| Ecommerce | `docs/roles/ai-shopify-manager.md` | Demand-based reorder alerts |

Outcome of this step: **3–5 concrete, high-ROI opportunities**, each mapped to an existing seat
(expand its SOP list) or a clear case for a new seat (write a new `docs/roles/` file).

## Step 2 — Choose the workflow, not just the tool

A tool alone creates no leverage; the workflow around it does. Map every candidate as:

```
Trigger  →  AI seat (label / evaluate / draft / route)  →  System of record updated  →  Human reviews only the exceptions
```

This is exactly the shape `agents/base.py` enforces in code: a deterministic guardrail check,
a model call with a confidence gate, then either autonomous execution or an escalation queue
entry a human clears. Before adding a workflow, confirm:

- It has **one system of record** (`docs/04-tech-stack.md` principle) — don't wire an agent to
  write into two places that can drift.
- The human touchpoint is scoped to **exceptions**, not a rubber stamp on every output — if a
  human is reviewing 100% of outputs indefinitely, the workflow isn't earning autonomy
  (see `docs/06-implementation-roadmap.md`).
- Every write path is logged (`agents/audit.py`) before it goes live.

## Step 3 — Test small, automate, measure

Don't roll a new workflow out company-wide on day one.

1. Pick **one** high-value process and record the *before* numbers: hours spent, cost, output
   quality.
2. Stand up the smallest version of the workflow that proves the loop end to end.
3. Run a weekly feedback loop for the first month: review outputs, fix tone/logic issues,
   tighten guardrails and confidence thresholds.
4. Track, per seat and per SOP:

   | Metric | What it measures |
   |---|---|
   | Time saved | Hours eliminated per task |
   | Cost | Labor cost vs. AI/automation cost |
   | Output consistency | % of outputs approved with no edits |
   | Escalation rate | Share of runs routed to a human vs. auto-executed |
   | ROI | (savings + revenue lift − AI cost) ÷ AI cost |

5. Only promote a seat's autonomy tier (`docs/06-implementation-roadmap.md`) once these numbers
   clear the bar for a defined clean-run period — never on a hunch.

## Step 4 — Standardize and scale the wins

Once a workflow proves ROI for one seat, replicate the pattern rather than reinventing it:

- Turn the working SOP into a `docs/roles/` entry (or an addition to an existing one) so the
  next person implementing it — human or agent-builder — doesn't start from scratch.
- Extend `agents/` the same way every existing seat was built: subclass `agents.base.Agent`,
  encode the role file's escalation triggers as deterministic guardrails first, add the model
  call with a confidence gate, wire it into `run_agents.py`, and add tests using
  `ExplodingLLMClient` (guardrails) and `FakeLLMClient` (confidence gate) — see
  `docs/07-running-the-agents.md`.
- Review the audit log and escalation queue quarterly per seat: a seat escalating too much
  routine traffic needs a sharper guardrail or a raised confidence bar, not a lowered one.
- Reinvest the freed-up human time into running this audit again on the next department.

## Running this audit

- **Cadence:** quarterly at the leadership level (per `docs/02-org-chart.md`'s reporting
  rhythm); monthly for any function currently mid-rollout.
- **Owner:** the human lead of the function being audited, with the CEO reviewing cross-seat
  priority (which opportunity gets built next) as part of the monthly autonomy-tier review.
- **Output:** an updated or new `docs/roles/*.md` file, a ranked backlog of the next 3-5
  opportunities, and — if scope changed — an update to `docs/02-org-chart.md` and
  `docs/04-tech-stack.md`.

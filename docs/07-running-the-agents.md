# Running the Agents

`docs/roles/` describes what each AI seat is accountable for. `agents/` is a working
implementation of all seven of those seats — enough to see the governance model
(`docs/03-governance-and-escalation.md`) actually run, not just be described.

## What's implemented

| Role file | Code | SOPs implemented |
|---|---|---|
| `docs/roles/ai-support.md` | `agents/support_agent.py` | triage, resolve |
| `docs/roles/ai-sales.md` | `agents/sales_agent.py` | qualify (inbound) |
| `docs/roles/ai-product-research.md` | `agents/product_research_agent.py` | cluster + brief |
| `docs/roles/ai-marketing.md` | `agents/marketing_agent.py` | draft |
| `docs/roles/ai-operations.md` | `agents/operations_agent.py` | track + nudge |
| `docs/roles/ai-finance.md` | `agents/finance_agent.py` | reconcile (categorize) |
| `docs/roles/ai-hr-recruiting.md` | `agents/hr_recruiting_agent.py` | screen |
| `docs/roles/ai-developer.md` | `agents/developer_agent.py` | triage |
| `docs/roles/ai-designer.md` | `agents/designer_agent.py` | draft_concept |
| `docs/roles/ai-shopify-manager.md` | `agents/shopify_manager_agent.py` | review_change |
| `docs/roles/ai-social-media.md` | `agents/social_media_agent.py` | draft_post |

Every seat covers at least one full SOP end to end (guardrails → model call →
confidence gate → audit/escalation), not the entirety of every SOP listed in its role
file — e.g. `SupportAgent` doesn't implement the "close the loop" follow-up SOP,
`FinanceAgent` doesn't implement invoicing or dunning. Extend a seat the same way
you'd add a new one (see below).

Two seats are worth calling out specifically because their guardrails encode a
*permanent* policy from the role file, not just a starting point that autonomy earns
its way past:

- **`FinanceAgent`** — any `outbound_payment` transaction hard-escalates unconditionally.
  `docs/roles/ai-finance.md` is explicit that this seat's "earned autonomy" never
  extends to moving money out of the company, at any amount, at any autonomy tier.
- **`HRRecruitingAgent`** — the code only exposes `screen()` (advance/decline against a
  scorecard). There is no method for a hire/no-hire or offer decision, because the role
  file says that's human-only, full stop - not something to gate behind confidence.

## Architecture

Every agent is built on `agents/base.py:Agent`, which enforces the governance model
from `docs/03-governance-and-escalation.md` in code, not just in docs:

1. **Deterministic guardrails first.** Each concrete agent checks its role file's
   escalation triggers with plain code (regex, thresholds) *before* the model is ever
   called — e.g. `SupportAgent` checks the refund amount against a threshold and scans
   for legal/security language. This means a guardrail can't be talked around by a
   clever prompt, because the model never gets a say when a guardrail fires.
2. **Model call with a confidence gate.** If no guardrail fires, the agent calls the
   model and requires a structured JSON response with a `confidence` score. Below
   `confidence_threshold` (default 0.7), or if the model itself sets `"escalate": true`,
   the action is routed to a human instead of executing — this is
   `docs/01-principles.md` principle 3 ("escalate on uncertainty, not just on failure")
   enforced in code.
3. **Every run is logged.** `agents/audit.py` writes one record per SOP invocation —
   executed or escalated — to `logs/audit.jsonl`. Escalated items also land in
   `logs/escalations.jsonl` via `agents/escalation.py`, tagged with the tier
   (`docs/03-governance-and-escalation.md`) and the reason.

Nothing here actually sends an email, issues a refund, or touches a real CRM — nothing
"executes" beyond returning a decision and logging it. Wiring `executed=True` results
to real systems (CRM writes, helpdesk replies, etc.) is the next step once you've
picked the tools in `docs/04-tech-stack.md`.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Run against the sample data

```bash
python run_agents.py support     # triage + resolve data/tickets.sample.json
python run_agents.py sales       # qualify data/leads.sample.json
python run_agents.py research    # cluster data/signal.sample.json
python run_agents.py marketing   # draft data/content_briefs.sample.json
python run_agents.py operations  # assess data/workflows.sample.json
python run_agents.py finance     # categorize data/transactions.sample.json
python run_agents.py hr          # screen data/candidates.sample.json
python run_agents.py developer   # triage data/dev_tickets.sample.json
python run_agents.py designer    # draft_concept data/design_briefs.sample.json
python run_agents.py shopify     # review_change data/shopify_requests.sample.json
python run_agents.py social      # draft_post data/social_slots.sample.json
python run_agents.py all
```

Each run prints whether the action executed or escalated, then appends to
`logs/audit.jsonl` and `logs/escalations.jsonl` (both gitignored — they're runtime
output, not source).

The sample data is deliberately mixed so both the execute path and every escalation
trigger get exercised, e.g.:

- `data/tickets.sample.json` — a refund over threshold, an enterprise cancellation, a
  GDPR request, and a repeated-contact ticket, alongside normal tickets.
- `data/signal.sample.json` — a security mention from two different accounts, which
  should trip the systemic-issue guardrail in `agents/product_research_agent.py`.
- `data/content_briefs.sample.json` — a competitor name mention, an uncleared
  testimonial, and spend over threshold.
- `data/workflows.sample.json` — an access-change request, a workflow overdue past its
  final nudge, and a recurring workflow missed by multiple owners.
- `data/transactions.sample.json` — an outbound payment (always escalates), a disputed
  charge, and an anomalous transfer.
- `data/candidates.sample.json` — a compensation question and a discrimination concern.
- `data/dev_tickets.sample.json` — a change touching auth, a production-data migration, and a
  ticket with no test plan.
- `data/design_briefs.sample.json` — a logo exploration, a client-facing investor deck slide, and
  an uncleared stock photo.
- `data/shopify_requests.sample.json` — a refund request, a price change over threshold, and a
  best-seller going out of stock.
- `data/social_slots.sample.json` — a competitor mention, a giveaway, and a boosted post over
  spend threshold.

## Running the tests

Tests don't require an API key — they inject a fake LLM client
(`tests/conftest.py:FakeLLMClient`) so guardrail logic and the confidence gate can be
verified deterministically:

```bash
pip install -r requirements.txt
pytest
```

## Adding a new agent

1. Read the corresponding file in `docs/roles/` — the escalation triggers section
   becomes your guardrail checks; the SOPs section becomes your `run_sop` calls.
2. Subclass `agents.base.Agent`, set `seat`, implement one method per SOP following
   `agents/support_agent.py` as a template: a `_hard_escalation_reason` check, then a
   `run_sop` call with a system prompt that requires JSON output including
   `confidence` and `escalate`.
3. Add sample data under `data/` and wire it into `run_agents.py`.
4. Write tests using `ExplodingLLMClient` to prove guardrails short-circuit the model,
   and `FakeLLMClient` to test the confidence gate — see `tests/test_support_agent.py`.

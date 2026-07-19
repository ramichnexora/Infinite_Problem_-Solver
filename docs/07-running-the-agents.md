# Running the Agents

`docs/roles/` describes what each AI seat is accountable for. `agents/` is a working
implementation of three of those seats — enough to see the governance model
(`docs/03-governance-and-escalation.md`) actually run, not just be described.

## What's implemented

| Role file | Code | SOPs implemented |
|---|---|---|
| `docs/roles/ai-support.md` | `agents/support_agent.py` | triage, resolve |
| `docs/roles/ai-sales.md` | `agents/sales_agent.py` | qualify (inbound) |
| `docs/roles/ai-product-research.md` | `agents/product_research_agent.py` | cluster + brief |

The other four roles (marketing, operations, finance, HR & recruiting) are documented
but not yet coded — follow the same pattern in `agents/base.py` to add them.

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
python run_agents.py all
```

Each run prints whether the action executed or escalated, then appends to
`logs/audit.jsonl` and `logs/escalations.jsonl` (both gitignored — they're runtime
output, not source).

The sample data is deliberately mixed: `data/tickets.sample.json` includes a refund
over threshold, an enterprise cancellation, and a GDPR request that should all hard-
escalate; `data/signal.sample.json` includes a security mention from two different
accounts that should trip the systemic-issue guardrail in
`agents/product_research_agent.py`.

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

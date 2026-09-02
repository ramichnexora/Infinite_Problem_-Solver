# Playbook: <name>

> Copy this file into the relevant `playbooks/<function>/` folder and fill it in.
> One playbook = one repeatable workflow. Keep it modular — if a playbook needs
> "and/or" in its Objective, it's probably two playbooks.

## Objective
What outcome this playbook exists to produce, in one sentence.

## Trigger
The specific event/condition that starts this playbook (a cron schedule, a new
order, a support ticket tagged X, a human request).

## Inputs
What this playbook needs to run — data, links, credentials (by name, never by
value), prior outputs from another playbook.

## Preconditions
What must be true before this playbook can run (e.g. "Master Prompt loaded,"
"knowledge base entry exists for this topic").

## Step-by-step process
1. ...
2. ...

## Tools
Which agent(s), MCP tool(s), or external service this playbook calls.

## Quality standards
What "good output" looks like — concrete, checkable, not vibes.

## Decision rules
If/then branches the agent should follow without escalating (e.g. "if refund
< $20, approve; if >= $20, escalate to Tier 3").

## Failure handling
What happens if a step fails — retry policy, fallback, when to escalate instead
of silently failing.

## Definition of Done
The checklist `qa/` uses to confirm this playbook's output is actually complete.

## Output format
Exact shape of the final deliverable (table, email draft, JSON, file, etc.).

---
**Owner (human):** <name/role>
**Version:** v1 — <date>
**Status:** draft | active | deprecated

# 10 — Fallback Protocol: an agent never "just stays"

**Rule:** when any agent or sub-agent cannot do its job, the work still gets
done — by the Claude Code session by default, by a human if the session is not
available. Being blocked is reported *alongside* finished work, never instead
of it.

## Why

Through 2026-09-09 the Python seats could not run at all because
`ANTHROPIC_API_KEY` was never set. Every scheduled run failed at startup, and
every product proposal, post draft and support reply was done by hand in the
Claude Code session — silently, outside the audit log. v2 makes that path
explicit, logged and routable.

## How it works

### Layer 1 — Python seats (`agents/`)

`agents.llm.build_llm_client()` returns a real `AnthropicLLMClient` when it
can, otherwise a `HandoffLLMClient`. `Agent.run_sop()` (`agents/base.py`) treats
three cases identically:

- the client is a `HandoffLLMClient` (no API key)
- `llm.complete()` raises (network, auth, rate-limit)
- the response is not valid JSON

In each case it calls `agents.handoff.write_handoff()`, which writes
`tasks/inbox/<utc-stamp>-<seat>-<sop>.md` containing the **full system prompt,
user prompt and inputs**, then escalates the SOP to Tier 3 with reason
`handoff:<file> (<cause>)`. The audit log and escalation queue record it like
any other escalation. Hard guardrails still run first and never write a
hand-off.

Every `run_*.py` entrypoint uses `build_llm_client()`, so a missing key no
longer aborts the run — it produces hand-offs.

### Layer 2 — Claude Code subagents (`.claude/agents/`)

Every subagent file carries the same "v2 — Never idle" section:

1. Check `tasks/inbox/` for `status: pending` hand-offs and complete them
   (fill **Result**, set `status: done`).
2. Label hand-done output `[manual fallback]`.
3. Report the precise blocker (which key/tool/permission) in the same
   message as the finished work.
4. Tier 3 actions still stop for the founder.

### Layer 3 — Scheduled routines

The hourly "MILI Dashboard refresh" routine also sweeps `tasks/inbox/`, so a
hand-off written by a cron-run seat is picked up within the hour even if
nobody is in the session.

## What this does NOT change

- Governance (`docs/03-governance-and-escalation.md`) — Tier 3 approvals,
  hard guardrails, the audit log.
- The founder still owns: sends, publishes, spend, live Shopify products.
- A hand-off is a **fallback**, not the target state. Setting
  `ANTHROPIC_API_KEY` where the schedulers can read it is still the fix.

## Operator checklist

```bash
python3 -c "from agents.handoff import pending_handoffs; print(*pending_handoffs(), sep='\n')"
```

- Pending files → do them (or ask the session to).
- A hand-off older than 24 h with `status: pending` is a process failure —
  raise it, don't delete it.

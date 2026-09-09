# Changelog

## v2.0.0 — 2026-09-09 — "Never idle"

**Every agent and sub-agent upgraded with a hand-off fallback.** An agent that
cannot run no longer crashes or silently stops — the job is written to
`tasks/inbox/` with its full prompt and completed by the Claude Code session
(or a human). See `docs/10-fallback-protocol.md`.

### Runtime (`agents/`)

- New `agents/handoff.py`: `write_handoff()`, `pending_handoffs()`,
  `HandoffLLMClient`.
- `agents/llm.py`: `build_llm_client()` factory — real Anthropic client when
  `ANTHROPIC_API_KEY` is set, hand-off client otherwise.
- `agents/base.py`: `run_sop()` converts an unavailable client, a raised
  model error, or a non-JSON response into a hand-off + Tier 3 escalation.
  Hard guardrails unchanged and still run first.
- Seat ids aligned with `config/agents.yaml` (`support`, `sales`, `finance`,
  `operations`, `hr_recruiting`, `product_research`) so MILI delegation, the
  audit log and hand-off files use one name per seat.
- `run_agents.py`, `run_daily_social_post.py`, `run_telegram_bot.py` use
  `build_llm_client()` — a missing key produces hand-offs instead of an abort.

### Claude Code subagents (`.claude/agents/`, 43 files) and role contracts (`docs/roles/`)

- "v2 — Never idle" section: sweep `tasks/inbox/`, do the work in-session,
  label `[manual fallback]`, report the precise blocker with the work.
- Executive Operating System wired in: Bottleneck Rule (§41) and
  Billion-Dollar Filter (§46) applied before recommending work.

### Tests

- `tests/test_handoff_fallback.py`: missing key, raised error, garbage
  response → hand-off; hard guardrail never writes a hand-off; done files are
  not re-listed.

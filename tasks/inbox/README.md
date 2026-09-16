# tasks/inbox — hand-offs from agents that could not run

Written automatically by `agents/handoff.py` when a seat cannot reach a model
(see `docs/10-fallback-protocol.md`). One file per SOP invocation, with the
full prompt and inputs.

- `status: pending` — nobody has done it yet. The Claude Code session (or the
  hourly routine) picks these up.
- `status: done` — completed; the **Result** section holds the output, which
  is labelled `[manual fallback]` wherever it is used.

Never delete a pending hand-off. Never edit the prompt — only the Result and
the status.

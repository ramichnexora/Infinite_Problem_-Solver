# Tasks

Flat files, one per task — no nested status folders. Status lives in the
YAML frontmatter (see `templates/task.md`) so tasks stay filterable and
reportable (`reports/`) by grep/script without directory gymnastics.

## Lifecycle

```
queued -> assigned -> in_progress -> review (Tier 3 only) -> done
                                            \-> escalated -> (resolved) -> done
                                            \-> failed
```

- `queued` — MILI has logged the task, not yet assigned a seat.
- `assigned` — a seat (agents/registry.py entry) owns it, not yet started.
- `in_progress` — the seat is actively running its SOP/playbook.
- `review` — Tier 3 action awaiting human sign-off
  (docs/03-governance-and-escalation.md).
- `escalated` — routed to logs/escalations.jsonl; stays visible until a
  human actions it (per existing governance doc — never silently dropped).
- `done` — met its Definition of Done, checked in `qa/`.
- `failed` — did not complete; reason logged in the task's Notes section.

## Naming

`task-<zero-padded-id>-<short-slug>.md` — e.g. `task-0001-cart-recovery-copy.md`.
IDs are sequential and never reused.

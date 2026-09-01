# AI Developer Agent

## Mandate

Turn well-scoped engineering tickets into implementation plans and routine code changes
without an engineer picking up every ticket by hand.

## In scope

- Triage incoming tickets: scope the change, list files likely touched, propose a test plan.
- Implement small, well-defined changes (copy tweaks, UI polish, bug fixes with a clear repro).
- Write/extend tests for the change being made.
- Draft PR descriptions summarizing the change and how it was verified.

## Out of scope

- Anything touching authentication, payments, billing, secrets, or encryption.
- Schema or production-data migrations.
- Production hotfixes/deploys without a human approving the change first.
- Architecture decisions or introducing a new dependency/service.

## SOPs

1. **Triage** — read the ticket, propose an implementation plan, files likely touched, a test
   plan, and an effort estimate.
2. **Implement** — write the change and its tests per the approved plan.
3. **Review gate** — every change goes through the review tier defined by its autonomy status
   before merging.
4. **Open PR** — open a PR with a description of the change, linked ticket, and how it was
   verified; request human review.

## KPIs

- Cycle time from ticket triage to PR opened.
- PR review pass rate (merged without major rework requested).
- Test coverage on agent-authored changes.

## Escalation triggers

- Change touches an auth/payments/secrets-sensitive area.
- Change involves a schema or production-data migration.
- No test plan can be inferred for the change.
- Ticket is flagged as a production hotfix.

## Tools

Source control (with PR review), CI/test runner, issue tracker — see `docs/04-tech-stack.md`.

## Starting autonomy tier

**Draft-and-review**: every PR is reviewed by an engineer before merging until a 30-day clean
run on a given ticket category, then well-defined small fixes move to merge-then-notify;
anything touching a sensitive area stays in review permanently.

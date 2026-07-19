# Overview

## The problem with "AI as a tool"

Most companies bolt AI onto existing roles: a rep uses an AI writer, a support agent
uses an AI summarizer. That speeds up a human, but the human is still the bottleneck —
every unit of output still passes through one person's calendar, inbox, and attention.

The AI Company Operating System (AI Company OS) takes a different stance: **some seats
on the org chart are filled by an AI agent, not a human**. The agent owns a mandate, runs
its own SOPs end-to-end, reports against KPIs, and only interrupts a human when it hits a
defined escalation trigger. The human's job shifts from *doing the work* to *designing,
supervising, and improving the system that does the work*.

## What a "seat" means here

Every seat in this system — human or AI — has the same four-part contract:

1. **Mandate** — what outcome this seat is accountable for, in one sentence.
2. **SOPs** — the repeatable procedures the seat runs to produce that outcome.
3. **KPIs** — the numbers that prove the mandate is being met.
4. **Escalation triggers** — the specific conditions under which the seat must stop and
   hand off to a human, rather than deciding on its own.

An AI seat is not "an AI that helps the sales team." It is the seat that owns outbound
prospecting, full stop, with a human sales leader reviewing its KPIs weekly and stepping
in only when an escalation trigger fires.

## Why this structure

- **Auditability** — because each seat's SOPs and escalation rules are written down,
  you can inspect *why* an agent did something, not just *what* it did.
- **Composability** — a new AI role is added the same way a new hire is: define the
  four-part contract, wire up the tools it needs (`docs/04-tech-stack.md`), and put it
  on the org chart (`docs/02-org-chart.md`).
- **Safe autonomy** — agents earn more autonomy over time by demonstrating they hit KPIs
  and respect escalation boundaries (`docs/06-implementation-roadmap.md`), rather than
  being given full authority on day one.

## How to use this repo

- If you're standing up a new AI role, copy the closest file in `docs/roles/` and adapt
  it — don't start from a blank page.
- If you're deciding how much autonomy to grant, read `docs/03-governance-and-escalation.md`
  before `docs/06-implementation-roadmap.md`.
- If you're wiring up tooling, `docs/04-tech-stack.md` lists what each role needs
  access to and why.

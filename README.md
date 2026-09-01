# Infinite Problem Solver — AI Company Operating System

A framework for running a company where AI agents own defined roles on the org chart —
not just tools that assist humans, but agents with their own mandate, SOPs, KPIs, and
escalation rules. Humans set strategy, review exceptions, and grow the system; agents
run the day-to-day.

## Start here

- [`docs/00-overview.md`](docs/00-overview.md) — what this system is and why it's structured this way
- [`docs/01-principles.md`](docs/01-principles.md) — the operating principles every role and SOP follows
- [`docs/02-org-chart.md`](docs/02-org-chart.md) — how work is divided between human and AI seats
- [`docs/roles/`](docs/roles) — one file per AI role: mandate, SOPs, KPIs, escalation triggers
- [`docs/03-governance-and-escalation.md`](docs/03-governance-and-escalation.md) — when an agent must stop and hand off to a human
- [`docs/04-tech-stack.md`](docs/04-tech-stack.md) — the tools/integrations each role needs
- [`docs/05-metrics-dashboard.md`](docs/05-metrics-dashboard.md) — the KPI set leadership watches across all roles
- [`docs/06-implementation-roadmap.md`](docs/06-implementation-roadmap.md) — the phased rollout, augmentation → autonomy
- [`docs/07-running-the-agents.md`](docs/07-running-the-agents.md) — working agent code for all 7 seats: setup, running, testing, extending
- [`docs/08-telegram-bot.md`](docs/08-telegram-bot.md) — a real Telegram channel wired to the AI Support Agent
- [`docs/09-deploying-the-bot.md`](docs/09-deploying-the-bot.md) — running the bot on a free host with no terminal required
- [`docs/10-business-strategy-audit.md`](docs/10-business-strategy-audit.md) — the recurring audit for deciding what an AI seat absorbs next

## Status

Framework docs for all 11 seats, plus a working agent runtime (`agents/`) implementing
one SOP per seat with guardrails, a confidence gate, an audit log, and an escalation
queue — see `docs/07-running-the-agents.md` to run it. The seats: Sales, Marketing,
Support, Operations, Finance, HR & Recruiting, Product Research, Developer, Designer,
Shopify Manager, and Social Media. `integrations/telegram_bot.py` wires the Support
seat to a live Telegram bot. Nothing yet writes to a real CRM/helpdesk/accounting/
Shopify system beyond that.

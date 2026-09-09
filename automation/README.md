# Automation

Trigger/schedule definitions — what runs when, without a human kicking it off
manually. Calls into existing `integrations/` (e.g. `telegram_bot.py`); does
not move or modify anything there.

Each automation is a small config (id, trigger type — cron/webhook/event,
target seat or playbook, tier) — the actual execution still goes through the
existing `agents/base.py` run loop, so every automated action is still
audited and tier-gated exactly like a manually triggered one.

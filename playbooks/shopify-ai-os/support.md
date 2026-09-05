# Playbook: Customer Support — the Concierge

Promoted from the delivered Shopify AI Operating System artifact. Owning
seat: `support` (`agents/support_agent.py`, `docs/roles/ai-support.md`,
already wired to `integrations/telegram_bot.py`).

## Objective
Resolve digital-download support (access, refunds, reviews) to first-contact
resolution, warmly, without founder involvement for the routine cases.

## Trigger
A support ticket/DM/email arrives, or a review-request window opens
(N days post-purchase, no complaint on file).

## Inputs
Order ID, issue type, `data/knowledge_base.md` / `knowledge/`, refund policy
threshold (`docs/roles/ai-support.md`).

## Preconditions
`master-prompt.md` loaded.

## Step-by-step process
1. **Download & access triage** — Role: support lead. Context: order id,
   issue ("can't find download" / "wrong file" / "refund"). Command: draft
   a fast, friendly one-message fix — resend link, explain format, or route
   to refund policy. Sound like a real person helping a friend.
2. **Review request, timed right** — Role: reputation-management assistant.
   Context: guide bought, days since purchase, no complaint on file.
   Command: short, non-pushy review ask referencing the specific guide/
   outcome.
3. **Refund & save conversation** — Role: retention-minded support agent.
   Context: refund reason, policy. Command: acknowledge honestly, offer a
   genuine save if it fits, process cleanly if not.

## Tools
`support` agent seat; Shopify order data; Telegram bot channel
(`integrations/telegram_bot.py`, existing).

## Quality standards
One-message resolution wherever possible; never "Dear Valued Customer."

## Decision rules
Per `data/knowledge_base.md`: refunds under $100 for billing errors ->
autonomous (Tier 1). Anything above, or non-billing-error refunds ->
escalate to Tier 3 (finance/support lead), per existing knowledge base rule
— do not change this threshold here; it's owned by `docs/roles/ai-support.md`.

## Failure handling
If the agent isn't confident about resolving in one message, escalate per
the existing confidence gate in `agents/base.py` — don't guess.

## Definition of Done
Ticket closed with a resolution the customer confirms, or cleanly routed to
Tier 3 with reason logged.

## Output format
Per prompt above — single reply drafts.

---
**Owner (human):** founder (Ops Leader)
**Version:** v1 — promoted from Shopify AI OS artifact
**Status:** active

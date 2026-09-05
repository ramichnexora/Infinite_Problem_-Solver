# Playbook: Sales — sell-by-chat

Promoted from the delivered Shopify AI Operating System artifact. Owning
seat: `sales` (`agents/sales_agent.py`, `docs/roles/ai-sales.md`).

## Objective
Turn Instagram/DM engagement into sales via friendly, low-pressure
conversation — never a hard sell.

## Trigger
A DM lands, a prospect engages with a post, or a thread has gone quiet and
needs a follow-up nudge.

## Inputs
Platform, trigger post/guide, proof links (reviews), the DM thread itself.

## Preconditions
`master-prompt.md` loaded; `memory/preferences/voice.md` (friendly/casual)
applies especially strongly here.

## Step-by-step process
1. **DM openers** — Role: social seller. Context: platform, trigger post,
   proof. Command: 10 human openers, no pressure, reference the exact post.
   Format: bullets (Trigger, Opener, Follow-up nudge, "if no reply" line).
2. **Conversation summary** — Role: sales assistant. Context: paste thread.
   Command: summarize status, best-fit guide, objection, next message.
   Format: Status / Best-fit guide / Objection / Suggested next message.
3. **Objection handling** — Role: objection strategist. Context: common
   objection + proof asset. Command: 3 honest talk tracks (data/story/
   future-pace). Format: track name, when to use, script, proof line.

## Tools
`sales` agent seat; Instagram DMs as the channel.

## Quality standards
Every opener/reply sounds like a real person, references something specific
to that prospect — never a copy-paste template detectable as such.

## Decision rules
Tier 2 (notify) for a completed sale confirmation; Tier 3 (human sign-off)
for any custom discount/bundle offer not already in the standard price list.

## Failure handling
If a conversation stalls after the follow-up nudge, log it and move on —
do not escalate to founder unless the prospect explicitly asks a question
the agent can't answer confidently.

## Definition of Done
Next message is drafted and either sent (Tier 1/2 actions) or queued for
review (Tier 3), with the thread status logged.

## Output format
Per prompt above.

---
**Owner (human):** founder (Sales Leader)
**Version:** v1 — promoted from Shopify AI OS artifact
**Status:** active

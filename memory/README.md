# Memory

Durable business knowledge — distinct from `logs/audit.jsonl`, which is the
*execution* record (what an agent did). Memory is *what's true and decided*,
asserted once and reused, not re-derived every conversation.

- **decisions/** — dated record of significant calls (Tier 3 decisions,
  architecture choices, mandate changes). One file per decision.
- **preferences/** — standing rules that shape how agents produce output
  (voice, tone, formatting, brand facts). See `preferences/voice.md`.
- **facts/** — durable business facts (catalog, pricing, audience) agents
  should read instead of re-deriving.

Rule: if something is asserted as fact more than once across playbooks or
conversations, it belongs here — not repeated inline everywhere.

No secrets/API keys/tokens in this directory — it's git-tracked.

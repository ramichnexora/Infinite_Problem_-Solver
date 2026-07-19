# Telegram Bot

A real channel for the AI Support Agent (`docs/roles/ai-support.md`): people message
your Telegram bot, the message runs through `SupportAgent.resolve()` exactly like any
other ticket, and the bot replies. Same guardrails, same confidence gate, same
escalation queue as every other entry point into that agent — Telegram is just how the
message got in and how the reply got out.

## How it works

```
Telegram message -> integrations/telegram_bot.py:handle_incoming_message()
                     -> builds a ticket dict -> SupportAgent.resolve()
                        -> executed: reply sent straight back to the user
                        -> escalated: user gets a holding reply,
                           TELEGRAM_OPS_CHAT_ID gets the escalation reason
                           + original message, same as agents/escalation.py
```

`handle_incoming_message` (in `integrations/telegram_bot.py`) has no network calls in
it — it's pure routing logic, which is what `tests/test_telegram_bot.py` exercises
directly with a fake LLM client. `TelegramClient` and `run_bot` are the thin,
untested-by-design I/O layer around it (long-polling `getUpdates`, `sendMessage`).

## Setup

1. Message [@BotFather](https://t.me/BotFather) on Telegram, run `/newbot`, and follow
   the prompts. You'll get a bot token that looks like `123456:ABC-...`.
2. (Optional but recommended) Create or pick a chat/group for escalation
   notifications, add your bot to it, and get that chat's ID — the simplest way is to
   send a message in the chat, then call
   `https://api.telegram.org/bot<TOKEN>/getUpdates` and read the `chat.id` field.
3. Export the environment variables — **never commit the token**, `.env` is
   gitignored for exactly this:

```bash
export TELEGRAM_BOT_TOKEN=123456:ABC-your-token-here
export TELEGRAM_OPS_CHAT_ID=-1001234567890   # optional; omit and escalations just won't notify anyone
export ANTHROPIC_API_KEY=sk-ant-...
```

4. Install dependencies and run:

```bash
pip install -r requirements.txt
python run_telegram_bot.py
```

Message your bot on Telegram. A normal support question (anything the sample
`data/knowledge_base.md` covers) gets answered directly. A message that trips a
guardrail — a GDPR request, an angry repeated message, anything the model itself
flags as low-confidence — gets a holding reply, and `TELEGRAM_OPS_CHAT_ID` gets the
full context.

## Extending this pattern

This wires exactly one seat (Support) to exactly one channel (Telegram). The same
shape works for any agent/channel pair: write a `handle_incoming_<channel>_message`
function that builds the input dict an agent's SOP method expects, call the SOP
method, and branch on `result.executed` — see `integrations/telegram_bot.py` as the
template, and `docs/04-tech-stack.md` for what other channels each seat is meant to
eventually connect to.

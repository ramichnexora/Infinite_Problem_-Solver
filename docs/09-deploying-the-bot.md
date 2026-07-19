# Deploying the Telegram Bot (no terminal required)

This runs `run_telegram_bot.py` (`docs/08-telegram-bot.md`) on a host that stays on,
so the bot keeps responding without your own computer needing to stay open. You do
this through the hosting provider's website — the only place you ever type your bot
token or API key is that provider's own "Environment Variables" / "Secrets" box, never
in a chat with anyone, including Claude.

## Before you start

You'll need:

- A GitHub account with this repository pushed to it (already done — branch
  `claude/ai-company-os-playbook-qspedx`).
- Your Telegram bot token from @BotFather.
- An Anthropic API key (from [console.anthropic.com](https://console.anthropic.com)).
- A free account on a hosting provider — steps below use **Railway**, but the same
  three steps (connect repo → set start command → add environment variables) work
  almost identically on **Render** or **Fly.io** if you prefer one of those.

## Steps (Railway)

1. Go to [railway.app](https://railway.app) and sign up/log in with your GitHub account.
2. Click **New Project** → **Deploy from GitHub repo** → pick this repository.
3. When asked which branch to deploy, choose `claude/ai-company-os-playbook-qspedx`
   (or `main`, once this PR is merged).
4. Railway will detect the `Dockerfile` in the repo root automatically and use it to
   build and run the bot — you don't need to configure a build command.
5. Open the new service's **Variables** tab and add:
   - `TELEGRAM_BOT_TOKEN` — your bot token from @BotFather
   - `ANTHROPIC_API_KEY` — your Anthropic API key
   - `TELEGRAM_OPS_CHAT_ID` — optional; the chat that gets notified on escalation
6. Save — Railway redeploys automatically whenever you add/change a variable.
7. Check the **Deployments** → **Logs** tab. You should see `Telegram bot running.
   Ctrl+C to stop.` — that confirms it started and is polling Telegram.
8. Message your bot on Telegram to test it end to end.

No inbound port or health-check URL is needed — this bot only makes outbound calls
(to Telegram and Anthropic), so a "background worker" / "no public networking"
service type is fine if the platform asks.

## Updating the bot later

Push new commits to the branch Railway is deployed from, and it redeploys
automatically. If you change `docs/roles/ai-support.md` or `agents/support_agent.py`,
the next redeploy picks it up — no separate step needed.

## Keeping the token safe

- The token lives only in Railway's (or your chosen host's) Variables tab and your own
  local shell if you also run it locally per `docs/08-telegram-bot.md` — never in this
  repo, never in a commit, never in a chat message.
- If a token was ever pasted somewhere it shouldn't have been (including into a chat),
  revoke it via @BotFather (`/mybots` → your bot → **API Token** → **Revoke current
  token**) and put the new one straight into the host's Variables tab.

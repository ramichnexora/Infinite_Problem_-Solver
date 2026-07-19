#!/usr/bin/env python3
"""Run the AI Support Agent as a Telegram bot - see docs/08-telegram-bot.md.

Requires:
    TELEGRAM_BOT_TOKEN     - from @BotFather
    ANTHROPIC_API_KEY      - see docs/07-running-the-agents.md
    TELEGRAM_OPS_CHAT_ID   - optional; chat/group ID notified when a message escalates

Usage:
    python run_telegram_bot.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from agents.llm import AnthropicLLMClient
from agents.support_agent import SupportAgent
from integrations.telegram_bot import TelegramClient, run_bot

DATA_DIR = Path(__file__).parent / "data"


def main() -> int:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print(
            "TELEGRAM_BOT_TOKEN is not set. Create a bot via @BotFather on Telegram "
            "and export the token - see docs/08-telegram-bot.md.",
            file=sys.stderr,
        )
        return 1

    kb = (DATA_DIR / "knowledge_base.md").read_text(encoding="utf-8")
    agent = SupportAgent(AnthropicLLMClient(), knowledge_base=kb)
    client = TelegramClient(token)
    ops_chat_id = os.environ.get("TELEGRAM_OPS_CHAT_ID")
    if not ops_chat_id:
        print(
            "Warning: TELEGRAM_OPS_CHAT_ID is not set - escalations will not notify a human chat.",
            file=sys.stderr,
        )

    run_bot(agent, client, ops_chat_id=ops_chat_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())

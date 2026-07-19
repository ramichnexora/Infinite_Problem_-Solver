"""Telegram channel for the AI Support Agent.

Wires a Telegram bot as a real inbound/outbound channel: an incoming message
becomes a support ticket run through SupportAgent.resolve() (docs/roles/ai-support.md).
If it executes, the reply goes straight back to the user. If it escalates -
same guardrails and confidence gate as every other channel - the user gets a
holding reply and a human ops chat gets notified with the reason, mirroring
the escalation queue in agents/escalation.py.

Uses the Telegram Bot HTTP API directly via `requests` (long polling) - no
extra bot-framework dependency.
"""
from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import Any, Optional

import requests

from agents.support_agent import SupportAgent

TELEGRAM_API_BASE = "https://api.telegram.org"


class TelegramClient:
    """Thin wrapper around the subset of the Telegram Bot API this integration needs."""

    def __init__(self, token: str, session: Optional[requests.Session] = None):
        self._base = f"{TELEGRAM_API_BASE}/bot{token}"
        self._session = session or requests.Session()

    def get_updates(self, offset: Optional[int] = None, timeout: int = 30) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"timeout": timeout}
        if offset is not None:
            params["offset"] = offset
        response = self._session.get(f"{self._base}/getUpdates", params=params, timeout=timeout + 10)
        response.raise_for_status()
        return response.json().get("result", [])

    def send_message(self, chat_id: int | str, text: str) -> None:
        response = self._session.post(
            f"{self._base}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=15
        )
        response.raise_for_status()


@dataclass
class MessageOutcome:
    reply_text: str
    notify_ops: Optional[str] = None  # set when a human ops chat should also be alerted


def handle_incoming_message(
    agent: SupportAgent, chat_id: int | str, message_id: int, text: str
) -> MessageOutcome:
    """Pure routing logic: one Telegram message in, one outcome out.

    No network I/O here - this is what tests/test_telegram_bot.py exercises
    directly with a fake LLM client, without needing a real bot token.
    """
    ticket = {
        "id": f"telegram-{chat_id}-{message_id}",
        "subject": "Telegram inquiry",
        "body": text,
        "account_tier": "standard",
        "contact_count": 1,
    }
    result = agent.resolve(ticket)

    if result.executed:
        return MessageOutcome(reply_text=result.output.get("response", "Thanks for reaching out."))

    reason = result.escalation_reason or "needs a closer look"
    return MessageOutcome(
        reply_text="Thanks for the message - I've flagged this for a teammate to follow up on shortly.",
        notify_ops=f"Escalated Telegram message from chat {chat_id}:\n{reason}\n\nOriginal message: {text}",
    )


def run_bot(
    agent: SupportAgent,
    client: TelegramClient,
    ops_chat_id: Optional[str] = None,
    poll_timeout: int = 30,
) -> None:
    """Long-polling loop. Runs until interrupted (Ctrl+C)."""
    offset: Optional[int] = None
    print("Telegram bot running. Ctrl+C to stop.", file=sys.stderr)
    while True:
        try:
            updates = client.get_updates(offset=offset, timeout=poll_timeout)
        except requests.RequestException as exc:
            print(f"getUpdates failed ({exc}); retrying in 5s", file=sys.stderr)
            time.sleep(5)
            continue

        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message")
            if not message or "text" not in message:
                continue

            chat_id = message["chat"]["id"]
            outcome = handle_incoming_message(agent, chat_id, message["message_id"], message["text"])
            client.send_message(chat_id, outcome.reply_text)
            if outcome.notify_ops and ops_chat_id:
                client.send_message(ops_chat_id, outcome.notify_ops)

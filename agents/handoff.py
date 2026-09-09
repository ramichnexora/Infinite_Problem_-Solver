"""Hand-off fallback: an agent that cannot run never "just stays".

When the model layer is unavailable (no ANTHROPIC_API_KEY, network failure,
malformed response) the job is written as a hand-off file under
tasks/inbox/ with the *complete* system + user prompt, so the Claude Code
session (or a human) can do the work with the same inputs the agent would
have used. The agent then returns a Tier-3 escalation, so the existing
audit log + escalation queue still record the event.

See docs/10-fallback-protocol.md.
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_INBOX = Path(__file__).resolve().parent.parent / "tasks" / "inbox"
HANDOFF_REASON_PREFIX = "handoff:"

_SLUG = re.compile(r"[^a-z0-9]+")


def _slug(text: str) -> str:
    return _SLUG.sub("-", text.lower()).strip("-") or "task"


@dataclass
class Handoff:
    seat: str
    sop: str
    cause: str
    path: Path

    @property
    def reason(self) -> str:
        return f"{HANDOFF_REASON_PREFIX}{self.path.name} ({self.cause})"


def write_handoff(
    *,
    seat: str,
    sop: str,
    cause: str,
    system_prompt: str,
    user_prompt: str,
    inputs: dict[str, Any] | None = None,
    inbox: str | Path = DEFAULT_INBOX,
) -> Handoff:
    inbox = Path(inbox)
    inbox.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    path = inbox / f"{stamp}-{_slug(seat)}-{_slug(sop)}.md"
    counter = 1
    while path.exists():
        counter += 1
        path = inbox / f"{stamp}-{_slug(seat)}-{_slug(sop)}-{counter}.md"

    body = "\n".join(
        [
            "---",
            f"seat: {seat}",
            f"sop: {sop}",
            "status: pending",
            f"cause: {json.dumps(cause)}",
            f"created_at: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
            "---",
            "",
            f"# Hand-off: {seat} / {sop}",
            "",
            "The Python seat could not run this SOP. Whoever picks this up (the Claude",
            "Code session by default) must do the work with the exact prompt below, write",
            "the result in the **Result** section, set `status: done` in the frontmatter,",
            "and label the output `[manual fallback]` wherever it is used downstream.",
            "",
            "## System prompt",
            "",
            "```",
            system_prompt.strip(),
            "```",
            "",
            "## User prompt",
            "",
            "```",
            user_prompt.strip(),
            "```",
            "",
            "## Inputs (JSON)",
            "",
            "```json",
            json.dumps(inputs or {}, indent=2, default=str),
            "```",
            "",
            "## Result",
            "",
            "_(not yet done)_",
            "",
        ]
    )
    path.write_text(body, encoding="utf-8")
    return Handoff(seat=seat, sop=sop, cause=cause, path=path)


def pending_handoffs(inbox: str | Path = DEFAULT_INBOX) -> list[Path]:
    inbox = Path(inbox)
    if not inbox.exists():
        return []
    result = []
    for path in sorted(inbox.glob("*.md")):
        head = path.read_text(encoding="utf-8")[:400]
        if "status: pending" in head:
            result.append(path)
    return result


class HandoffLLMClient:
    """LLMClient stand-in used when no real model is reachable.

    `complete()` returns a JSON escalation the base agent understands. The
    prompt itself is captured by Agent.run_sop, which writes the hand-off
    file — this client only signals that the model is unavailable.
    """

    unavailable = True

    def __init__(self, cause: str = "ANTHROPIC_API_KEY is not set"):
        self.cause = cause

    def complete(self, *, system: str, user: str) -> str:
        return json.dumps(
            {
                "escalate": True,
                "confidence": 0.0,
                "escalation_reason": f"model unavailable: {self.cause}",
            }
        )

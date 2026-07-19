"""Approval tiers and the escalation queue.

Mirrors docs/03-governance-and-escalation.md:
  Tier 1 - autonomous, no human involved before acting.
  Tier 2 - autonomous, human notified after acting.
  Tier 3 - human sign-off required before acting.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any


class Tier(IntEnum):
    AUTONOMOUS = 1
    NOTIFY = 2
    HUMAN_APPROVAL = 3


@dataclass
class EscalationItem:
    seat: str
    sop: str
    reason: str
    tier: Tier
    payload: dict[str, Any]
    created_at: float = field(default_factory=time.time)

    def to_json(self) -> dict[str, Any]:
        record = asdict(self)
        record["tier"] = int(self.tier)
        return record


class EscalationQueue:
    """Append-only queue of items waiting on a human per docs/03-governance-and-escalation.md.

    Tier 3 items always land here before anything executes. Tier 1/2 items
    only land here if the agent itself was uncertain (see AgentResult.escalate).
    """

    def __init__(self, path: str | Path = "logs/escalations.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def push(self, item: EscalationItem) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(item.to_json()) + "\n")

    def pending(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

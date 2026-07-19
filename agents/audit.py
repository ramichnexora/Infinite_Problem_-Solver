"""Audit logging.

Per docs/01-principles.md #4 ("every agent action is logged and
attributable") and docs/04-tech-stack.md ("Audit log ... build/buy it before
turning on autonomous seats"). Every SOP run gets one line here regardless
of whether it executed autonomously or was routed to the escalation queue.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class AuditRecord:
    seat: str
    sop: str
    inputs: dict[str, Any]
    decision: dict[str, Any]
    tier: int
    executed: bool
    created_at: float = field(default_factory=time.time)


class AuditLog:
    def __init__(self, path: str | Path = "logs/audit.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, record: AuditRecord) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(record)) + "\n")

    def all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

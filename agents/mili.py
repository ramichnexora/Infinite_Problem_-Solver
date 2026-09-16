"""MILI — the central orchestrator.

MILI does not run SOPs itself and does not bypass the existing governance
system (docs/03-governance-and-escalation.md). It is a routing and
bookkeeping layer on top of the existing agent runtime:

  1. Take a business objective.
  2. Break it into tasks (tasks/*.md).
  3. Look up which registered agent owns each task (agents/registry.py).
  4. Call that agent's existing `run_sop()` (agents/base.py — untouched).
  5. Record the delegation decision to the existing AuditLog, tagged
     seat="mili", sop="delegate:<target-seat>".
  6. Roll results up into a project status (projects/<id>/status.md).

Nothing here modifies base.py, the existing seat agents, or the escalation/
audit machinery — it composes them.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .audit import AuditLog, AuditRecord
from .escalation import EscalationQueue
from .registry import AgentRegistry, AgentSpec


@dataclass
class DelegationDecision:
    task_id: str
    target_seat: str
    reason: str
    confidence: float


class MILI:
    """Central orchestrator. Delegates; does not execute specialist work."""

    seat = "mili"

    def __init__(
        self,
        registry: AgentRegistry | None = None,
        audit_log: AuditLog | None = None,
        escalation_queue: EscalationQueue | None = None,
    ):
        self.registry = registry or AgentRegistry()
        self.audit_log = audit_log or AuditLog()
        self.escalation_queue = escalation_queue or EscalationQueue()
        self._agent_cache: dict[str, Any] = {}

    def list_seats(self) -> list[AgentSpec]:
        """Active specialist seats MILI can delegate to."""
        return self.registry.active_agents()

    def choose_seat(self, task_description: str, candidate_seats: list[str]) -> str:
        """Placeholder decision rule: given a short list of plausible seats for
        a task, pick one. Real routing should call the LLM the same way
        agents/base.py does (system+user prompt -> JSON with a `seat` field
        and a `confidence`), then fall through the same escalation path as
        any other agent decision. Left simple here on purpose — this file
        adds orchestration plumbing, not a new prompting pattern to review
        separately.
        """
        if not candidate_seats:
            raise ValueError("No candidate seats provided — cannot delegate.")
        for seat_id in candidate_seats:
            spec = self.registry.all_agents()
            if any(s.id == seat_id and s.is_active for s in spec):
                return seat_id
        raise ValueError(
            f"None of the candidate seats {candidate_seats} are active in the registry."
        )

    def delegate(
        self,
        *,
        task_id: str,
        target_seat: str,
        reason: str,
        confidence: float = 1.0,
    ) -> DelegationDecision:
        """Record a delegation decision. Does not execute the seat's SOP —
        the caller (a CLI, a scheduled job, or a human-triggered run) invokes
        the resolved agent class separately via `self.registry.resolve_class`.
        """
        decision = DelegationDecision(
            task_id=task_id, target_seat=target_seat, reason=reason, confidence=confidence
        )
        self.audit_log.record(
            AuditRecord(
                seat=self.seat,
                sop=f"delegate:{target_seat}",
                inputs={"task_id": task_id, "reason": reason},
                decision={"target_seat": target_seat, "confidence": confidence},
                tier=1,
                executed=True,
            )
        )
        return decision

    def resolve_agent(self, seat_id: str):
        """Instantiate (and cache) the concrete agent class for a seat id."""
        if seat_id not in self._agent_cache:
            agent_cls = self.registry.resolve_class(seat_id)
            self._agent_cache[seat_id] = agent_cls
        return self._agent_cache[seat_id]

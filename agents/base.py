"""Base Agent: the run loop every concrete agent (support, sales, ...) uses.

Two layers of escalation, matching docs/03-governance-and-escalation.md:

1. Deterministic "hard" guardrails - regex/threshold checks a concrete agent
   runs *before* ever calling the model (e.g. "ticket mentions GDPR"). These
   never depend on the model self-reporting risk, per docs/01-principles.md
   principle 3: never trust the model to be the sole safety check.
2. Model-reported uncertainty - if the model itself returns low confidence
   or sets escalate=true, that's still routed to a human even though no
   hard guardrail fired.

Either path skips execution and lands in the EscalationQueue instead;
everything is written to the AuditLog regardless of outcome.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .audit import AuditLog, AuditRecord
from .escalation import EscalationItem, EscalationQueue, Tier
from .llm import LLMClient, parse_json_response


@dataclass
class AgentResult:
    output: dict[str, Any]
    tier: Tier
    executed: bool
    escalation_reason: Optional[str] = None


class Agent:
    seat: str = "base-agent"

    def __init__(
        self,
        llm: LLMClient,
        audit_log: AuditLog | None = None,
        escalation_queue: EscalationQueue | None = None,
        confidence_threshold: float = 0.7,
    ):
        self.llm = llm
        self.audit_log = audit_log or AuditLog()
        self.escalation_queue = escalation_queue or EscalationQueue()
        self.confidence_threshold = confidence_threshold

    def run_sop(
        self,
        *,
        sop: str,
        system_prompt: str,
        user_prompt: str,
        inputs: dict[str, Any],
        default_tier: Tier,
        hard_escalation_reason: str | None = None,
    ) -> AgentResult:
        """Run one SOP invocation end to end: guardrail check, model call,
        confidence gate, audit log, escalation queue."""

        if hard_escalation_reason is not None:
            result = AgentResult(
                output={"escalate": True, "reason": hard_escalation_reason},
                tier=Tier.HUMAN_APPROVAL,
                executed=False,
                escalation_reason=hard_escalation_reason,
            )
            self._finish(sop, inputs, result)
            return result

        raw = self.llm.complete(system=system_prompt, user=user_prompt)
        output = parse_json_response(raw)

        confidence = float(output.get("confidence", 0.0))
        model_wants_escalation = bool(output.get("escalate", False))

        if model_wants_escalation or confidence < self.confidence_threshold:
            reason = output.get("escalation_reason") or (
                f"confidence {confidence:.2f} below threshold {self.confidence_threshold:.2f}"
            )
            result = AgentResult(
                output=output,
                tier=Tier.HUMAN_APPROVAL,
                executed=False,
                escalation_reason=reason,
            )
        else:
            result = AgentResult(output=output, tier=default_tier, executed=True)

        self._finish(sop, inputs, result)
        return result

    def _finish(self, sop: str, inputs: dict[str, Any], result: AgentResult) -> None:
        self.audit_log.record(
            AuditRecord(
                seat=self.seat,
                sop=sop,
                inputs=inputs,
                decision=result.output,
                tier=int(result.tier),
                executed=result.executed,
            )
        )
        if not result.executed:
            self.escalation_queue.push(
                EscalationItem(
                    seat=self.seat,
                    sop=sop,
                    reason=result.escalation_reason or "escalated",
                    tier=result.tier,
                    payload={"inputs": inputs, "output": result.output},
                )
            )

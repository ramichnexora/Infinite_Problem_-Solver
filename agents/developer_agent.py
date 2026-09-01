"""AI Developer Agent - implements the triage/implement step of docs/roles/ai-developer.md.

Deterministic guardrails cover the escalation triggers that don't require
judgment to detect: anything touching auth/payments/secrets, a schema or
production-data migration, and a change with no test plan. Ambiguous
scoping/estimation is left to the model's own confidence score.
"""
from __future__ import annotations

import re
from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

SENSITIVE_AREA_PATTERN = re.compile(
    r"\b(auth|authentication|authorization|payment|billing|secret|api key|credential|encryption)\b",
    re.IGNORECASE,
)
MIGRATION_PATTERN = re.compile(
    r"\b(schema migration|database migration|drop table|alter table|prod(uction)? data)\b",
    re.IGNORECASE,
)

TRIAGE_SYSTEM_PROMPT = """You are the AI Developer Agent's triage/implement step \
(docs/roles/ai-developer.md). Given a ticket, propose an implementation plan.

Respond with JSON only, no prose, no code fences:
{
  "plan": "<step-by-step implementation approach>",
  "files_likely_touched": ["<path>", ...],
  "test_plan": "<how this will be verified>",
  "estimated_effort": "<small|medium|large>",
  "confidence": <0.0-1.0, how confident you are this plan is correct and safe>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class DeveloperAgent(Agent):
    seat = "ai-developer-agent"

    def _hard_escalation_reason(self, ticket: dict[str, Any]) -> str | None:
        text = f"{ticket.get('title', '')} {ticket.get('description', '')}"

        if SENSITIVE_AREA_PATTERN.search(text):
            return "change touches an auth/payments/secrets-sensitive area"

        if MIGRATION_PATTERN.search(text):
            return "change involves a schema or production-data migration"

        if ticket.get("no_test_plan"):
            return "ticket has no test plan and none can be inferred"

        if ticket.get("is_production_hotfix"):
            return "production hotfix requires human sign-off before deploy"

        return None

    def triage(self, ticket: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(ticket)
        user_prompt = (
            f"Title: {ticket.get('title', '')}\n"
            f"Description: {ticket.get('description', '')}\n"
            f"Repo/area: {ticket.get('area', 'unknown')}\n"
            f"Priority: {ticket.get('priority', 'unknown')}\n"
        )
        return self.run_sop(
            sop="triage",
            system_prompt=TRIAGE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"ticket_id": ticket.get("id")},
            default_tier=Tier.NOTIFY,
            hard_escalation_reason=hard_reason,
        )

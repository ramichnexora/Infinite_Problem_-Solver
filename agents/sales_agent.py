"""AI Sales Agent - implements the qualify step of docs/roles/ai-sales.md (SOP 3).

Deterministic guardrails cover the escalation triggers listed in the role
file that don't require judgment to detect: pricing/contract questions,
named strategic accounts, and complaint/legal/press language. Ambiguous
qualification is left to the model's own confidence score.
"""
from __future__ import annotations

import re
from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

PRICING_PATTERN = re.compile(
    r"\b(pricing|price|discount|contract terms|quote|cost)\b", re.IGNORECASE
)
COMPLAINT_PATTERN = re.compile(
    r"\b(complaint|lawsuit|legal action|press|journalist|reporter)\b", re.IGNORECASE
)

QUALIFY_SYSTEM_PROMPT = """You are the AI Sales Agent's inbound qualification step \
(SOP 3 in docs/roles/ai-sales.md). Score the lead against a BANT-style rubric using \
only the information given - do not assume facts not stated.

Respond with JSON only, no prose, no code fences:
{
  "qualified": <true|false>,
  "score": <0-100>,
  "reasoning": "<one or two sentences>",
  "confidence": <0.0-1.0, how confident you are in this score given the available info>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class SalesAgent(Agent):
    seat = "ai-sales-agent"

    def _hard_escalation_reason(self, lead: dict[str, Any]) -> str | None:
        text = f"{lead.get('notes', '')} {lead.get('message', '')}"

        if lead.get("is_strategic_account"):
            return "prospect is a named strategic/enterprise account"

        if PRICING_PATTERN.search(text):
            return "prospect asked a pricing or contract question the agent isn't authorized to answer"

        if COMPLAINT_PATTERN.search(text):
            return "prospect message contains complaint/legal/press language"

        return None

    def qualify(self, lead: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(lead)
        user_prompt = (
            f"Company: {lead.get('company', 'unknown')}\n"
            f"Role/title: {lead.get('title', 'unknown')}\n"
            f"Company size: {lead.get('company_size', 'unknown')}\n"
            f"Notes: {lead.get('notes', '')}\n"
            f"Inbound message: {lead.get('message', '')}\n"
        )
        return self.run_sop(
            sop="qualify",
            system_prompt=QUALIFY_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"lead_id": lead.get("id")},
            default_tier=Tier.NOTIFY,
            hard_escalation_reason=hard_reason,
        )

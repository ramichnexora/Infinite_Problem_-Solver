"""AI Marketing Agent - implements the draft step of docs/roles/ai-marketing.md (SOP 2).

Deterministic guardrails cover the escalation triggers that don't require
judgment to detect: competitor mentions, legal/compliance-sensitive topics,
an uncleared testimonial/logo, spend above the pre-approved threshold, and
inbound partnership/co-marketing requests.
"""
from __future__ import annotations

import re
from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

LEGAL_COMPLIANCE_PATTERN = re.compile(
    r"\b(gdpr|hipaa|ccpa|lawsuit|regulatory|compliance claim|medical claim|financial advice|guarantee(d)? results)\b",
    re.IGNORECASE,
)
PARTNERSHIP_PATTERN = re.compile(
    r"\b(partnership|co-marketing|sponsorship|affiliate deal)\b", re.IGNORECASE
)

DRAFT_SYSTEM_PROMPT = """You are the AI Marketing Agent's draft step (SOP 2 in \
docs/roles/ai-marketing.md). Write on-brand content for the given calendar slot.

Respond with JSON only, no prose, no code fences:
{
  "draft": "<the content>",
  "suggested_channel": "<blog|newsletter|social>",
  "cta": "<call to action>",
  "confidence": <0.0-1.0, how confident you are this fits brand voice and the brief>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class MarketingAgent(Agent):
    seat = "ai-marketing-agent"

    def __init__(
        self,
        llm,
        competitor_names: list[str] | None = None,
        spend_threshold: float = 500.0,
        **kwargs: Any,
    ):
        super().__init__(llm, **kwargs)
        self.competitor_names = competitor_names or []
        self.spend_threshold = spend_threshold

    def _hard_escalation_reason(self, brief: dict[str, Any]) -> str | None:
        text = f"{brief.get('topic', '')} {brief.get('brief_text', '')}"

        for competitor in self.competitor_names:
            if re.search(rf"\b{re.escape(competitor)}\b", text, re.IGNORECASE):
                return f"content references competitor '{competitor}' by name"

        if LEGAL_COMPLIANCE_PATTERN.search(text):
            return "topic touches a legal/compliance-sensitive area"

        if brief.get("uses_testimonial") and not brief.get("testimonial_cleared"):
            return "content uses a customer testimonial/logo not yet cleared for use"

        spend = brief.get("requested_spend")
        if spend is not None and spend > self.spend_threshold:
            return f"requested spend ${spend:.2f} exceeds the pre-approved threshold ${self.spend_threshold:.2f}"

        if brief.get("is_partnership_request") or PARTNERSHIP_PATTERN.search(text):
            return "inbound partnership/co-marketing request"

        return None

    def draft(self, brief: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(brief)
        user_prompt = (
            f"Topic: {brief.get('topic', '')}\n"
            f"Channel: {brief.get('channel', 'blog')}\n"
            f"Brief: {brief.get('brief_text', '')}\n"
        )
        return self.run_sop(
            sop="draft",
            system_prompt=DRAFT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"brief_id": brief.get("id")},
            default_tier=Tier.NOTIFY,
            hard_escalation_reason=hard_reason,
        )

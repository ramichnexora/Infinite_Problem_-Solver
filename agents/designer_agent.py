"""AI Designer Agent - implements the concept step of docs/roles/ai-designer.md.

Deterministic guardrails cover the escalation triggers that don't require
judgment to detect: brand identity/logo changes, unlicensed third-party
assets, and client-facing pitch material. Ambiguous creative direction is
left to the model's own confidence score.
"""
from __future__ import annotations

import re
from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

BRAND_IDENTITY_PATTERN = re.compile(
    r"\b(logo|brand identity|rebrand|brand guidelines?|color palette change)\b",
    re.IGNORECASE,
)
CLIENT_FACING_PATTERN = re.compile(
    r"\b(client pitch|investor deck|press kit|external partner)\b", re.IGNORECASE
)

CONCEPT_SYSTEM_PROMPT = """You are the AI Designer Agent's concept step \
(docs/roles/ai-designer.md). Produce a design concept for the given brief, staying \
within the existing brand/style guide.

Respond with JSON only, no prose, no code fences:
{
  "concept": "<description of the visual approach>",
  "layout_notes": "<key layout/composition decisions>",
  "asset_list": ["<asset needed>", ...],
  "confidence": <0.0-1.0, how confident you are this fits the brief and style guide>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class DesignerAgent(Agent):
    seat = "ai-designer-agent"

    def _hard_escalation_reason(self, brief: dict[str, Any]) -> str | None:
        text = f"{brief.get('title', '')} {brief.get('brief_text', '')}"

        if BRAND_IDENTITY_PATTERN.search(text):
            return "request involves brand identity/logo changes, not routine asset production"

        if brief.get("uses_third_party_asset") and not brief.get("license_cleared"):
            return "design uses a third-party/stock asset not yet cleared for licensing"

        if brief.get("is_client_facing") or CLIENT_FACING_PATTERN.search(text):
            return "asset is client/investor-facing and needs human review before use"

        return None

    def draft_concept(self, brief: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(brief)
        user_prompt = (
            f"Title: {brief.get('title', '')}\n"
            f"Format: {brief.get('format', 'unknown')}\n"
            f"Brief: {brief.get('brief_text', '')}\n"
        )
        return self.run_sop(
            sop="draft_concept",
            system_prompt=CONCEPT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"brief_id": brief.get("id")},
            default_tier=Tier.NOTIFY,
            hard_escalation_reason=hard_reason,
        )

"""AI Social Media Agent - implements the everyday-post step of
docs/roles/ai-social-media.md.

Deterministic guardrails cover the escalation triggers that don't require
judgment to detect: competitor mentions, political/controversial topics,
giveaways/contests (which trigger legal/regulatory rules), and paid boost
spend above the pre-approved threshold. Routine day-to-day post drafting is
left to the model's own confidence score.
"""
from __future__ import annotations

import re
from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

CONTROVERSIAL_PATTERN = re.compile(
    r"\b(politic(s|al)|election|religion|controvers(y|ial))\b", re.IGNORECASE
)
GIVEAWAY_PATTERN = re.compile(r"\b(giveaway|contest|sweepstakes|raffle)\b", re.IGNORECASE)
CRISIS_PATTERN = re.compile(
    r"\b(complaint|backlash|pr crisis|apology|recall)\b", re.IGNORECASE
)

DRAFT_SYSTEM_PROMPT = """You are the AI Social Media Agent's everyday-post step \
(docs/roles/ai-social-media.md). Draft a day-to-day post for the given slot, on-brand \
and native to the target platform.

Respond with JSON only, no prose, no code fences:
{
  "caption": "<the post copy>",
  "hashtags": ["<tag>", ...],
  "suggested_platform": "<instagram|x|linkedin|tiktok|facebook>",
  "suggested_time": "<e.g. 'today 5pm local'>",
  "confidence": <0.0-1.0, how confident you are this fits brand voice and the slot>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class SocialMediaAgent(Agent):
    seat = "ai-social-media-agent"

    def __init__(
        self,
        llm,
        competitor_names: list[str] | None = None,
        boost_spend_threshold: float = 100.0,
        **kwargs: Any,
    ):
        super().__init__(llm, **kwargs)
        self.competitor_names = competitor_names or []
        self.boost_spend_threshold = boost_spend_threshold

    def _hard_escalation_reason(self, slot: dict[str, Any]) -> str | None:
        text = f"{slot.get('topic', '')} {slot.get('notes', '')}"

        for competitor in self.competitor_names:
            if re.search(rf"\b{re.escape(competitor)}\b", text, re.IGNORECASE):
                return f"post references competitor '{competitor}' by name"

        if CONTROVERSIAL_PATTERN.search(text):
            return "topic touches politics/religion/controversy - needs human review"

        if slot.get("is_giveaway") or GIVEAWAY_PATTERN.search(text):
            return "giveaway/contest posts trigger legal/regulatory rules and need sign-off"

        if CRISIS_PATTERN.search(text):
            return "post responds to a complaint/PR situation - needs human-owned response"

        boost = slot.get("requested_boost_spend")
        if boost is not None and boost > self.boost_spend_threshold:
            return (
                f"requested boost spend ${boost:.2f} exceeds the pre-approved "
                f"threshold ${self.boost_spend_threshold:.2f}"
            )

        return None

    def draft_post(self, slot: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(slot)
        user_prompt = (
            f"Topic: {slot.get('topic', '')}\n"
            f"Platform preference: {slot.get('platform', 'any')}\n"
            f"Notes: {slot.get('notes', '')}\n"
        )
        return self.run_sop(
            sop="draft_post",
            system_prompt=DRAFT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"slot_id": slot.get("id")},
            default_tier=Tier.AUTONOMOUS,
            hard_escalation_reason=hard_reason,
        )

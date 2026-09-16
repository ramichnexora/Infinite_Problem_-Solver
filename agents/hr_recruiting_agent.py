"""AI HR & Recruiting Agent - implements the screen step of
docs/roles/ai-hr-recruiting.md (SOP 2).

This agent only ever recommends advance/decline against a scorecard - the
role file is explicit that hire/no-hire and offer decisions are human-only,
so this code doesn't even expose a method for that. Compensation
negotiation and discrimination/harassment/legal concerns hard-escalate
regardless of how well the candidate scores.
"""
from __future__ import annotations

import re
from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

COMPENSATION_PATTERN = re.compile(
    r"\b(salary|compensation|comp package|equity|stock options|negotiate pay)\b", re.IGNORECASE
)
LEGAL_CONCERN_PATTERN = re.compile(
    r"\b(discriminat\w*|harass\w*|lawsuit|attorney|lawyer|EEOC)\b", re.IGNORECASE
)

SCREEN_SYSTEM_PROMPT = """You are the AI HR & Recruiting Agent's screening step (SOP 2 \
in docs/roles/ai-hr-recruiting.md). Score the candidate against the role scorecard using \
only the information given.

Respond with JSON only, no prose, no code fences:
{
  "recommendation": "<advance|decline>",
  "score": <0-100>,
  "reasoning": "<one or two sentences citing the scorecard>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class HRRecruitingAgent(Agent):
    seat = "hr_recruiting"

    def _hard_escalation_reason(self, candidate: dict[str, Any]) -> str | None:
        text = f"{candidate.get('notes', '')} {candidate.get('message', '')}"

        if COMPENSATION_PATTERN.search(text):
            return "candidate communication involves compensation negotiation"

        if LEGAL_CONCERN_PATTERN.search(text):
            return "candidate communication raises a discrimination/harassment/legal concern"

        return None

    def screen(self, candidate: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(candidate)
        user_prompt = (
            f"Role: {candidate.get('role', '')}\n"
            f"Scorecard criteria: {candidate.get('scorecard_criteria', '')}\n"
            f"Resume summary: {candidate.get('resume_summary', '')}\n"
            f"Notes: {candidate.get('notes', '')}\n"
        )
        return self.run_sop(
            sop="screen",
            system_prompt=SCREEN_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"candidate_id": candidate.get("id")},
            default_tier=Tier.NOTIFY,
            hard_escalation_reason=hard_reason,
        )

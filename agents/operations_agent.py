"""AI Operations Agent - implements the track/nudge step of docs/roles/ai-operations.md
(SOPs 1-2).

Deterministic guardrails cover the two escalation triggers the role file
calls out: a workflow overdue past its final nudge, and any request to
change access/permissions. "Process appears broken" (multiple distinct
owners missing the same recurring workflow) is also a hard guardrail,
since it's a pattern-match over structured data, not a judgment call.
"""
from __future__ import annotations

from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

NUDGE_SYSTEM_PROMPT = """You are the AI Operations Agent's nudge step (SOP 2 in \
docs/roles/ai-operations.md). Write a short reminder message to the workflow owner, \
with tone matching the urgency (a first nudge is a friendly reminder; a later nudge \
is more direct).

Respond with JSON only, no prose, no code fences:
{
  "nudge_message": "<the reminder text>",
  "urgency": "<low|medium|high>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class OperationsAgent(Agent):
    seat = "operations"

    def __init__(
        self,
        llm,
        final_nudge_threshold: int = 3,
        broken_process_owner_threshold: int = 2,
        **kwargs: Any,
    ):
        super().__init__(llm, **kwargs)
        self.final_nudge_threshold = final_nudge_threshold
        self.broken_process_owner_threshold = broken_process_owner_threshold

    def _hard_escalation_reason(self, workflow: dict[str, Any]) -> str | None:
        if workflow.get("requests_access_change"):
            return "workflow item requests an access/permissions change"

        nudge_count = workflow.get("nudge_count", 0)
        days_overdue = workflow.get("days_overdue", 0)
        if days_overdue > 0 and nudge_count >= self.final_nudge_threshold:
            return (
                f"workflow is {days_overdue} day(s) overdue after {nudge_count} nudges "
                "with no response - past the final nudge"
            )

        distinct_owners_missed = workflow.get("distinct_owners_missed", 0)
        if distinct_owners_missed >= self.broken_process_owner_threshold:
            return (
                f"{distinct_owners_missed} distinct owners have missed this recurring "
                "workflow - process appears broken, not an individual being late"
            )

        return None

    def assess_workflow(self, workflow: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(workflow)
        user_prompt = (
            f"Workflow: {workflow.get('name', '')}\n"
            f"Owner: {workflow.get('owner', '')}\n"
            f"Days overdue: {workflow.get('days_overdue', 0)}\n"
            f"Prior nudges sent: {workflow.get('nudge_count', 0)}\n"
        )
        return self.run_sop(
            sop="track_and_nudge",
            system_prompt=NUDGE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"workflow_id": workflow.get("id")},
            default_tier=Tier.AUTONOMOUS,
            hard_escalation_reason=hard_reason,
        )

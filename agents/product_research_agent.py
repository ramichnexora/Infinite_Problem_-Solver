"""AI Product Research Agent - implements docs/roles/ai-product-research.md.

The role file calls out one escalation trigger that shouldn't wait for the
next brief cadence: signal suggesting a systemic issue such as a security
concern raised by multiple customers. That's enforced deterministically -
counting distinct sources referencing security/breach language - rather
than relying on the model to notice.
"""
from __future__ import annotations

import re
from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

SECURITY_PATTERN = re.compile(
    r"\b(security|vulnerability|breach|hacked|exploit|data leak)\b", re.IGNORECASE
)

CLUSTER_SYSTEM_PROMPT = """You are the AI Product Research Agent (docs/roles/ai-product-research.md). \
Cluster the customer signal items below into themes, per SOP 2 (cluster) and SOP 3 (brief). \
Rank themes by frequency. Cite the source of each item you group into a theme.

Respond with JSON only, no prose, no code fences:
{
  "themes": [
    {"theme": "<short name>", "frequency": <int>, "impact_summary": "<1 sentence>", "sources": ["<source id>", ...]}
  ],
  "brief": "<2-4 sentence prioritized summary for the product leader>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class ProductResearchAgent(Agent):
    seat = "ai-product-research-agent"

    def __init__(self, llm, systemic_threshold: int = 2, **kwargs: Any):
        super().__init__(llm, **kwargs)
        self.systemic_threshold = systemic_threshold

    def _hard_escalation_reason(self, signal_items: list[dict[str, Any]]) -> str | None:
        security_hits = [item for item in signal_items if SECURITY_PATTERN.search(item.get("text", ""))]
        distinct_sources = {item.get("account") or item.get("source") for item in security_hits}
        distinct_sources.discard(None)

        if len(distinct_sources) >= self.systemic_threshold:
            return (
                f"security-related signal from {len(distinct_sources)} distinct sources - "
                "possible systemic issue, routing immediately per role file"
            )
        return None

    def cluster_signal(self, signal_items: list[dict[str, Any]]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(signal_items)
        lines = [
            f"- [{item.get('source', 'unknown')} / {item.get('account', 'n/a')}] {item.get('text', '')}"
            for item in signal_items
        ]
        user_prompt = "Signal items:\n" + "\n".join(lines)
        return self.run_sop(
            sop="cluster_and_brief",
            system_prompt=CLUSTER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"item_count": len(signal_items)},
            default_tier=Tier.AUTONOMOUS,
            hard_escalation_reason=hard_reason,
        )

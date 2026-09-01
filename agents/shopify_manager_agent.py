"""AI Shopify Manager Agent - implements docs/roles/ai-shopify-manager.md.

Deterministic guardrails cover the escalation triggers that don't require
judgment to detect: price changes above the pre-approved percentage, any
refund/chargeback handling, and a best-seller going out of stock.
Routine listing copy/tag/inventory-count updates are left to the model's
own confidence score.
"""
from __future__ import annotations

from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

REVIEW_SYSTEM_PROMPT = """You are the AI Shopify Manager Agent (docs/roles/ai-shopify-manager.md). \
Review the requested store change and decide how to apply it.

Respond with JSON only, no prose, no code fences:
{
  "action_summary": "<what will be changed>",
  "updated_fields": {"<field>": "<new value>"},
  "confidence": <0.0-1.0, how confident you are this change is correct and safe to apply>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class ShopifyManagerAgent(Agent):
    seat = "ai-shopify-manager-agent"

    def __init__(self, llm, price_change_pct_threshold: float = 15.0, **kwargs: Any):
        super().__init__(llm, **kwargs)
        self.price_change_pct_threshold = price_change_pct_threshold

    def _hard_escalation_reason(self, request: dict[str, Any]) -> str | None:
        change_type = request.get("change_type", "")

        if change_type == "refund" or change_type == "chargeback":
            return f"{change_type} handling requires human sign-off, not agent-executed"

        if change_type == "price_change":
            current = request.get("current_price")
            new = request.get("new_price")
            if current and new:
                pct_change = abs(new - current) / current * 100
                if pct_change > self.price_change_pct_threshold:
                    return (
                        f"price change of {pct_change:.1f}% exceeds the pre-approved "
                        f"threshold of {self.price_change_pct_threshold:.1f}%"
                    )

        if request.get("is_best_seller") and request.get("new_inventory_count", 1) <= 0:
            return "best-selling product would go out of stock - needs human review before publishing"

        if request.get("involves_legal_or_health_claim"):
            return "listing copy makes a legal/health claim that needs compliance review"

        return None

    def review_change(self, request: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(request)
        user_prompt = (
            f"Product: {request.get('product_title', 'unknown')}\n"
            f"Change type: {request.get('change_type', 'unknown')}\n"
            f"Current price: {request.get('current_price', 'n/a')}\n"
            f"Requested new price: {request.get('new_price', 'n/a')}\n"
            f"Requested inventory count: {request.get('new_inventory_count', 'n/a')}\n"
            f"Notes: {request.get('notes', '')}\n"
        )
        return self.run_sop(
            sop="review_change",
            system_prompt=REVIEW_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"request_id": request.get("id")},
            default_tier=Tier.NOTIFY,
            hard_escalation_reason=hard_reason,
        )

"""AI Digital Product Agent - builds digital PDF product specs (title, description,
pricing, positioning) for the Shopify store, then QA-gates the spec before any
human sees it as a launch-ready draft.

This agent never touches Shopify directly - it produces a spec. Creating the
actual Shopify product (draft, never live) and setting price/description stays
a human-triggered action (via the store's own tools), same as every other real
send in this system: Tier 3, always, per docs/roles/human-founder.md's standing
outbound-communication rule extended here to new-product launches.

2 SOPs:
1. draft_product_spec - turn a raw idea (title + one-line angle + audience)
   into a full spec: description, price justification, tags.
2. qa_check - score the spec against a launch-readiness rubric before it's
   shown to the founder. Below the confidence gate, escalate with the reason
   rather than presenting a half-finished spec as ready.
"""
from __future__ import annotations

from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

DRAFT_SPEC_SYSTEM_PROMPT = """You are the AI Digital Product Agent's spec-drafting step \
(SOP 1). Given a raw product idea, produce a complete, launch-ready digital-product spec \
for a Shopify store selling PDF guides/playbooks.

Rules:
1. The description must state concretely what's inside (a bullet list of real content, \
not vague marketing fluff) and who it's for.
2. Never invent a guarantee, refund policy, or statistic that isn't given to you - if the \
brief doesn't specify a refund policy, leave "refund_policy_note" as a reminder to confirm \
with the founder rather than assuming one.
3. Price justification must be honest: name what a $X price actually buys the reader \
(time saved, an alternative cost it replaces), not hype.
4. Tags should be real Shopify-searchable terms, not internal jargon.

Respond with JSON only, no prose, no code fences:
{
  "title": "<product title>",
  "description_html": "<full HTML description, ready to paste into Shopify>",
  "price_usd": <number>,
  "price_justification": "<one or two honest sentences>",
  "product_type": "<e.g. Digital Guide>",
  "tags": ["<tag>", ...],
  "refund_policy_note": "<confirm with founder, or the given policy if one was provided>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

QA_SYSTEM_PROMPT = """You are the AI Digital Product Agent's QA step (SOP 2). Score the \
given product spec against a launch-readiness rubric, 0-100 on each dimension. A spec \
below 80 overall is not launch-ready - list exactly what to fix, don't just say "needs work".

Dimensions:
- content_clarity: does the description say what's actually inside, concretely?
- pricing_honesty: does the price justification avoid hype and invented guarantees?
- audience_fit: is the target audience specific and does the copy speak to them?
- completeness: title, description, price, tags, refund_policy_note all present and non-generic?

Respond with JSON only, no prose, no code fences:
{
  "scores": {"content_clarity": <0-100>, "pricing_honesty": <0-100>, "audience_fit": <0-100>, "completeness": <0-100>},
  "overall": <0-100, average>,
  "launch_ready": <true|false, true only if overall >= 80 AND no dimension below 60>,
  "fixes_needed": ["<specific fix>", ...],
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class DigitalProductAgent(Agent):
    seat = "digital_product"

    def draft_product_spec(
        self, title: str, angle: str, target_audience: str, price_hint: float | None = None
    ) -> AgentResult:
        """SOP 1 - Draft a full product spec from a raw idea.

        Args:
            title: working product title
            angle: one-line description of the product's core promise
            target_audience: who this is for
            price_hint: optional price to anchor around; the model may still
                flag if it doesn't match the described value
        """
        user_prompt = (
            f"Title: {title}\n"
            f"Angle: {angle}\n"
            f"Target audience: {target_audience}\n"
            f"Price hint: {price_hint if price_hint is not None else 'not specified - propose one'}\n"
        )
        return self.run_sop(
            sop="draft_product_spec",
            system_prompt=DRAFT_SPEC_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"title": title, "target_audience": target_audience},
            default_tier=Tier.HUMAN_APPROVAL,
        )

    def qa_check(self, spec: dict[str, Any]) -> AgentResult:
        """SOP 2 - Score a drafted spec for launch readiness before it reaches the founder."""
        user_prompt = (
            f"Title: {spec.get('title', '')}\n"
            f"Description: {spec.get('description_html', '')}\n"
            f"Price: ${spec.get('price_usd', 'unset')}\n"
            f"Price justification: {spec.get('price_justification', '')}\n"
            f"Tags: {spec.get('tags', [])}\n"
            f"Refund policy note: {spec.get('refund_policy_note', '')}\n"
        )
        return self.run_sop(
            sop="qa_check",
            system_prompt=QA_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"title": spec.get("title")},
            default_tier=Tier.HUMAN_APPROVAL,
        )

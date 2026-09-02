"""AI Marketing Agent - implements SOPs 1, 2, and 4 of docs/roles/ai-marketing.md
(Plan, Draft, Publish). SOP 3 (review gate) and SOP 5 (report) are not yet
implemented.

Deterministic guardrails cover the escalation triggers that don't require
judgment to detect: competitor mentions, legal/compliance-sensitive topics,
an uncleared testimonial/logo, spend above the pre-approved threshold, and
inbound partnership/co-marketing requests.

Whether a brief clears the content-value test ("does this actually help the
reader") is a judgment call, not a regex match - it's enforced by asking the
model to self-escalate in DRAFT_SYSTEM_PROMPT and routing low-confidence/
escalate=true responses through the same confidence gate as everything else
(agents/base.py), per docs/01-principles.md principle 3.

`plan_daily_content()` (SOP 1) and `publish()` (SOP 4) back the daily social
posting automation (automation/daily-social-post.yaml,
playbooks/shopify-ai-os/marketing.md prompt #5).
"""
from __future__ import annotations

import re
from typing import Any, Callable, Optional

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

Before drafting, check the content value test: the piece must teach something, save \
the reader time, help them make money, reduce stress, increase productivity, help \
them avoid a mistake, solve a real problem, simplify something complex, or build \
confidence. If you cannot map the brief to at least one of those outcomes, do not \
draft filler - set "escalate": true and explain why in "escalation_reason" (see the \
worked example in docs/examples/ai-education-content-brand.md).

If you do draft, open with a hook that earns attention in the first couple of \
seconds/lines, and make sure the content stands on its own without a hard sell -
educate first, sell second.

Respond with JSON only, no prose, no code fences:
{
  "draft": "<the content>",
  "hook": "<opening line/pattern interrupt>",
  "suggested_channel": "<blog|newsletter|social>",
  "value_tag": "<which content-value-test outcome this serves>",
  "cta": "<call to action>",
  "confidence": <0.0-1.0, how confident you are this fits brand voice and the brief>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


PLAN_SYSTEM_PROMPT = """You are the AI Marketing Agent's plan step (SOP 1 in \
docs/roles/ai-marketing.md), running the Storyteller pattern from \
playbooks/shopify-ai-os/marketing.md prompt #1: success leaves clues - study what's \
already working in the niche, then remix it with Infinite Problem Solver's own \
guides, frameworks, and voice. This is for a Shopify store selling $15-$27 \
AI-automation guides to solopreneurs, freelancers, creators, and VAs.

Produce exactly ONE fresh content angle for today. Do not repeat an angle already \
listed under "Recent topics" in the user prompt - if every safe angle feels reused, \
set "escalate": true rather than forcing a stale one.

Respond with JSON only, no prose, no code fences, matching the brief shape the \
Draft step (SOP 2) expects:
{
  "topic": "<the angle/hook for today>",
  "channel": "<instagram|facebook|tiktok>",
  "brief_text": "<what the post should cover, 2-3 sentences>",
  "audience": "<who this speaks to>",
  "pain_point": "<the specific pain this angle addresses>",
  "desired_outcome": "<what the reader should feel/do after>",
  "primary_keyword": "<the guide or theme this ties back to, if any>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class MarketingAgent(Agent):
    seat = "marketing"

    def __init__(
        self,
        llm,
        competitor_names: list[str] | None = None,
        spend_threshold: float = 500.0,
        channel_publishers: Optional[dict[str, Callable[[dict[str, Any]], dict[str, Any]]]] = None,
        tier_override: Optional[dict[str, Tier]] = None,
        **kwargs: Any,
    ):
        super().__init__(llm, **kwargs)
        self.competitor_names = competitor_names or []
        self.spend_threshold = spend_threshold
        # channel -> callable(post) -> {"post_id": ...}. A channel with no
        # entry here has no live integration yet (e.g. tiktok pre-app-review)
        # and always stays Tier 3 regardless of tier_override.
        self.channel_publishers = channel_publishers or {}
        # channel -> Tier. Missing entries default to HUMAN_APPROVAL
        # (draft-and-review), per docs/06-implementation-roadmap.md Phase 1 -
        # promote a channel to NOTIFY only after its clean-run exit criterion.
        self.tier_override = tier_override or {}

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
            f"Audience: {brief.get('audience', 'not specified')}\n"
            f"Audience pain point: {brief.get('pain_point', 'not specified')}\n"
            f"Desired outcome: {brief.get('desired_outcome', 'not specified')}\n"
            f"Primary SEO keyword: {brief.get('primary_keyword', 'not specified')}\n"
        )
        return self.run_sop(
            sop="draft",
            system_prompt=DRAFT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"brief_id": brief.get("id")},
            default_tier=Tier.NOTIFY,
            hard_escalation_reason=hard_reason,
        )

    def plan_daily_content(self, date: str, recent_topics: list[str] | None = None) -> AgentResult:
        """SOP 1 - Plan. Produces one content brief for `date`, shaped so its
        output feeds directly into draft() without reshaping."""
        recent = recent_topics or []
        user_prompt = (
            f"Date: {date}\n"
            f"Recent topics (do not repeat these angles): {', '.join(recent) if recent else 'none'}\n"
        )
        return self.run_sop(
            sop="plan",
            system_prompt=PLAN_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"date": date, "recent_topics": recent},
            default_tier=Tier.NOTIFY,
            hard_escalation_reason=None,
        )

    def publish(self, post: dict[str, Any], channel: str) -> AgentResult:
        """SOP 4 - Publish. Deterministic dispatch, not a model call: a channel
        with no registered integration (self.channel_publishers) always stays
        Tier 3; a channel with an integration still stays Tier 3 unless
        explicitly promoted via tier_override (draft-and-review by default,
        per docs/06-implementation-roadmap.md)."""
        integration = self.channel_publishers.get(channel)

        if integration is None:
            result = AgentResult(
                output={"channel": channel},
                tier=Tier.HUMAN_APPROVAL,
                executed=False,
                escalation_reason=f"no live publishing integration registered for channel '{channel}'",
            )
        else:
            tier = self.tier_override.get(channel, Tier.HUMAN_APPROVAL)
            if tier == Tier.HUMAN_APPROVAL:
                result = AgentResult(
                    output={"channel": channel, "post": post},
                    tier=Tier.HUMAN_APPROVAL,
                    executed=False,
                    escalation_reason=(
                        f"channel '{channel}' is in draft-and-review (Tier 3) - "
                        "promote via tier_override once its clean-run exit criterion is met"
                    ),
                )
            else:
                try:
                    response = integration(post)
                except Exception as exc:  # noqa: BLE001 - surface any provider failure as an escalation, never a crash
                    result = AgentResult(
                        output={"channel": channel, "error": str(exc)},
                        tier=Tier.HUMAN_APPROVAL,
                        executed=False,
                        escalation_reason=f"publish to '{channel}' failed: {exc}",
                    )
                else:
                    result = AgentResult(
                        output={"channel": channel, "post_id": response.get("post_id")},
                        tier=tier,
                        executed=True,
                    )

        self._finish("publish", {"channel": channel, "post_id_input": post.get("id")}, result)
        return result

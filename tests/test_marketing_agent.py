from __future__ import annotations

from agents.escalation import Tier
from agents.marketing_agent import MarketingAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return MarketingAgent(
        llm, competitor_names=["CompetitorX"], audit_log=audit_log, escalation_queue=escalation_queue, **kwargs
    )


def test_seat_id_matches_registry():
    """config/agents.yaml registers this seat as 'marketing' - keep them aligned
    so MILI's registry-based delegation and the audit log agree."""
    assert MarketingAgent.seat == "marketing"


def test_normal_brief_executes(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "draft": "5 ways to cut onboarding time in half...",
            "suggested_channel": "blog",
            "cta": "Read the full guide",
            "confidence": 0.9,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)
    brief = {"id": "C-1", "topic": "onboarding tips", "channel": "blog", "brief_text": "practical tips"}

    result = agent.draft(brief)

    assert result.executed is True
    assert result.tier == Tier.NOTIFY


def test_competitor_mention_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    brief = {"id": "C-2", "topic": "Why teams switch from CompetitorX", "brief_text": "comparison post"}

    result = agent.draft(brief)

    assert result.executed is False
    assert "CompetitorX" in result.escalation_reason


def test_uncleared_testimonial_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    brief = {
        "id": "C-3",
        "topic": "Customer spotlight",
        "brief_text": "feature their logo and quote",
        "uses_testimonial": True,
        "testimonial_cleared": False,
    }

    result = agent.draft(brief)

    assert result.executed is False
    assert "testimonial" in result.escalation_reason


def test_spend_above_threshold_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue, spend_threshold=500.0)
    brief = {"id": "C-4", "topic": "Boosted launch post", "brief_text": "paid social", "requested_spend": 1500}

    result = agent.draft(brief)

    assert result.executed is False
    assert "spend" in result.escalation_reason


def test_legal_topic_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    brief = {"id": "C-5", "topic": "Our GDPR compliance claim", "brief_text": "regulatory messaging"}

    result = agent.draft(brief)

    assert result.executed is False
    assert "legal" in result.escalation_reason


def test_model_escalates_when_no_content_value(audit_log, escalation_queue):
    """The content-value test (teach/save time/make money/... ) is a judgment call,
    so it's enforced by the model self-escalating, not a hard guardrail - see
    docs/examples/ai-education-content-brand.md."""
    llm = FakeLLMClient(
        {
            "draft": None,
            "hook": None,
            "suggested_channel": "social",
            "value_tag": None,
            "cta": None,
            "confidence": 0.2,
            "escalate": True,
            "escalation_reason": "brief has no clear educational/business value, would just be filler",
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)
    brief = {"id": "C-6", "topic": "post something today", "brief_text": "anything trending, just get views"}

    result = agent.draft(brief)

    assert result.executed is False
    assert "filler" in result.escalation_reason


def test_draft_prompt_carries_content_value_test_and_audience_framework(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "draft": "...",
            "hook": "...",
            "suggested_channel": "social",
            "value_tag": "save time",
            "cta": "...",
            "confidence": 0.9,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)
    brief = {
        "id": "C-7",
        "topic": "onboarding tips",
        "brief_text": "practical tips",
        "audience": "solo founders new to AI tools",
        "pain_point": "wasting hours on manual setup",
        "desired_outcome": "a working onboarding flow in under 30 minutes",
        "primary_keyword": "ai onboarding checklist",
    }

    agent.draft(brief)

    assert "content value test" in llm.calls[0]["system"]
    assert "solo founders new to AI tools" in llm.calls[0]["user"]
    assert "ai onboarding checklist" in llm.calls[0]["user"]


# --- plan_daily_content() (SOP 1) ---


def test_plan_daily_content_executes_and_carries_recent_topics(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "topic": "the 3am refund reply nobody wrote",
            "channel": "instagram",
            "brief_text": "how the support guide handles refunds while you sleep",
            "audience": "solopreneurs",
            "pain_point": "answering the same DM at midnight",
            "desired_outcome": "feel like they can finally log off",
            "primary_keyword": "ai support playbook",
            "confidence": 0.85,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)

    result = agent.plan_daily_content("2026-09-03", recent_topics=["cart recovery story", "cold email hook"])

    assert result.executed is True
    assert result.tier == Tier.NOTIFY
    assert "cart recovery story" in llm.calls[0]["user"]
    assert result.output["channel"] == "instagram"


def test_plan_daily_content_escalates_when_model_cannot_find_a_fresh_angle(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "topic": None,
            "channel": None,
            "brief_text": None,
            "audience": None,
            "pain_point": None,
            "desired_outcome": None,
            "primary_keyword": None,
            "confidence": 0.3,
            "escalate": True,
            "escalation_reason": "every safe angle for this niche was used in the last 14 days",
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)

    result = agent.plan_daily_content("2026-09-03", recent_topics=["a"] * 14)

    assert result.executed is False
    assert "14 days" in result.escalation_reason


# --- publish() (SOP 4) ---


def test_publish_escalates_when_no_integration_registered_for_channel(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)

    result = agent.publish({"id": "P-1", "draft": "..."}, channel="tiktok")

    assert result.executed is False
    assert result.tier == Tier.HUMAN_APPROVAL
    assert "no live publishing integration" in result.escalation_reason


def test_publish_stays_tier_3_even_with_integration_until_promoted(audit_log, escalation_queue):
    """A registered integration alone doesn't auto-publish - tier_override must
    explicitly promote the channel, per docs/06-implementation-roadmap.md."""
    calls = []
    agent = make_agent(
        ExplodingLLMClient(),
        audit_log,
        escalation_queue,
        channel_publishers={"instagram": lambda post: calls.append(post) or {"post_id": "ig-1"}},
    )

    result = agent.publish({"id": "P-2", "draft": "..."}, channel="instagram")

    assert result.executed is False
    assert result.tier == Tier.HUMAN_APPROVAL
    assert calls == []  # integration must never be called while still Tier 3


def test_publish_executes_once_channel_is_promoted(audit_log, escalation_queue):
    agent = make_agent(
        ExplodingLLMClient(),
        audit_log,
        escalation_queue,
        channel_publishers={"instagram": lambda post: {"post_id": "ig-42"}},
        tier_override={"instagram": Tier.NOTIFY},
    )

    result = agent.publish({"id": "P-3", "draft": "..."}, channel="instagram")

    assert result.executed is True
    assert result.tier == Tier.NOTIFY
    assert result.output["post_id"] == "ig-42"


def test_publish_escalates_instead_of_crashing_when_integration_raises(audit_log, escalation_queue):
    def failing_publish(post):
        raise RuntimeError("Graph API rate limited")

    agent = make_agent(
        ExplodingLLMClient(),
        audit_log,
        escalation_queue,
        channel_publishers={"facebook": failing_publish},
        tier_override={"facebook": Tier.NOTIFY},
    )

    result = agent.publish({"id": "P-4", "draft": "..."}, channel="facebook")

    assert result.executed is False
    assert result.tier == Tier.HUMAN_APPROVAL
    assert "rate limited" in result.escalation_reason

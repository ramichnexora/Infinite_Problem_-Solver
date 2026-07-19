from __future__ import annotations

from agents.escalation import Tier
from agents.marketing_agent import MarketingAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return MarketingAgent(
        llm, competitor_names=["CompetitorX"], audit_log=audit_log, escalation_queue=escalation_queue, **kwargs
    )


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

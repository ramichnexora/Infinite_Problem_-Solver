from __future__ import annotations

from agents.escalation import Tier
from agents.social_media_agent import SocialMediaAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return SocialMediaAgent(
        llm, competitor_names=["CompetitorX"], audit_log=audit_log, escalation_queue=escalation_queue, **kwargs
    )


def test_routine_post_executes(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "caption": "Behind the scenes in the studio today.",
            "hashtags": ["#bts", "#studio"],
            "suggested_platform": "instagram",
            "suggested_time": "today 5pm local",
            "confidence": 0.9,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)
    slot = {"id": "SOC-1", "topic": "behind the scenes photo", "platform": "instagram", "notes": "casual"}

    result = agent.draft_post(slot)

    assert result.executed is True
    assert result.tier == Tier.AUTONOMOUS


def test_competitor_mention_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    slot = {"id": "SOC-2", "topic": "Why customers are leaving CompetitorX for us"}

    result = agent.draft_post(slot)

    assert result.executed is False
    assert "CompetitorX" in result.escalation_reason


def test_controversial_topic_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    slot = {"id": "SOC-3", "topic": "Our take on the election"}

    result = agent.draft_post(slot)

    assert result.executed is False
    assert "controversy" in result.escalation_reason


def test_giveaway_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    slot = {"id": "SOC-4", "topic": "Win a year of free product", "is_giveaway": True}

    result = agent.draft_post(slot)

    assert result.executed is False
    assert "giveaway" in result.escalation_reason


def test_crisis_response_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    slot = {"id": "SOC-5", "topic": "Responding to the recall complaint"}

    result = agent.draft_post(slot)

    assert result.executed is False
    assert "complaint" in result.escalation_reason


def test_boost_spend_above_threshold_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue, boost_spend_threshold=100.0)
    slot = {"id": "SOC-6", "topic": "Flash sale reminder", "requested_boost_spend": 250}

    result = agent.draft_post(slot)

    assert result.executed is False
    assert "boost spend" in result.escalation_reason

from __future__ import annotations

from agents.digital_product_agent import DigitalProductAgent
from agents.escalation import Tier
from tests.conftest import FakeLLMClient


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return DigitalProductAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue, **kwargs)


def test_seat_id_matches_registry():
    """config/agents.yaml registers this seat as 'digital_product'."""
    assert DigitalProductAgent.seat == "digital_product"


def test_draft_product_spec_stays_tier3_even_when_confident(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "title": "The AI-Powered Side Hustle Playbook",
            "description_html": "<p>...</p>",
            "price_usd": 29,
            "price_justification": "Replaces hours of trial-and-error prompting.",
            "product_type": "Digital Guide",
            "tags": ["ai-tools", "side-hustle"],
            "refund_policy_note": "confirm with founder",
            "confidence": 0.95,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)

    result = agent.draft_product_spec(
        title="The AI-Powered Side Hustle Playbook",
        angle="Automate 80% of freelance gig work with AI",
        target_audience="freelancers and office workers",
    )

    # Product launches are never auto-executed, even at high model confidence -
    # this is the same standing rule as docs/roles/human-founder.md's outbound
    # send policy, extended to new product launches.
    assert result.executed is True
    assert result.tier == Tier.HUMAN_APPROVAL


def test_qa_check_flags_low_scoring_spec(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "scores": {"content_clarity": 40, "pricing_honesty": 90, "audience_fit": 70, "completeness": 60},
            "overall": 65,
            "launch_ready": False,
            "fixes_needed": ["Description doesn't say what's actually inside"],
            "confidence": 0.85,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)

    result = agent.qa_check(
        {
            "title": "Some Product",
            "description_html": "<p>Vague marketing copy</p>",
            "price_usd": 200,
            "price_justification": "It's great",
            "tags": ["x"],
            "refund_policy_note": "confirm with founder",
        }
    )

    assert result.executed is True
    assert result.output["launch_ready"] is False
    assert result.output["fixes_needed"]

from __future__ import annotations

from agents.designer_agent import DesignerAgent
from agents.escalation import Tier
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return DesignerAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue, **kwargs)


def test_routine_brief_executes(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "concept": "A 4-slide carousel using brand colors and existing iconography.",
            "layout_notes": "Lead with the benefit, close with a CTA slide.",
            "asset_list": ["icon set", "brand palette"],
            "confidence": 0.85,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)
    brief = {"id": "DS-1", "title": "Feature launch carousel", "format": "social carousel", "brief_text": "announce feature"}

    result = agent.draft_concept(brief)

    assert result.executed is True
    assert result.tier == Tier.NOTIFY


def test_logo_change_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    brief = {"id": "DS-2", "title": "New logo exploration", "brief_text": "explore new logo directions"}

    result = agent.draft_concept(brief)

    assert result.executed is False
    assert "brand identity" in result.escalation_reason


def test_uncleared_third_party_asset_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    brief = {
        "id": "DS-3",
        "title": "Blog header",
        "brief_text": "use a stock photo",
        "uses_third_party_asset": True,
        "license_cleared": False,
    }

    result = agent.draft_concept(brief)

    assert result.executed is False
    assert "licensing" in result.escalation_reason


def test_client_facing_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    brief = {"id": "DS-4", "title": "Investor deck cover", "brief_text": "cover slide", "is_client_facing": True}

    result = agent.draft_concept(brief)

    assert result.executed is False
    assert "client" in result.escalation_reason

from __future__ import annotations

from agents.escalation import Tier
from agents.sales_agent import SalesAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def test_normal_lead_executes_and_gets_scored(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "qualified": True,
            "score": 78,
            "reasoning": "Clear ICP match, engaged with content, explicit ask for a call.",
            "confidence": 0.88,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = SalesAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue)
    lead = {
        "id": "L-1",
        "company": "Northwind Logistics",
        "title": "VP Operations",
        "company_size": "80-150 employees",
        "notes": "Downloaded ROI calculator.",
        "message": "Can we set up a call?",
        "is_strategic_account": False,
    }

    result = agent.qualify(lead)

    assert result.executed is True
    assert result.tier == Tier.NOTIFY
    assert result.output["qualified"] is True


def test_strategic_account_hard_escalates(audit_log, escalation_queue):
    agent = SalesAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    lead = {"id": "L-2", "company": "Massive Global Retail", "is_strategic_account": True, "message": "hi"}

    result = agent.qualify(lead)

    assert result.executed is False
    assert "strategic" in result.escalation_reason


def test_pricing_question_hard_escalates(audit_log, escalation_queue):
    agent = SalesAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    lead = {"id": "L-3", "company": "Bramble Studio", "is_strategic_account": False, "message": "What's your pricing for 8 seats?"}

    result = agent.qualify(lead)

    assert result.executed is False
    assert "pricing" in result.escalation_reason


def test_complaint_language_hard_escalates(audit_log, escalation_queue):
    agent = SalesAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    lead = {"id": "L-4", "company": "Acme", "is_strategic_account": False, "message": "considering legal action over your last outreach"}

    result = agent.qualify(lead)

    assert result.executed is False
    assert "complaint" in result.escalation_reason

from __future__ import annotations

from agents.escalation import Tier
from agents.support_agent import SupportAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient

KB = "## Resetting your password\nUse Settings > Security > Reset Password."


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return SupportAgent(llm, knowledge_base=KB, audit_log=audit_log, escalation_queue=escalation_queue, **kwargs)


def test_resolve_normal_ticket_executes(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "response": "Head to Settings > Security > Reset Password.",
            "kb_article_cited": "Resetting your password",
            "confidence": 0.92,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)
    ticket = {"id": "T-1", "subject": "reset", "body": "can't log in", "account_tier": "standard", "contact_count": 1}

    result = agent.resolve(ticket)

    assert result.executed is True
    assert result.tier == Tier.AUTONOMOUS
    assert result.output["kb_article_cited"] == "Resetting your password"


def test_refund_above_threshold_hard_escalates_without_calling_model(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue, refund_threshold=100.0)
    ticket = {
        "id": "T-2",
        "subject": "refund",
        "body": "please refund my last 3 invoices",
        "account_tier": "standard",
        "contact_count": 1,
        "requested_refund_amount": 480.0,
    }

    result = agent.resolve(ticket)

    assert result.executed is False
    assert "480.00" in result.escalation_reason
    assert escalation_queue.pending()


def test_enterprise_cancellation_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    ticket = {
        "id": "T-3",
        "subject": "cancelling",
        "body": "we are cancelling our enterprise contract",
        "account_tier": "enterprise",
        "contact_count": 1,
    }

    result = agent.triage(ticket)

    assert result.executed is False
    assert "enterprise/strategic" in result.escalation_reason


def test_legal_language_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    ticket = {"id": "T-4", "subject": "GDPR request", "body": "please provide data per GDPR", "contact_count": 1}

    result = agent.triage(ticket)

    assert result.executed is False
    assert "legal" in result.escalation_reason


def test_repeated_contact_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue, angry_contact_threshold=3)
    ticket = {"id": "T-5", "subject": "still broken", "body": "fix this please", "contact_count": 3}

    result = agent.triage(ticket)

    assert result.executed is False
    assert "escalated" in result.escalation_reason


def test_low_confidence_resolution_escalates(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "response": "Not sure, might need to check settings.",
            "kb_article_cited": None,
            "confidence": 0.3,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)
    ticket = {"id": "T-6", "subject": "weird issue", "body": "something strange happened", "contact_count": 1}

    result = agent.resolve(ticket)

    assert result.executed is False

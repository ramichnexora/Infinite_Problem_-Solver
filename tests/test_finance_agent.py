from __future__ import annotations

from agents.escalation import Tier
from agents.finance_agent import FinanceAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def test_normal_inbound_transaction_executes(audit_log, escalation_queue):
    llm = FakeLLMClient({"category": "Subscription Revenue", "confidence": 0.95, "escalate": False, "escalation_reason": None})
    agent = FinanceAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue)
    transaction = {"id": "TX-1", "amount": 49.0, "description": "SaaS subscription", "type": "inbound_payment"}

    result = agent.categorize_transaction(transaction)

    assert result.executed is True
    assert result.tier == Tier.AUTONOMOUS


def test_outbound_payment_always_hard_escalates(audit_log, escalation_queue):
    agent = FinanceAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    transaction = {"id": "TX-2", "amount": 1.0, "description": "tiny vendor payment", "type": "outbound_payment"}

    result = agent.categorize_transaction(transaction)

    assert result.executed is False
    assert "payment-initiation" in result.escalation_reason


def test_disputed_invoice_hard_escalates(audit_log, escalation_queue):
    agent = FinanceAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    transaction = {
        "id": "TX-3",
        "amount": 199.0,
        "description": "duplicate charge",
        "type": "inbound_payment",
        "customer_dispute": True,
    }

    result = agent.categorize_transaction(transaction)

    assert result.executed is False
    assert "disputes" in result.escalation_reason


def test_anomaly_hard_escalates(audit_log, escalation_queue):
    agent = FinanceAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    transaction = {
        "id": "TX-4",
        "amount": 15000.0,
        "description": "unexplained transfer",
        "type": "inbound_payment",
        "is_anomaly": True,
    }

    result = agent.categorize_transaction(transaction)

    assert result.executed is False
    assert "anomaly" in result.escalation_reason


def test_tax_question_hard_escalates(audit_log, escalation_queue):
    agent = FinanceAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    transaction = {
        "id": "TX-5",
        "amount": 300.0,
        "description": "reimbursement",
        "type": "inbound_payment",
        "tax_question": True,
    }

    result = agent.categorize_transaction(transaction)

    assert result.executed is False
    assert "tax" in result.escalation_reason

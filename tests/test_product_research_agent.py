from __future__ import annotations

from agents.escalation import Tier
from agents.product_research_agent import ProductResearchAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def test_normal_signal_clusters_and_executes(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "themes": [
                {
                    "theme": "Export reliability",
                    "frequency": 2,
                    "impact_summary": "Export fails or times out for some customers.",
                    "sources": ["support_ticket", "churn_survey"],
                }
            ],
            "brief": "Export reliability is the top theme this cycle.",
            "confidence": 0.85,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = ProductResearchAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue)
    signal_items = [
        {"source": "support_ticket", "account": "Acct-A", "text": "Export times out for large datasets."},
        {"source": "churn_survey", "account": "Acct-D", "text": "Left because export was unreliable."},
    ]

    result = agent.cluster_signal(signal_items)

    assert result.executed is True
    assert result.tier == Tier.AUTONOMOUS
    assert result.output["themes"][0]["theme"] == "Export reliability"


def test_security_signal_from_multiple_accounts_hard_escalates(audit_log, escalation_queue):
    agent = ProductResearchAgent(
        ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue, systemic_threshold=2
    )
    signal_items = [
        {"source": "support_ticket", "account": "Acct-E", "text": "Potential security vulnerability - saw another team's data."},
        {"source": "support_ticket", "account": "Acct-F", "text": "Similar security bug, exported report had another account's rows."},
    ]

    result = agent.cluster_signal(signal_items)

    assert result.executed is False
    assert "systemic" in result.escalation_reason
    assert escalation_queue.pending()


def test_single_security_mention_does_not_hard_escalate(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "themes": [],
            "brief": "n/a",
            "confidence": 0.8,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = ProductResearchAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue, systemic_threshold=2)
    signal_items = [
        {"source": "support_ticket", "account": "Acct-E", "text": "Possible security issue, only saw it once."},
    ]

    result = agent.cluster_signal(signal_items)

    assert result.executed is True

from __future__ import annotations

from agents.escalation import Tier
from agents.operations_agent import OperationsAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def test_normal_workflow_executes(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "nudge_message": "Friendly reminder this is due tomorrow.",
            "urgency": "low",
            "confidence": 0.9,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = OperationsAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue)
    workflow = {"id": "W-1", "name": "equipment request", "days_overdue": 0, "nudge_count": 0}

    result = agent.assess_workflow(workflow)

    assert result.executed is True
    assert result.tier == Tier.AUTONOMOUS


def test_access_change_request_hard_escalates(audit_log, escalation_queue):
    agent = OperationsAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    workflow = {"id": "W-2", "name": "access recert", "requests_access_change": True}

    result = agent.assess_workflow(workflow)

    assert result.executed is False
    assert "access" in result.escalation_reason


def test_overdue_past_final_nudge_hard_escalates(audit_log, escalation_queue):
    agent = OperationsAgent(
        ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue, final_nudge_threshold=3
    )
    workflow = {"id": "W-3", "name": "expense report", "days_overdue": 5, "nudge_count": 4}

    result = agent.assess_workflow(workflow)

    assert result.executed is False
    assert "final nudge" in result.escalation_reason


def test_broken_process_hard_escalates(audit_log, escalation_queue):
    agent = OperationsAgent(
        ExplodingLLMClient(),
        audit_log=audit_log,
        escalation_queue=escalation_queue,
        broken_process_owner_threshold=2,
    )
    workflow = {"id": "W-4", "name": "onboarding checklist", "days_overdue": 3, "distinct_owners_missed": 3}

    result = agent.assess_workflow(workflow)

    assert result.executed is False
    assert "process appears broken" in result.escalation_reason

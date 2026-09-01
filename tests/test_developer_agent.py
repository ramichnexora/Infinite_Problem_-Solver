from __future__ import annotations

from agents.developer_agent import DeveloperAgent
from agents.escalation import Tier
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return DeveloperAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue, **kwargs)


def test_routine_ticket_executes(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "plan": "Add an export button and wire it to the existing CSV helper.",
            "files_likely_touched": ["web/reports/ExportButton.tsx"],
            "test_plan": "Unit test the CSV helper; snapshot test the button.",
            "estimated_effort": "small",
            "confidence": 0.9,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)
    ticket = {"id": "D-1", "title": "Add export button", "description": "export to CSV"}

    result = agent.triage(ticket)

    assert result.executed is True
    assert result.tier == Tier.NOTIFY


def test_auth_area_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    ticket = {"id": "D-2", "title": "Fix login bug", "description": "update the authentication flow"}

    result = agent.triage(ticket)

    assert result.executed is False
    assert "auth" in result.escalation_reason


def test_migration_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    ticket = {"id": "D-3", "title": "Backfill totals", "description": "run a production data migration"}

    result = agent.triage(ticket)

    assert result.executed is False
    assert "migration" in result.escalation_reason


def test_no_test_plan_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    ticket = {"id": "D-4", "title": "Tweak copy", "description": "change the empty state text", "no_test_plan": True}

    result = agent.triage(ticket)

    assert result.executed is False
    assert "test plan" in result.escalation_reason


def test_production_hotfix_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    ticket = {
        "id": "D-5",
        "title": "Hotfix outage",
        "description": "patch the crash",
        "is_production_hotfix": True,
    }

    result = agent.triage(ticket)

    assert result.executed is False
    assert "hotfix" in result.escalation_reason

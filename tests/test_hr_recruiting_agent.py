from __future__ import annotations

from agents.escalation import Tier
from agents.hr_recruiting_agent import HRRecruitingAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def test_normal_candidate_executes(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "recommendation": "advance",
            "score": 82,
            "reasoning": "Meets all scorecard criteria.",
            "confidence": 0.9,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = HRRecruitingAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue)
    candidate = {
        "id": "H-1",
        "role": "Backend Engineer",
        "scorecard_criteria": "3+ years backend, Go or Python",
        "resume_summary": "4 years backend engineering, built a Go microservices platform.",
    }

    result = agent.screen(candidate)

    assert result.executed is True
    assert result.tier == Tier.NOTIFY


def test_compensation_negotiation_hard_escalates(audit_log, escalation_queue):
    agent = HRRecruitingAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    candidate = {
        "id": "H-2",
        "role": "Account Executive",
        "notes": "Asked what the base salary and equity range is before proceeding.",
    }

    result = agent.screen(candidate)

    assert result.executed is False
    assert "compensation" in result.escalation_reason


def test_legal_concern_hard_escalates(audit_log, escalation_queue):
    agent = HRRecruitingAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)
    candidate = {
        "id": "H-3",
        "role": "Support Specialist",
        "notes": "Felt a previous interviewer's questions were inappropriate and discriminatory.",
    }

    result = agent.screen(candidate)

    assert result.executed is False
    assert "legal" in result.escalation_reason

from __future__ import annotations

from agents.base import Agent
from agents.escalation import Tier
from tests.conftest import ExplodingLLMClient, FakeLLMClient


class DummyAgent(Agent):
    seat = "dummy-agent"


def test_hard_escalation_never_calls_the_model(audit_log, escalation_queue):
    agent = DummyAgent(ExplodingLLMClient(), audit_log=audit_log, escalation_queue=escalation_queue)

    result = agent.run_sop(
        sop="dummy_sop",
        system_prompt="unused",
        user_prompt="unused",
        inputs={"x": 1},
        default_tier=Tier.AUTONOMOUS,
        hard_escalation_reason="a deterministic guardrail fired",
    )

    assert result.executed is False
    assert result.tier == Tier.HUMAN_APPROVAL
    assert result.escalation_reason == "a deterministic guardrail fired"

    pending = escalation_queue.pending()
    assert len(pending) == 1
    assert pending[0]["reason"] == "a deterministic guardrail fired"
    assert pending[0]["tier"] == int(Tier.HUMAN_APPROVAL)

    records = audit_log.all()
    assert len(records) == 1
    assert records[0]["executed"] is False


def test_low_confidence_model_output_escalates(audit_log, escalation_queue):
    llm = FakeLLMClient({"confidence": 0.2, "escalate": False, "value": 42})
    agent = DummyAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue, confidence_threshold=0.7)

    result = agent.run_sop(
        sop="dummy_sop",
        system_prompt="sys",
        user_prompt="usr",
        inputs={},
        default_tier=Tier.AUTONOMOUS,
    )

    assert result.executed is False
    assert result.tier == Tier.HUMAN_APPROVAL
    assert "confidence" in result.escalation_reason
    assert escalation_queue.pending()


def test_model_requested_escalation_is_honored(audit_log, escalation_queue):
    llm = FakeLLMClient({"confidence": 0.95, "escalate": True, "escalation_reason": "not sure about this one"})
    agent = DummyAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue)

    result = agent.run_sop(
        sop="dummy_sop",
        system_prompt="sys",
        user_prompt="usr",
        inputs={},
        default_tier=Tier.AUTONOMOUS,
    )

    assert result.executed is False
    assert result.escalation_reason == "not sure about this one"


def test_confident_output_executes_at_default_tier(audit_log, escalation_queue):
    llm = FakeLLMClient({"confidence": 0.95, "escalate": False})
    agent = DummyAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue)

    result = agent.run_sop(
        sop="dummy_sop",
        system_prompt="sys",
        user_prompt="usr",
        inputs={},
        default_tier=Tier.NOTIFY,
    )

    assert result.executed is True
    assert result.tier == Tier.NOTIFY
    assert escalation_queue.pending() == []
    assert audit_log.all()[0]["executed"] is True

from __future__ import annotations

import json

import pytest

from agents.base import Agent
from agents.escalation import Tier
from agents.handoff import HandoffLLMClient, pending_handoffs, write_handoff
from agents.llm import build_llm_client
from agents.support_agent import SupportAgent


class BrokenLLMClient:
    def complete(self, *, system: str, user: str) -> str:
        raise ConnectionError("upstream unreachable")


class GarbageLLMClient:
    def complete(self, *, system: str, user: str) -> str:
        return "definitely not json"


def _agent(llm, tmp_path, audit_log, escalation_queue):
    agent = Agent(llm, audit_log, escalation_queue, handoff_inbox=tmp_path / "inbox")
    agent.seat = "support"
    return agent


def _run(agent):
    return agent.run_sop(
        sop="triage",
        system_prompt="SYSTEM PROMPT",
        user_prompt="USER PROMPT",
        inputs={"ticket_id": "T-1"},
        default_tier=Tier.AUTONOMOUS,
    )


def test_missing_api_key_writes_handoff_instead_of_crashing(
    tmp_path, audit_log, escalation_queue, monkeypatch
):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    llm = build_llm_client()
    assert isinstance(llm, HandoffLLMClient)

    result = _run(_agent(llm, tmp_path, audit_log, escalation_queue))

    assert result.executed is False
    assert result.tier == Tier.HUMAN_APPROVAL
    assert result.escalation_reason.startswith("handoff:")
    files = pending_handoffs(tmp_path / "inbox")
    assert len(files) == 1
    text = files[0].read_text(encoding="utf-8")
    assert "SYSTEM PROMPT" in text and "USER PROMPT" in text and '"ticket_id": "T-1"' in text
    assert "seat: support" in text and "sop: triage" in text
    assert escalation_queue.pending()[0]["reason"] == result.escalation_reason


@pytest.mark.parametrize("llm", [BrokenLLMClient(), GarbageLLMClient()])
def test_model_failure_becomes_handoff(llm, tmp_path, audit_log, escalation_queue):
    result = _run(_agent(llm, tmp_path, audit_log, escalation_queue))

    assert result.executed is False
    assert "handoff:" in result.escalation_reason
    assert len(pending_handoffs(tmp_path / "inbox")) == 1
    records = audit_log.path.read_text(encoding="utf-8").strip().splitlines()
    assert json.loads(records[-1])["executed"] is False


def test_hard_guardrail_never_writes_handoff(tmp_path, audit_log, escalation_queue):
    agent = SupportAgent(
        HandoffLLMClient(),
        knowledge_base="kb",
        audit_log=audit_log,
        escalation_queue=escalation_queue,
        handoff_inbox=tmp_path / "inbox",
    )
    result = agent.triage({"id": "T-9", "subject": "GDPR request", "body": "delete my data under GDPR"})
    assert result.executed is False
    assert not result.escalation_reason.startswith("handoff:")
    assert pending_handoffs(tmp_path / "inbox") == []


def test_pending_handoffs_ignores_done_files(tmp_path):
    h = write_handoff(
        seat="sales", sop="qualify", cause="test", system_prompt="s", user_prompt="u",
        inbox=tmp_path,
    )
    assert pending_handoffs(tmp_path) == [h.path]
    h.path.write_text(h.path.read_text(encoding="utf-8").replace("status: pending", "status: done"))
    assert pending_handoffs(tmp_path) == []

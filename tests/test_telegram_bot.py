from __future__ import annotations

from agents.support_agent import SupportAgent
from integrations.telegram_bot import handle_incoming_message
from tests.conftest import ExplodingLLMClient, FakeLLMClient

KB = "## Resetting your password\nUse Settings > Security > Reset Password."


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return SupportAgent(llm, knowledge_base=KB, audit_log=audit_log, escalation_queue=escalation_queue, **kwargs)


def test_resolved_message_replies_directly_with_no_ops_notification(audit_log, escalation_queue):
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

    outcome = handle_incoming_message(agent, chat_id=123, message_id=1, text="How do I reset my password?")

    assert outcome.reply_text == "Head to Settings > Security > Reset Password."
    assert outcome.notify_ops is None


def test_hard_escalated_message_gets_holding_reply_and_ops_notification(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)

    outcome = handle_incoming_message(
        agent, chat_id=456, message_id=2, text="Please provide all data you hold on me per GDPR"
    )

    assert "flagged this for a teammate" in outcome.reply_text
    assert outcome.notify_ops is not None
    assert "chat 456" in outcome.notify_ops
    assert "GDPR" in outcome.notify_ops


def test_low_confidence_message_escalates_with_ops_notification(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "response": "Not sure about this one.",
            "kb_article_cited": None,
            "confidence": 0.2,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)

    outcome = handle_incoming_message(agent, chat_id=789, message_id=3, text="Something strange is happening")

    assert "flagged this for a teammate" in outcome.reply_text
    assert outcome.notify_ops is not None

    pending = escalation_queue.pending()
    assert len(pending) == 1
    assert pending[0]["seat"] == "ai-support-agent"

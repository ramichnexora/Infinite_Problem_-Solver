"""AI Support Agent - implements docs/roles/ai-support.md.

SOPs implemented: triage (SOP 1) and resolve (SOP 2). Escalation triggers
from the role file are enforced as deterministic guardrails *before* the
model is ever called, per docs/01-principles.md principle 3 - the model is
never the sole judge of whether something is a legal, security, or angry-
customer situation.
"""
from __future__ import annotations

import re
from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

LEGAL_SECURITY_PATTERN = re.compile(
    r"\b(gdpr|ccpa|hipaa|lawsuit|subpoena|attorney|lawyer|data breach|breach of)\b",
    re.IGNORECASE,
)
CANCEL_PATTERN = re.compile(r"\b(cancel|cancelling|terminate|downgrade)\b", re.IGNORECASE)
HOSTILE_PATTERN = re.compile(
    r"\b(unacceptable|furious|going public|scam|fraud|never again|worst (company|service|support))\b",
    re.IGNORECASE,
)

TRIAGE_SYSTEM_PROMPT = """You are the AI Support Agent's triage step (SOP 1 in \
docs/roles/ai-support.md). Categorize the ticket and assess urgency using only the \
information given. Respond with JSON only, no prose, no code fences:

{{
  "category": "<billing|technical|account|feature_question|other>",
  "urgency": "<low|medium|high>",
  "confidence": <0.0-1.0, how confident you are in this categorization>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}}
"""

RESOLVE_SYSTEM_PROMPT = """You are the AI Support Agent's resolution step (SOP 2 in \
docs/roles/ai-support.md). Answer using ONLY the knowledge base below - if it doesn't \
cover the question, you must escalate rather than guess. Cite the KB article you used.

Knowledge base:
---
{kb}
---

Respond with JSON only, no prose, no code fences:
{{
  "response": "<the reply you would send to the customer>",
  "kb_article_cited": "<article title, or null if none applied>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}}
"""

EMAIL_REPLY_SYSTEM_PROMPT = """You are the AI Support Agent's inbound-email reply step \
(SOP 3). You draft the reply to a real email from a customer or prospect. Use ONLY the \
knowledge base below - if it doesn't cover the question, escalate rather than guess. \
Never invent a discount, refund, or promise not in the knowledge base.

Knowledge base:
---
{kb}
---

Respond with JSON only, no prose, no code fences:
{{
  "reply_body": "<the exact email reply text, friendly and concise>",
  "kb_article_cited": "<article title, or null>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}}
"""

SOCIAL_REPLY_SYSTEM_PROMPT = """You are the AI Support Agent's social-media reply step \
(SOP 4), replying to a public comment or DM on Instagram/Facebook/TikTok. The reply is \
PUBLIC unless the source says it's a DM - never share order details, personal data, or \
troubleshooting steps that require verifying identity in a public comment; ask the \
person to DM instead. Keep tone warm and on-brand for a new-parent audience. Use ONLY \
the knowledge base below.

Knowledge base:
---
{kb}
---

Respond with JSON only, no prose, no code fences:
{{
  "reply_body": "<the exact public/DM reply text>",
  "is_public": <true|false>,
  "kb_article_cited": "<article title, or null>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}}
"""


class SupportAgent(Agent):
    seat = "ai-support-agent"

    def __init__(
        self,
        llm,
        knowledge_base: str,
        refund_threshold: float = 100.0,
        angry_contact_threshold: int = 3,
        **kwargs: Any,
    ):
        super().__init__(llm, **kwargs)
        self.knowledge_base = knowledge_base
        self.refund_threshold = refund_threshold
        self.angry_contact_threshold = angry_contact_threshold

    def _hard_escalation_reason(self, ticket: dict[str, Any]) -> str | None:
        text = f"{ticket.get('subject', '')} {ticket.get('body', '')}"

        refund = ticket.get("requested_refund_amount")
        if refund is not None and refund > self.refund_threshold:
            return (
                f"refund request ${refund:.2f} exceeds the pre-approved threshold "
                f"${self.refund_threshold:.2f}"
            )

        if ticket.get("account_tier") in ("enterprise", "strategic") and CANCEL_PATTERN.search(text):
            return "cancellation intent from an enterprise/strategic account"

        if LEGAL_SECURITY_PATTERN.search(text):
            return "legal/security/data-privacy language detected in ticket"

        contact_count = ticket.get("contact_count", 1)
        if contact_count >= self.angry_contact_threshold or HOSTILE_PATTERN.search(text):
            return "customer appears escalated (repeated contact or hostile language)"

        return None

    def triage(self, ticket: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(ticket)
        user_prompt = (
            f"Subject: {ticket.get('subject', '')}\n"
            f"Body: {ticket.get('body', '')}\n"
            f"Account tier: {ticket.get('account_tier', 'standard')}\n"
            f"Prior contacts on this issue: {ticket.get('contact_count', 1)}\n"
        )
        return self.run_sop(
            sop="triage",
            system_prompt=TRIAGE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"ticket_id": ticket.get("id")},
            default_tier=Tier.AUTONOMOUS,
            hard_escalation_reason=hard_reason,
        )

    def resolve(self, ticket: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(ticket)
        user_prompt = (
            f"Subject: {ticket.get('subject', '')}\n"
            f"Body: {ticket.get('body', '')}\n"
            f"Account tier: {ticket.get('account_tier', 'standard')}\n"
        )
        return self.run_sop(
            sop="resolve",
            system_prompt=RESOLVE_SYSTEM_PROMPT.format(kb=self.knowledge_base),
            user_prompt=user_prompt,
            inputs={"ticket_id": ticket.get("id")},
            default_tier=Tier.AUTONOMOUS,
            hard_escalation_reason=hard_reason,
        )

    def reply_email(self, message: dict[str, Any]) -> AgentResult:
        """SOP 3 - Draft a reply to an inbound email.

        Args:
            message: dict with 'subject', 'body', 'from_email', optionally
                'account_tier', 'contact_count', 'requested_refund_amount'
        """
        hard_reason = self._hard_escalation_reason(message)
        user_prompt = (
            f"From: {message.get('from_email', '')}\n"
            f"Subject: {message.get('subject', '')}\n"
            f"Body: {message.get('body', '')}\n"
        )
        return self.run_sop(
            sop="reply_email",
            system_prompt=EMAIL_REPLY_SYSTEM_PROMPT.format(kb=self.knowledge_base),
            user_prompt=user_prompt,
            inputs={"from_email": message.get("from_email")},
            default_tier=Tier.AUTONOMOUS,
            hard_escalation_reason=hard_reason,
        )

    def reply_social_comment(self, comment: dict[str, Any]) -> AgentResult:
        """SOP 4 - Draft a reply to a social-media comment or DM.

        Args:
            comment: dict with 'platform', 'text', 'is_public' (bool),
                'author_handle', optionally 'contact_count'
        """
        hard_reason = self._hard_escalation_reason({"body": comment.get("text", ""),
                                                       "contact_count": comment.get("contact_count", 1)})
        user_prompt = (
            f"Platform: {comment.get('platform', '')}\n"
            f"Public: {comment.get('is_public', True)}\n"
            f"Author: {comment.get('author_handle', '')}\n"
            f"Text: {comment.get('text', '')}\n"
        )
        return self.run_sop(
            sop="reply_social_comment",
            system_prompt=SOCIAL_REPLY_SYSTEM_PROMPT.format(kb=self.knowledge_base),
            user_prompt=user_prompt,
            inputs={"platform": comment.get("platform"), "author": comment.get("author_handle")},
            default_tier=Tier.AUTONOMOUS,
            hard_escalation_reason=hard_reason,
        )

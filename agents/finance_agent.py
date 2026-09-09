"""AI Finance Agent - implements the reconcile/categorize step of
docs/roles/ai-finance.md (SOP 1).

docs/roles/ai-finance.md is explicit that this is "the one seat where
'earned autonomy' does not extend to outbound payments" - so outbound
payment transactions hard-escalate unconditionally here, with no
threshold or confidence score that could ever let one through
autonomously. Disputes, suspected duplicates/anomalies, and tax questions
are also hard guardrails per the role file's escalation triggers.
"""
from __future__ import annotations

from typing import Any

from .base import Agent, AgentResult
from .escalation import Tier

CATEGORIZE_SYSTEM_PROMPT = """You are the AI Finance Agent's reconciliation step (SOP 1 \
in docs/roles/ai-finance.md). Categorize the transaction against the standard chart of \
accounts categories using only the information given.

Respond with JSON only, no prose, no code fences:
{
  "category": "<chart-of-accounts category>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""


class FinanceAgent(Agent):
    seat = "finance"

    def _hard_escalation_reason(self, transaction: dict[str, Any]) -> str | None:
        # Outbound payments are never autonomous, at any amount, regardless of
        # autonomy tier or model confidence - see docs/roles/ai-finance.md.
        if transaction.get("type") == "outbound_payment":
            return "outbound payment - payment-initiation always requires human approval, no exceptions"

        if transaction.get("customer_dispute"):
            return "customer disputes this invoice or requests a payment plan/term change"

        if transaction.get("is_duplicate_suspected") or transaction.get("is_anomaly"):
            return "transaction may be a duplicate/fraud/billing anomaly"

        if transaction.get("tax_question"):
            return "transaction raises a tax-treatment or compliance question"

        return None

    def categorize_transaction(self, transaction: dict[str, Any]) -> AgentResult:
        hard_reason = self._hard_escalation_reason(transaction)
        user_prompt = (
            f"Amount: {transaction.get('amount')}\n"
            f"Description: {transaction.get('description', '')}\n"
            f"Type: {transaction.get('type', 'unknown')}\n"
        )
        return self.run_sop(
            sop="reconcile",
            system_prompt=CATEGORIZE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            inputs={"transaction_id": transaction.get("id")},
            default_tier=Tier.AUTONOMOUS,
            hard_escalation_reason=hard_reason,
        )

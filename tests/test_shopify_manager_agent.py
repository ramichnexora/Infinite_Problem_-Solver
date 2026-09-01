from __future__ import annotations

from agents.escalation import Tier
from agents.shopify_manager_agent import ShopifyManagerAgent
from tests.conftest import ExplodingLLMClient, FakeLLMClient


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return ShopifyManagerAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue, **kwargs)


def test_routine_inventory_update_executes(audit_log, escalation_queue):
    llm = FakeLLMClient(
        {
            "action_summary": "Update inventory count to 140 units.",
            "updated_fields": {"inventory_count": 140},
            "confidence": 0.95,
            "escalate": False,
            "escalation_reason": None,
        }
    )
    agent = make_agent(llm, audit_log, escalation_queue)
    request = {
        "id": "SHP-1",
        "product_title": "Tote",
        "change_type": "inventory_update",
        "current_price": 28.0,
        "new_price": 28.0,
        "new_inventory_count": 140,
    }

    result = agent.review_change(request)

    assert result.executed is True
    assert result.tier == Tier.NOTIFY


def test_refund_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    request = {"id": "SHP-2", "product_title": "Hoodie", "change_type": "refund"}

    result = agent.review_change(request)

    assert result.executed is False
    assert "refund" in result.escalation_reason


def test_large_price_change_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue, price_change_pct_threshold=15.0)
    request = {
        "id": "SHP-3",
        "product_title": "Sneaker",
        "change_type": "price_change",
        "current_price": 60.0,
        "new_price": 90.0,
    }

    result = agent.review_change(request)

    assert result.executed is False
    assert "price change" in result.escalation_reason


def test_best_seller_out_of_stock_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    request = {
        "id": "SHP-4",
        "product_title": "Signature Hoodie",
        "change_type": "inventory_update",
        "is_best_seller": True,
        "new_inventory_count": 0,
    }

    result = agent.review_change(request)

    assert result.executed is False
    assert "best-selling" in result.escalation_reason


def test_legal_claim_hard_escalates(audit_log, escalation_queue):
    agent = make_agent(ExplodingLLMClient(), audit_log, escalation_queue)
    request = {
        "id": "SHP-5",
        "product_title": "Supplement",
        "change_type": "listing_copy",
        "involves_legal_or_health_claim": True,
    }

    result = agent.review_change(request)

    assert result.executed is False
    assert "compliance" in result.escalation_reason

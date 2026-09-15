from __future__ import annotations

from agents.escalation import Tier
from agents.shopify_product_agent import ShopifyProductAgent
from tests.conftest import FakeLLMClient

_SPECIALIST_RESPONSES = {
    "product": {
        "title": "The AI Side Hustle Playbook",
        "product_type": "Digital Guide",
        "vendor": "Infinite Problem Solver",
        "tags": ["ai-tools", "side-hustle"],
        "collections": ["Digital Guides"],
        "sku": "AISH-001",
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    },
    "cro": {
        "page_structure": ["hero", "what's inside", "faq", "cta"],
        "primary_cta": "Get the Playbook",
        "trust_signals": ["Written by a working founder, not a marketer"],
        "faq": [{"q": "Is this a PDF?", "a": "Yes, instant digital download."}],
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    },
    "seo": {
        "seo_title": "AI Side Hustle Playbook",
        "meta_description": "A practical guide to automating freelance work with AI.",
        "handle": "ai-side-hustle-playbook",
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    },
    "digital_delivery": {
        "file_plan": ["playbook.pdf"],
        "delivery_method": "Shopify digital download app",
        "format_notes": "none",
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    },
    "merchandising": {
        "cross_sell": ["Debt Snowball Reality Check"],
        "upsell": [],
        "bundle_suggestion": None,
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    },
    "pricing": {
        "price_usd": 29,
        "compare_at_price_usd": None,
        "offer": None,
        "price_justification": "Replaces hours of trial-and-error prompting.",
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    },
    "copywriting": {
        "description_html": "<p>What's inside: 5 real automations...</p>",
        "refund_policy_note": "confirm with founder",
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    },
    "visual": {
        "cover_brief": "Laptop + coffee, warm light, no stock-photo cliches",
        "gallery_briefs": ["Screenshot of the automation in action"],
        "palette_notes": "matches existing dusty-rose brand palette",
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    },
    "analytics": {
        "tracking_checklist": ["conversion rate", "refund rate"],
        "success_metric": "10 sales in first 14 days",
        "review_after_days": 14,
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    },
}

_QA_PASS = {
    "scores": {"cro": 92, "seo": 90, "ux": 91, "offer": 90, "technical": 95},
    "overall": 92,
    "launch_ready": True,
    "fixes_needed": [],
    "confidence": 0.9,
    "escalate": False,
    "escalation_reason": None,
}

_QA_FAIL = {
    "scores": {"cro": 60, "seo": 90, "ux": 91, "offer": 90, "technical": 95},
    "overall": 85,
    "launch_ready": False,
    "fixes_needed": ["CTA is generic, needs to reflect the actual outcome"],
    "confidence": 0.9,
    "escalate": False,
    "escalation_reason": None,
}


def _sop_order():
    return [
        "product",
        "cro",
        "seo",
        "digital_delivery",
        "merchandising",
        "pricing",
        "copywriting",
        "visual",
        "analytics",
    ]


def make_agent(llm, audit_log, escalation_queue, **kwargs):
    return ShopifyProductAgent(llm, audit_log=audit_log, escalation_queue=escalation_queue, **kwargs)


def test_seat_id_matches_registry():
    assert ShopifyProductAgent.seat == "shopify_product"


def test_build_product_passes_qa_gate_and_returns_preview(audit_log, escalation_queue):
    responses = [_SPECIALIST_RESPONSES[sop] for sop in _sop_order()] + [_QA_PASS]
    llm = FakeLLMClient(responses)
    agent = make_agent(llm, audit_log, escalation_queue)

    result = agent.build_product("The AI Side Hustle Playbook", source_files=None, brand_context="")

    assert result.executed is True
    assert result.tier == Tier.HUMAN_APPROVAL  # Gate 1 - always Tier 3
    assert result.output["gate_passed"] is True
    assert "SHOPIFY IMPLEMENTATION PREVIEW" in result.output["preview"]
    assert result.output["qa"]["overall"] == 92


def test_build_product_stops_and_reports_fixes_below_qa_gate(audit_log, escalation_queue):
    responses = [_SPECIALIST_RESPONSES[sop] for sop in _sop_order()] + [_QA_FAIL]
    llm = FakeLLMClient(responses)
    agent = make_agent(llm, audit_log, escalation_queue)

    result = agent.build_product("The AI Side Hustle Playbook", source_files=None, brand_context="")

    # Below 90 overall (or any dimension below 70) - never presented as ready.
    assert result.executed is False
    assert result.output["gate_passed"] is False
    assert result.output["preview"] is None
    assert "fixes needed" in (result.escalation_reason or "").lower()


def test_build_product_stops_at_first_specialist_escalation(audit_log, escalation_queue):
    low_confidence_product = dict(_SPECIALIST_RESPONSES["product"])
    low_confidence_product["confidence"] = 0.1
    llm = FakeLLMClient([low_confidence_product])
    agent = make_agent(llm, audit_log, escalation_queue)

    result = agent.build_product("The AI Side Hustle Playbook", source_files=None, brand_context="")

    assert result.executed is False
    # Only the "product" SOP should have been called - the pipeline must not
    # keep going once an early specialist escalates.
    assert len(llm.calls) == 1


def test_qa_gate_requires_min_dimension_not_just_average(audit_log, escalation_queue):
    """A high average with one very low dimension must still fail the gate -
    it isn't just overall >= 90."""
    responses = [_SPECIALIST_RESPONSES[sop] for sop in _sop_order()]
    borderline_qa = {
        "scores": {"cro": 50, "seo": 100, "ux": 100, "offer": 100, "technical": 100},
        "overall": 90,
        "launch_ready": False,
        "fixes_needed": ["CRO structure is broken"],
        "confidence": 0.9,
        "escalate": False,
        "escalation_reason": None,
    }
    llm = FakeLLMClient(responses + [borderline_qa])
    agent = make_agent(llm, audit_log, escalation_queue)

    result = agent.build_product("The AI Side Hustle Playbook", source_files=None, brand_context="")

    assert result.executed is False
    assert result.output["gate_passed"] is False


def test_publish_product_never_auto_executes(audit_log, escalation_queue):
    """publish_product() is Gate 2 - a hard stop with no model call, always escalated."""
    llm = FakeLLMClient({})  # should never be called
    agent = make_agent(llm, audit_log, escalation_queue)

    result = agent.publish_product("gid://shopify/Product/1")

    assert result.executed is False
    assert result.tier == Tier.HUMAN_APPROVAL
    assert len(llm.calls) == 0
    assert "FINAL PUBLISH CHECK" in result.output["preview"]


def test_publish_product_confirmed_requires_shopify_client(audit_log, escalation_queue):
    llm = FakeLLMClient({})
    agent = make_agent(llm, audit_log, escalation_queue)  # no shopify_client passed

    try:
        agent.publish_product_confirmed("gid://shopify/Product/1")
        assert False, "expected RuntimeError when no shopify_client is configured"
    except RuntimeError as exc:
        assert "shopify_client" in str(exc)


def test_create_shopify_draft_uses_shopify_client(audit_log, escalation_queue):
    class FakeShopifyClient:
        def create_product_draft(self, spec):
            return {"product_id": "gid://1", "variant_id": "gid://v1", "status": "DRAFT"}

        def verify_product(self, product_id, expected):
            return {"product": {}, "mismatches": [], "verified": True}

    llm = FakeLLMClient({})
    agent = make_agent(llm, audit_log, escalation_queue, shopify_client=FakeShopifyClient())

    plan = {
        "product": {"title": "T", "product_type": "Digital Guide", "tags": []},
        "copywriting": {"description_html": "<p>x</p>"},
        "seo": {"handle": "t"},
        "pricing": {"price_usd": 29},
    }
    report = agent.create_shopify_draft(plan)

    assert report["status"] == "DRAFT"
    assert report["verification"]["verified"] is True

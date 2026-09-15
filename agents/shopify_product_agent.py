"""AI Shopify Product Agent - turns an approved title (+ optional source files)
into a fully specified, QA'd, human-approved Shopify product, per the founder's
"INFINITE SHOPIFY MASTER AGENT" spec (docs/roles/ai-shopify-product.md).

The spec describes 10 named specialist roles (Product, CRO, SEO, Digital
Delivery, Merchandising, Pricing, Copywriting, Visual, Analytics, QA). This
repo's existing convention (every seat, one Agent class, one run_sop() call
per specialist step - see marketing_agent.py's Plan/Draft/Publish, or
digital_product_agent.py's draft/qa) is kept here rather than 10 separate
files: 10 real, separately-audited SOP methods on one seat, so the audit
trail still shows 10 distinct specialist decisions without the un-scoped
seat sprawl docs/01-principles.md #8 warns against.

Two Human Approval Gates, matching the spec exactly:
  Gate 1 (build_product) - every specialist SOP + qa() run before a human
    ever sees anything; qa() gates at 90 overall, below that build_product()
    stops and reports fixes rather than proceeding. Always Tier 3 - product
    launches are never auto-executed (docs/roles/human-founder.md's standing
    outbound-communication rule, already extended to digital_product_agent).
  Gate 2 (publish_product) - after create_shopify_draft() creates the DRAFT
    product and verify_product() confirms every approved field actually
    landed, a second explicit Tier 3 stop before DRAFT -> ACTIVE.

Nothing in this file talks to Shopify directly - integrations/shopify_admin.py
does that, called only by create_shopify_draft()/publish_product(), never by
the specialist SOPs themselves.
"""
from __future__ import annotations

from typing import Any, Optional

from .base import Agent, AgentResult
from .escalation import Tier

# --- Specialist system prompts (10 roles from the founder's spec) ---------

PRODUCT_SYSTEM_PROMPT = """You are the Product specialist (SOP 1 of 10) for a new Shopify \
digital product. Given an approved title and any source material, define the product's \
core shape.

Respond with JSON only, no prose, no code fences:
{
  "title": "<final product title>",
  "product_type": "<e.g. Digital Guide>",
  "vendor": "<store name>",
  "tags": ["<tag>", ...],
  "collections": ["<collection name>", ...],
  "sku": "<sku>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

CRO_SYSTEM_PROMPT = """You are the CRO (conversion rate optimization) specialist (SOP 2 of \
10). Given the product basics, define the product page's conversion structure.

Respond with JSON only, no prose, no code fences:
{
  "page_structure": ["<section, in order>", ...],
  "primary_cta": "<exact CTA button text>",
  "trust_signals": ["<real, honest trust signal - no invented reviews/counts>", ...],
  "faq": [{"q": "<question>", "a": "<answer>"}, ...],
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

SEO_SYSTEM_PROMPT = """You are the SEO specialist (SOP 3 of 10). Given the product basics, \
write the on-page SEO fields.

Respond with JSON only, no prose, no code fences:
{
  "seo_title": "<<=60 chars>",
  "meta_description": "<<=160 chars, honest, no invented claims>",
  "handle": "<url-slug>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

DIGITAL_DELIVERY_SYSTEM_PROMPT = """You are the Digital Delivery specialist (SOP 4 of 10). \
Given the product basics and any source files described, plan how the buyer receives the \
product after purchase.

Respond with JSON only, no prose, no code fences:
{
  "file_plan": ["<file name and what it contains>", ...],
  "delivery_method": "<e.g. Shopify digital download app, email fulfillment>",
  "format_notes": "<any conversion/formatting the source files still need>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

MERCHANDISING_SYSTEM_PROMPT = """You are the Merchandising specialist (SOP 5 of 10). Given \
the product basics, plan cross-sell and upsell placement within the existing catalog.

Respond with JSON only, no prose, no code fences:
{
  "cross_sell": ["<existing product/collection this pairs with>", ...],
  "upsell": ["<existing product this could upsell to, or null if none fits>", ...],
  "bundle_suggestion": "<a real bundle idea, or null if none makes sense>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

PRICING_SYSTEM_PROMPT = """You are the Pricing specialist (SOP 6 of 10). Given the product \
basics, set price and any launch offer.

Rules: never invent a "was $X" anchor price unless one is actually given to you - inventing \
a fake original price is a deceptive-pricing violation.

Respond with JSON only, no prose, no code fences:
{
  "price_usd": <number>,
  "compare_at_price_usd": <number or null - only if a real anchor price was given>,
  "offer": "<launch offer description, or null>",
  "price_justification": "<honest one or two sentences>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

COPYWRITING_SYSTEM_PROMPT = """You are the Copywriting specialist (SOP 7 of 10). Given the \
product basics and CRO page structure, write the actual product description copy.

Rules: state concretely what's inside (real content, not vague marketing fluff). Never \
invent a statistic, guarantee, or refund policy not given to you.

Respond with JSON only, no prose, no code fences:
{
  "description_html": "<full HTML description, ready to paste into Shopify>",
  "refund_policy_note": "<confirm with founder, or the given policy if one was provided>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

VISUAL_SYSTEM_PROMPT = """You are the Visual specialist (SOP 8 of 10). Given the product \
basics, write a media brief for whoever designs the product images/cover.

Respond with JSON only, no prose, no code fences:
{
  "cover_brief": "<what the primary product image should show>",
  "gallery_briefs": ["<additional image brief>", ...],
  "palette_notes": "<color/style direction consistent with the store's existing brand>",
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

ANALYTICS_SYSTEM_PROMPT = """You are the Analytics specialist (SOP 9 of 10). Given the \
product basics, define what to track once this product is live.

Respond with JSON only, no prose, no code fences:
{
  "tracking_checklist": ["<event/metric to confirm is tracked>", ...],
  "success_metric": "<the one metric that defines launch success>",
  "review_after_days": <integer>,
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

QA_SYSTEM_PROMPT = """You are the QA specialist (SOP 10 of 10) - the final gate before a \
human ever sees this as a launch-ready "SHOPIFY IMPLEMENTATION PREVIEW". Score the full \
assembled product plan 0-100 on each dimension below. Below 90 overall, this does not \
proceed - list exactly what to fix.

Dimensions:
- cro: is the page structure and CTA actually built to convert?
- seo: are the SEO fields complete and honest?
- ux: does digital delivery + merchandising fit together cleanly for the buyer?
- offer: is pricing honest (no invented anchor price) and does the offer make sense?
- technical: title/description/price/tags/sku/handle all present and non-generic?

Respond with JSON only, no prose, no code fences:
{
  "scores": {"cro": <0-100>, "seo": <0-100>, "ux": <0-100>, "offer": <0-100>, "technical": <0-100>},
  "overall": <0-100, average>,
  "launch_ready": <true|false, true only if overall >= 90 AND no dimension below 70>,
  "fixes_needed": ["<specific fix>", ...],
  "confidence": <0.0-1.0>,
  "escalate": <true|false>,
  "escalation_reason": "<reason, or null>"
}
"""

_QA_GATE_OVERALL = 90
_QA_GATE_MIN_DIMENSION = 70


class ShopifyProductAgent(Agent):
    seat = "shopify_product"

    def __init__(self, *args: Any, shopify_client: Any = None, **kwargs: Any) -> None:
        """`shopify_client` is optional - a integrations.shopify_admin.ShopifyAdminClient
        (or a test double). Only used by create_shopify_draft()/publish_product(); every
        specialist SOP and qa() run without it."""
        super().__init__(*args, **kwargs)
        self.shopify_client = shopify_client

    # --- 10 specialist SOPs -------------------------------------------

    def product(self, title: str, source_files: list[str] | None, brand_context: str) -> AgentResult:
        return self._run_specialist(
            "product",
            PRODUCT_SYSTEM_PROMPT,
            f"Title: {title}\nSource files: {source_files or []}\nBrand context: {brand_context}\n",
            {"title": title},
        )

    def cro(self, title: str, product_basics: dict[str, Any]) -> AgentResult:
        return self._run_specialist(
            "cro",
            CRO_SYSTEM_PROMPT,
            f"Title: {title}\nProduct basics: {product_basics}\n",
            {"title": title},
        )

    def seo(self, title: str, product_basics: dict[str, Any]) -> AgentResult:
        return self._run_specialist(
            "seo",
            SEO_SYSTEM_PROMPT,
            f"Title: {title}\nProduct basics: {product_basics}\n",
            {"title": title},
        )

    def digital_delivery(self, title: str, source_files: list[str] | None) -> AgentResult:
        return self._run_specialist(
            "digital_delivery",
            DIGITAL_DELIVERY_SYSTEM_PROMPT,
            f"Title: {title}\nSource files: {source_files or []}\n",
            {"title": title},
        )

    def merchandising(self, title: str, product_basics: dict[str, Any]) -> AgentResult:
        return self._run_specialist(
            "merchandising",
            MERCHANDISING_SYSTEM_PROMPT,
            f"Title: {title}\nProduct basics: {product_basics}\n",
            {"title": title},
        )

    def pricing(self, title: str, product_basics: dict[str, Any], price_hint: float | None = None) -> AgentResult:
        return self._run_specialist(
            "pricing",
            PRICING_SYSTEM_PROMPT,
            f"Title: {title}\nProduct basics: {product_basics}\n"
            f"Price hint: {price_hint if price_hint is not None else 'not specified - propose one'}\n",
            {"title": title},
        )

    def copywriting(self, title: str, product_basics: dict[str, Any], cro_output: dict[str, Any]) -> AgentResult:
        return self._run_specialist(
            "copywriting",
            COPYWRITING_SYSTEM_PROMPT,
            f"Title: {title}\nProduct basics: {product_basics}\nCRO page structure: {cro_output}\n",
            {"title": title},
        )

    def visual(self, title: str, product_basics: dict[str, Any]) -> AgentResult:
        return self._run_specialist(
            "visual",
            VISUAL_SYSTEM_PROMPT,
            f"Title: {title}\nProduct basics: {product_basics}\n",
            {"title": title},
        )

    def analytics(self, title: str, product_basics: dict[str, Any]) -> AgentResult:
        return self._run_specialist(
            "analytics",
            ANALYTICS_SYSTEM_PROMPT,
            f"Title: {title}\nProduct basics: {product_basics}\n",
            {"title": title},
        )

    def qa(self, plan: dict[str, Any]) -> AgentResult:
        """SOP 10 - final gate at 90 overall / 70 per-dimension before Gate 1."""
        return self._run_specialist(
            "qa",
            QA_SYSTEM_PROMPT,
            f"Assembled product plan: {plan}\n",
            {"title": plan.get("product", {}).get("title")},
        )

    def _run_specialist(
        self, sop: str, system_prompt: str, user_prompt: str, inputs: dict[str, Any]
    ) -> AgentResult:
        # Specialist SOPs feed the orchestrator, not a human directly - they
        # execute at whatever tier the model earns (confidence gate still
        # applies); only build_product()'s final preview and publish_product()
        # are hard Tier 3, per the spec's "never publish automatically" rule.
        return self.run_sop(
            sop=sop,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            inputs=inputs,
            default_tier=Tier.NOTIFY,
        )

    # --- Master orchestration -------------------------------------------

    def build_product(
        self, title: str, source_files: list[str] | None = None, brand_context: str = ""
    ) -> AgentResult:
        """Run all 10 specialist SOPs in sequence, then qa(). Always returns
        Tier 3 (Human Approval Gate #1) - matches the spec's "never publish
        automatically". Below the QA gate (90 overall / 70 per dimension),
        stops and reports fixes instead of presenting a half-finished plan
        as ready."""
        product_result = self.product(title, source_files, brand_context)
        if not product_result.executed:
            return product_result
        product_basics = product_result.output

        cro_result = self.cro(title, product_basics)
        if not cro_result.executed:
            return cro_result

        seo_result = self.seo(title, product_basics)
        if not seo_result.executed:
            return seo_result

        delivery_result = self.digital_delivery(title, source_files)
        if not delivery_result.executed:
            return delivery_result

        merch_result = self.merchandising(title, product_basics)
        if not merch_result.executed:
            return merch_result

        pricing_result = self.pricing(title, product_basics)
        if not pricing_result.executed:
            return pricing_result

        copy_result = self.copywriting(title, product_basics, cro_result.output)
        if not copy_result.executed:
            return copy_result

        visual_result = self.visual(title, product_basics)
        if not visual_result.executed:
            return visual_result

        analytics_result = self.analytics(title, product_basics)
        if not analytics_result.executed:
            return analytics_result

        plan = {
            "product": product_basics,
            "cro": cro_result.output,
            "seo": seo_result.output,
            "digital_delivery": delivery_result.output,
            "merchandising": merch_result.output,
            "pricing": pricing_result.output,
            "copywriting": copy_result.output,
            "visual": visual_result.output,
            "analytics": analytics_result.output,
        }

        qa_result = self.qa(plan)
        if not qa_result.executed:
            return qa_result

        qa_output = qa_result.output
        scores = qa_output.get("scores", {})
        gate_passed = qa_output.get("overall", 0) >= _QA_GATE_OVERALL and all(
            v >= _QA_GATE_MIN_DIMENSION for v in scores.values()
        )

        if not gate_passed:
            # Below the gate: report fixes, never proceed to the human as "ready".
            result = AgentResult(
                output={
                    "plan": plan,
                    "qa": qa_output,
                    "preview": None,
                    "gate_passed": False,
                },
                tier=Tier.HUMAN_APPROVAL,
                executed=False,
                escalation_reason=f"QA gate not met: {qa_output.get('overall')} overall "
                f"(need >={_QA_GATE_OVERALL}, no dimension below {_QA_GATE_MIN_DIMENSION}) - "
                f"fixes needed: {qa_output.get('fixes_needed')}",
            )
            self._finish("build_product", {"title": title}, result)
            return result

        result = AgentResult(
            output={
                "plan": plan,
                "qa": qa_output,
                "preview": self._format_implementation_preview(plan, qa_output),
                "gate_passed": True,
            },
            tier=Tier.HUMAN_APPROVAL,
            executed=True,
        )
        self._finish("build_product", {"title": title}, result)
        return result

    @staticmethod
    def _format_implementation_preview(plan: dict[str, Any], qa_output: dict[str, Any]) -> str:
        product = plan["product"]
        pricing = plan["pricing"]
        return (
            "SHOPIFY IMPLEMENTATION PREVIEW\n"
            f"Title: {product.get('title')}\n"
            f"Type: {product.get('product_type')} | SKU: {product.get('sku')}\n"
            f"Price: ${pricing.get('price_usd')} ({pricing.get('price_justification')})\n"
            f"Tags: {product.get('tags')}\n"
            f"Collections: {product.get('collections')}\n"
            f"QA: {qa_output.get('overall')}/100 - launch_ready={qa_output.get('launch_ready')}\n"
            "Status: DRAFT ONLY until explicit approval + publish_product().\n"
        )

    # --- Execution (only after Gate 1 approval) --------------------------

    def create_shopify_draft(self, plan: dict[str, Any]) -> dict[str, Any]:
        """Create the Shopify product as DRAFT via integrations/shopify_admin.py, then
        re-verify every approved field actually landed. Only call this after a human has
        approved build_product()'s output. Returns the "SHOPIFY DEPLOYMENT REPORT" data."""
        if self.shopify_client is None:
            raise RuntimeError(
                "No shopify_client configured - see integrations/shopify_admin.py::client_from_env()."
            )
        product = plan["product"]
        copy = plan["copywriting"]
        seo = plan["seo"]
        pricing = plan["pricing"]

        spec = {
            "title": product.get("title"),
            "description_html": copy.get("description_html"),
            "price_usd": pricing.get("price_usd"),
            "product_type": product.get("product_type"),
            "tags": product.get("tags", []),
            "handle": seo.get("handle"),
        }
        created = self.shopify_client.create_product_draft(spec)
        verification = self.shopify_client.verify_product(created["product_id"], spec)
        return {
            "product_id": created["product_id"],
            "variant_id": created["variant_id"],
            "status": created["status"],
            "verification": verification,
        }

    def publish_product(self, product_id: str) -> AgentResult:
        """Human Approval Gate #2 - "FINAL PUBLISH CHECK". Only ever executes
        DRAFT -> ACTIVE on an explicit, separate approval; default_tier is
        HUMAN_APPROVAL so it never auto-executes even at full model confidence
        (there is no model call here - this is a hard gate, not a scored one)."""
        result = AgentResult(
            output={
                "product_id": product_id,
                "action": "publish",
                "preview": f"FINAL PUBLISH CHECK\nProduct: {product_id}\n"
                "This will flip status DRAFT -> ACTIVE on the live store. "
                "Requires explicit approval - call publish_product_confirmed() to execute.",
            },
            tier=Tier.HUMAN_APPROVAL,
            executed=False,
            escalation_reason="Gate 2: explicit publish approval required before going live.",
        )
        self._finish("publish_product", {"product_id": product_id}, result)
        return result

    def publish_product_confirmed(self, product_id: str) -> dict[str, Any]:
        """The actual DRAFT -> ACTIVE call - only invoke after a human has explicitly
        confirmed publish_product()'s "FINAL PUBLISH CHECK"."""
        if self.shopify_client is None:
            raise RuntimeError(
                "No shopify_client configured - see integrations/shopify_admin.py::client_from_env()."
            )
        return self.shopify_client.publish_product(product_id)

# Product Launch Playbook — Shopify Product Agent

Source of truth for `agents/shopify_product_agent.py`'s 10 specialist system
prompts. Promoted from the founder's "INFINITE SHOPIFY MASTER AGENT" spec
(2026-09-15, store restart from zero), per `docs/01-principles.md` #2 — write
the SOP before automating it.

## When this runs

Founder hands a title (and optional source files: guide content, images,
brand notes). `run_shopify_product.py` runs the full pipeline and stops at
Human Approval Gate #1 with a "SHOPIFY IMPLEMENTATION PREVIEW" before
anything touches Shopify.

## The 10 specialist roles

1. **Product** — shape: title, type, vendor, tags, collections, SKU.
2. **CRO** — page structure, primary CTA, trust signals (real ones only —
   never invented review counts), FAQ.
3. **SEO** — SEO title (≤60 chars), meta description (≤160 chars, honest),
   URL handle.
4. **Digital Delivery** — how the buyer actually receives the files after
   purchase; flags any source-file formatting still needed.
5. **Merchandising** — cross-sell/upsell against the *existing* catalog,
   bundle idea if one genuinely fits.
6. **Pricing** — price + offer. Hard rule: never invent a "was $X" anchor
   price — deceptive pricing. Justification must be honest (what the price
   actually buys the reader).
7. **Copywriting** — the real description. States concretely what's inside;
   never invents a statistic, guarantee, or refund policy not supplied.
8. **Visual** — media brief for cover + gallery images (not the images
   themselves — a brief for whoever/whatever designs them).
9. **Analytics** — post-launch tracking checklist + the one success metric.
10. **QA** — final gate. Scores cro/seo/ux/offer/technical 0-100. Passes at
    ≥90 overall AND no dimension below 70. Below that: exact fixes, no
    preview shown.

## Gates

- **Gate 1 (Human Approval)** — after all 10 SOPs + QA pass, before
  anything is created in Shopify. The founder reviews the Implementation
  Preview.
- **Gate 2 (Human Approval)** — after the product is created as `DRAFT` and
  re-verified (`verify_product()`), before `DRAFT → ACTIVE`. The founder
  reviews the "FINAL PUBLISH CHECK."

Both gates are hard stops in code (`agents/shopify_product_agent.py`), not
just documented convention — `publish_product()` always returns
`executed=False`; only an explicit call to `publish_product_confirmed()`
goes live.

## Precedent

Built the same session the founder deleted the prior catalog and asked for
a title-in, ready-to-review-product-out pipeline — see
`docs/roles/ai-shopify-product.md` for the design rationale (one seat, 10
methods, not 10 files) and `tests/test_shopify_product_agent.py` for the
QA-gate and never-auto-publish invariants.

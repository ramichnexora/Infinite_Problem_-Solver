# AI Shopify Product Agent

## Mandate

Turn an approved title (+ optional source files, + brand context) into a fully
specified, QA'd, human-approved Shopify product — from the founder's "INFINITE
SHOPIFY MASTER AGENT" spec, built for the store's from-zero relaunch
(2026-09-15).

Distinct from `digital_product` (2 SOPs: draft a spec, QA it). This seat runs
the founder's full 10-specialist pipeline and owns real Shopify execution
(DRAFT creation + a second, separate publish gate), not just a spec.

## Design note — one class, 10 methods, not 10 files

The founder's spec describes 10 separately-named sub-agents (Product, CRO,
SEO, Digital Delivery, Merchandising, Pricing, Copywriting, Visual,
Analytics, QA). This repo's existing convention — one `Agent` subclass per
seat, one `run_sop()` call per specialist step (see `marketing_agent.py`,
`digital_product_agent.py`) — is kept here: `ShopifyProductAgent` has 10 real
methods, each a separately-audited `run_sop()` call, so the audit trail shows
10 distinct specialist decisions without the un-scoped seat sprawl
`docs/01-principles.md` #8 warns against.

## SOPs (agents/shopify_product_agent.py)

1. `product(title, source_files, brand_context)` — title/type/vendor/tags/
   collections/SKU.
2. `cro(title, product_basics)` — page structure, primary CTA, trust
   signals, FAQ.
3. `seo(title, product_basics)` — SEO title, meta description, handle.
4. `digital_delivery(title, source_files)` — file plan, delivery method.
5. `merchandising(title, product_basics)` — cross-sell, upsell, bundle idea.
6. `pricing(title, product_basics, price_hint)` — price + honest offer.
   Never invents a "was $X" anchor price unless one is actually given.
7. `copywriting(title, product_basics, cro_output)` — the real product
   description. Never invents a statistic, guarantee, or refund policy.
8. `visual(title, product_basics)` — media brief for cover + gallery images.
9. `analytics(title, product_basics)` — post-launch tracking checklist +
   the one metric that defines success.
10. `qa(plan)` — scores the assembled plan 0-100 on cro/seo/ux/offer/
    technical. Gate: overall ≥90 AND no dimension below 70. Below the gate,
    stops and reports exactly what to fix — never proceeds.

## Orchestration

`build_product(title, source_files, brand_context)` runs all 10 SOPs in
sequence and always returns Tier 3 (**Human Approval Gate #1**) — matches
the spec's "never publish automatically." Below the QA gate, `executed` is
`False` and the output carries `fixes_needed` instead of a preview. At/above
the gate, the output includes a formatted "SHOPIFY IMPLEMENTATION PREVIEW."

## Execution (separate from the SOPs, only after Gate 1 approval)

- `create_shopify_draft(plan)` — calls `integrations/shopify_admin.py` to
  create the product, **always as `DRAFT`**, then immediately re-reads it
  (`verify_product()`) to confirm every approved field actually landed —
  the "SHOPIFY DEPLOYMENT REPORT."
- `publish_product(product_id)` — **Human Approval Gate #2**, a hard stop
  (`executed=False` always) presenting the "FINAL PUBLISH CHECK." Only
  `publish_product_confirmed(product_id)` actually flips `DRAFT → ACTIVE`,
  and that method is never called by anything in this repo automatically —
  a human (or the Claude Code session, on explicit instruction) calls it.

Requires `SHOPIFY_STORE_DOMAIN` and `SHOPIFY_ADMIN_ACCESS_TOKEN` (a Shopify
custom-app Admin API access token — never hardcoded, never committed). Same
credentials as `digital_product`'s Shopify integration; both seats share
`integrations/shopify_admin.py`.

## What this agent does NOT do

- No SOP, and no orchestration method, ever calls Shopify's Admin API to
  publish (`ACTIVE`) — that path only exists behind `publish_product_confirmed()`,
  which nothing in this repo invokes without an explicit, separate human
  approval matching Gate 2's "FINAL PUBLISH CHECK."
- Does not invent statistics, guarantees, refund policies, or "was $X"
  anchor prices not given to it — same standing rule as `digital_product`
  (see `ai-digital-product.md`'s Postpartum Sleep Handbook precedent).

## v2 — Never idle: fallback rule

Same as every other seat: if `agents/` cannot reach a model, the SOP is
written to `tasks/inbox/` as a hand-off and escalates to Tier 3
(`agents/handoff.py`, `docs/10-fallback-protocol.md`).

Strategic frame: `docs/EXECUTIVE_OPERATING_SYSTEM.md` — Bottleneck Rule
(§41), Billion-Dollar Filter (§46).

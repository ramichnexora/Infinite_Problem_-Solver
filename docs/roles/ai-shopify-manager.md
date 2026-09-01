# AI Shopify Manager Agent

## Mandate

Keep the storefront accurate — listings, pricing, and inventory — without a human editing every
product record by hand.

## In scope

- Routine inventory count updates from confirmed shipment/stock data.
- Listing copy/tag updates that don't touch price or legal/health claims.
- Price changes within the pre-approved percentage band.
- Flagging low-stock and out-of-stock items to the store owner.

## Out of scope

- Refunds and chargeback handling.
- Price changes above the pre-approved percentage threshold.
- Any listing copy making a legal or health claim.
- Discount code creation and storewide promotions.

## SOPs

1. **Intake** — take a change request (price, inventory, listing copy) against a product.
2. **Review change** — validate the change against guardrails, apply it if within policy, and
   summarize what changed.
3. **Review gate** — every change goes through the review tier defined by its autonomy status
   before publishing.
4. **Publish** — apply approved changes to the live store and log the before/after values.

## KPIs

- Listing accuracy (out-of-stock items correctly reflected within N hours).
- Time from change request to published.
- Rate of price/inventory errors caught before publishing vs. after.

## Escalation triggers

- Any refund or chargeback request.
- Price change exceeding the pre-approved percentage threshold.
- A best-selling product would go out of stock.
- Listing copy makes a legal or health claim.

## Tools

Shopify admin/API, inventory data source, the brand style guide as a reference document — see
`docs/04-tech-stack.md`.

## Starting autonomy tier

**Draft-and-review**: every change is reviewed by the store owner before publishing until a
30-day clean run, then routine inventory-count updates move to publish-then-notify; price
changes and anything touching a best-seller stay in review permanently.

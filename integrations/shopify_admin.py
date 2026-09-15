"""Shopify Admin GraphQL API integration for the digital_product seat.

Mirrors integrations/instagram.py's pattern: a thin wrapper doing the actual
network I/O, kept separate from the agent so tests never need a real token.

Credentials come from environment variables only - never hardcoded, never
committed:
  SHOPIFY_STORE_DOMAIN         - e.g. "your-store.myshopify.com"
  SHOPIFY_ADMIN_ACCESS_TOKEN   - a Shopify custom-app Admin API access token

Hard rule (see docs/roles/ai-digital-product.md): every product this creates
is DRAFT, never ACTIVE. Publishing a product to the live store is a separate,
explicit, founder-triggered action - this module intentionally has no
"publish" function, only create_product_draft() and update_price().
"""
from __future__ import annotations

import os
from typing import Any, Optional

import requests

API_VERSION = "2025-01"


class ShopifyAdminClient:
    """Thin wrapper around the subset of the Shopify Admin GraphQL API this integration needs."""

    def __init__(self, store_domain: str, access_token: str, session: Optional[requests.Session] = None):
        self._url = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
        self._token = access_token
        self._session = session or requests.Session()

    def _graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        response = self._session.post(
            self._url,
            json={"query": query, "variables": variables},
            headers={"X-Shopify-Access-Token": self._token, "Content-Type": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        body = response.json()
        if "errors" in body:
            raise RuntimeError(f"Shopify GraphQL error: {body['errors']}")
        return body["data"]

    def create_product_draft(self, spec: dict[str, Any]) -> dict[str, Any]:
        """Create a new Shopify product, always as DRAFT. `spec` must have
        title, description_html, price_usd; may have product_type, tags.
        Returns {"product_id": ..., "variant_id": ..., "status": "DRAFT"}."""
        data = self._graphql(
            """
            mutation CreateProduct($input: ProductInput!) {
              productCreate(input: $input) {
                product { id title status variants(first: 1) { edges { node { id } } } }
                userErrors { field message }
              }
            }
            """,
            {
                "input": {
                    "title": spec["title"],
                    "descriptionHtml": spec.get("description_html", ""),
                    "productType": spec.get("product_type", "Digital Guide"),
                    "tags": spec.get("tags", []),
                    "status": "DRAFT",
                }
            },
        )
        result = data["productCreate"]
        if result["userErrors"]:
            raise RuntimeError(f"Shopify productCreate errors: {result['userErrors']}")
        product = result["product"]
        variant_id = product["variants"]["edges"][0]["node"]["id"]

        price = spec.get("price_usd")
        if price is not None:
            self.update_price(variant_id, price)

        return {"product_id": product["id"], "variant_id": variant_id, "status": product["status"]}

    def update_price(self, variant_id: str, price_usd: float) -> dict[str, Any]:
        product_id = None  # productVariantsBulkUpdate needs the parent product id
        data = self._graphql(
            """
            query GetProductIdForVariant($id: ID!) {
              productVariant(id: $id) { product { id } }
            }
            """,
            {"id": variant_id},
        )
        product_id = data["productVariant"]["product"]["id"]

        data = self._graphql(
            """
            mutation UpdatePrice($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
              productVariantsBulkUpdate(productId: $productId, variants: $variants) {
                productVariants { id price }
                userErrors { field message }
              }
            }
            """,
            {"productId": product_id, "variants": [{"id": variant_id, "price": f"{price_usd:.2f}"}]},
        )
        result = data["productVariantsBulkUpdate"]
        if result["userErrors"]:
            raise RuntimeError(f"Shopify price update errors: {result['userErrors']}")
        return result["productVariants"][0]

    def verify_product(self, product_id: str, expected: dict[str, Any]) -> dict[str, Any]:
        """Re-read a created product and confirm the fields that were meant to land actually
        did - the shopify_product seat's post-execution QA step, before the "SHOPIFY
        DEPLOYMENT REPORT" is shown to a human. Never mutates anything."""
        data = self._graphql(
            """
            query VerifyProduct($id: ID!) {
              product(id: $id) {
                id title descriptionHtml productType status tags handle
                variants(first: 1) { edges { node { id price } } }
              }
            }
            """,
            {"id": product_id},
        )
        product = data["product"]
        if product is None:
            raise RuntimeError(f"Shopify product {product_id} not found during verification")

        mismatches: list[str] = []
        if expected.get("title") and product["title"] != expected["title"]:
            mismatches.append(f"title: expected {expected['title']!r}, got {product['title']!r}")
        if expected.get("price_usd") is not None:
            variant_price = product["variants"]["edges"][0]["node"]["price"] if product["variants"]["edges"] else None
            if variant_price is not None and float(variant_price) != float(expected["price_usd"]):
                mismatches.append(f"price: expected {expected['price_usd']}, got {variant_price}")
        if product["status"] != "DRAFT":
            mismatches.append(f"status: expected DRAFT, got {product['status']!r}")

        return {"product": product, "mismatches": mismatches, "verified": not mismatches}

    def publish_product(self, product_id: str) -> dict[str, Any]:
        """Flip a product DRAFT -> ACTIVE. Only ever called after an explicit human
        approval (ShopifyProductAgent.publish_product_confirmed()) - never automatically."""
        data = self._graphql(
            """
            mutation PublishProduct($id: ID!, $input: ProductUpdateInput!) {
              productUpdate(product: $input) {
                product { id status }
                userErrors { field message }
              }
            }
            """,
            {"id": product_id, "input": {"id": product_id, "status": "ACTIVE"}},
        )
        result = data["productUpdate"]
        if result["userErrors"]:
            raise RuntimeError(f"Shopify publish errors: {result['userErrors']}")
        return {"product_id": result["product"]["id"], "status": result["product"]["status"]}


def client_from_env() -> ShopifyAdminClient:
    """Build a client from SHOPIFY_STORE_DOMAIN / SHOPIFY_ADMIN_ACCESS_TOKEN.
    Raises a clear error (not a crash deep in a network call) if either is missing."""
    domain = os.environ.get("SHOPIFY_STORE_DOMAIN")
    token = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
    if not domain or not token:
        raise RuntimeError(
            "SHOPIFY_STORE_DOMAIN and SHOPIFY_ADMIN_ACCESS_TOKEN must both be set to create "
            "Shopify products - see docs/roles/ai-digital-product.md."
        )
    return ShopifyAdminClient(domain, token)

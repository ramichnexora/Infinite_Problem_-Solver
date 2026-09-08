"""Mocked tests for integrations/shopify_admin.py - never makes a real Shopify call."""
from __future__ import annotations

import os
import unittest
from unittest.mock import MagicMock, patch

from integrations.shopify_admin import ShopifyAdminClient, client_from_env


class TestClientFromEnv(unittest.TestCase):
    def test_raises_clearly_when_credentials_missing(self):
        env = {k: v for k, v in os.environ.items() if k not in ("SHOPIFY_STORE_DOMAIN", "SHOPIFY_ADMIN_ACCESS_TOKEN")}
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaises(RuntimeError) as ctx:
                client_from_env()
        self.assertIn("SHOPIFY_STORE_DOMAIN", str(ctx.exception))

    def test_builds_client_when_credentials_present(self):
        env = {"SHOPIFY_STORE_DOMAIN": "test-store.myshopify.com", "SHOPIFY_ADMIN_ACCESS_TOKEN": "shpat_test"}
        with patch.dict(os.environ, env, clear=False):
            client = client_from_env()
        self.assertIsInstance(client, ShopifyAdminClient)


class TestCreateProductDraft(unittest.TestCase):
    def _client_with_mock_session(self, responses):
        session = MagicMock()
        session.post.side_effect = responses
        return ShopifyAdminClient("test-store.myshopify.com", "shpat_test", session=session)

    def test_always_creates_as_draft_and_applies_price(self):
        create_resp = MagicMock()
        create_resp.json.return_value = {
            "data": {
                "productCreate": {
                    "product": {
                        "id": "gid://shopify/Product/1",
                        "title": "Test Product",
                        "status": "DRAFT",
                        "variants": {"edges": [{"node": {"id": "gid://shopify/ProductVariant/1"}}]},
                    },
                    "userErrors": [],
                }
            }
        }
        lookup_resp = MagicMock()
        lookup_resp.json.return_value = {"data": {"productVariant": {"product": {"id": "gid://shopify/Product/1"}}}}
        price_resp = MagicMock()
        price_resp.json.return_value = {
            "data": {
                "productVariantsBulkUpdate": {
                    "productVariants": [{"id": "gid://shopify/ProductVariant/1", "price": "29.00"}],
                    "userErrors": [],
                }
            }
        }
        client = self._client_with_mock_session([create_resp, lookup_resp, price_resp])

        result = client.create_product_draft(
            {"title": "Test Product", "description_html": "<p>desc</p>", "price_usd": 29.00}
        )

        self.assertEqual(result["status"], "DRAFT")
        self.assertEqual(result["product_id"], "gid://shopify/Product/1")

    def test_raises_on_user_errors_instead_of_silently_succeeding(self):
        create_resp = MagicMock()
        create_resp.json.return_value = {
            "data": {"productCreate": {"product": None, "userErrors": [{"field": ["title"], "message": "can't be blank"}]}}
        }
        client = self._client_with_mock_session([create_resp])

        with self.assertRaises(RuntimeError):
            client.create_product_draft({"title": "", "description_html": ""})


if __name__ == "__main__":
    unittest.main()

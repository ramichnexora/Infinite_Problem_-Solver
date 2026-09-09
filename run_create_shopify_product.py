#!/usr/bin/env python3
"""Create a DRAFT Shopify product from an already-approved spec JSON file.

This is a manual, founder-triggered step - NOT called automatically by
DigitalProductAgent.draft_product_spec() or qa_check(). Those two SOPs only
produce/score a spec; turning an approved spec into a real Shopify product is
a separate, explicit action, per docs/roles/ai-digital-product.md and the
standing outbound-action rule in docs/roles/human-founder.md.

The created product is always DRAFT - never live/ACTIVE. Publishing it is a
separate manual step in Shopify admin (or a future publish_product() once
that gate is explicitly designed).

Usage:
    python run_create_shopify_product.py path/to/approved-spec.json

Spec JSON shape (matches DigitalProductAgent.draft_product_spec output):
{
  "title": "...",
  "description_html": "...",
  "price_usd": 29.00,
  "product_type": "Digital Guide",
  "tags": ["..."]
}

Requires:
    SHOPIFY_STORE_DOMAIN, SHOPIFY_ADMIN_ACCESS_TOKEN - see integrations/shopify_admin.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from integrations.shopify_admin import client_from_env


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python run_create_shopify_product.py path/to/approved-spec.json", file=sys.stderr)
        return 1

    spec_path = Path(sys.argv[1])
    if not spec_path.exists():
        print(f"Spec file not found: {spec_path}", file=sys.stderr)
        return 1

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    for required in ("title", "description_html", "price_usd"):
        if required not in spec:
            print(f"Spec is missing required field: {required}", file=sys.stderr)
            return 1

    try:
        client = client_from_env()
    except RuntimeError as exc:
        print(f"Cannot start: {exc}", file=sys.stderr)
        return 1

    print(f"[*] Creating DRAFT product: {spec['title']}")
    result = client.create_product_draft(spec)
    print(f"[+] Created: {result['product_id']} (status={result['status']}, price=${spec['price_usd']:.2f})")
    print("[!] Product is DRAFT - review in Shopify admin, then publish manually when ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

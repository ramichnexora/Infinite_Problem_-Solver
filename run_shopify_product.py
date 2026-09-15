#!/usr/bin/env python3
"""Run the Shopify Product Agent pipeline - see
playbooks/shopify-ai-os/product-launch.md and docs/roles/ai-shopify-product.md.

Takes a title (+ optional source file paths), runs the 10-specialist
pipeline through build_product(), and stops for explicit human approval
(writes a tasks/ review task, same pattern as run_daily_social_post.py) -
this script never creates or publishes a Shopify product by itself.

Once the founder approves the printed "SHOPIFY IMPLEMENTATION PREVIEW":
    python run_shopify_product.py --create-draft path/to/approved-plan.json
creates the DRAFT product and prints the "SHOPIFY DEPLOYMENT REPORT."

Publishing (DRAFT -> ACTIVE) is Gate 2 and is never scripted here on
purpose - it requires a second, separate, explicit approval. See
ShopifyProductAgent.publish_product_confirmed().

Requires:
    ANTHROPIC_API_KEY                              - see docs/07-running-the-agents.md
    SHOPIFY_STORE_DOMAIN, SHOPIFY_ADMIN_ACCESS_TOKEN  - only for --create-draft

Usage:
    python run_shopify_product.py "The Product Title" [--source-file path]... [--brand-context "..."]
    python run_shopify_product.py --create-draft path/to/approved-plan.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date as date_cls
from pathlib import Path

from agents.llm import build_llm_client
from agents.shopify_product_agent import ShopifyProductAgent

ROOT = Path(__file__).parent
TASKS_DIR = ROOT / "tasks"


def next_task_id() -> str:
    existing = sorted(TASKS_DIR.glob("task-*.md"))
    numbers = [int(m.group(1)) for p in existing if (m := re.match(r"task-(\d+)-", p.name))]
    return f"{(max(numbers) + 1) if numbers else 1:04d}"


def _slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]


def write_review_task(*, title: str, build_output: dict, today: str) -> Path:
    task_id = next_task_id()
    slug = f"product-{_slugify(title)}"
    path = TASKS_DIR / f"task-{task_id}-{slug}.md"
    plan_path = TASKS_DIR / f"task-{task_id}-{slug}.plan.json"
    plan_path.write_text(json.dumps(build_output.get("plan", {}), indent=2), encoding="utf-8")

    gate_passed = build_output.get("gate_passed", False)
    preview = build_output.get("preview") or "(QA gate not met - see qa.fixes_needed below)"
    qa = build_output.get("qa", {})

    path.write_text(
        f"""---
id: task-{task_id}-{slug}
project: null
seat: shopify_product
status: review
tier: 3
priority: medium
created: {today}
updated: {today}
---

## Description
New Shopify product build for "{title}", Human Approval Gate #1
(playbooks/shopify-ai-os/product-launch.md). QA gate passed: {gate_passed}.

## Definition of Done
Founder reviews the preview below. If approved, run:
    python run_shopify_product.py --create-draft {plan_path.relative_to(ROOT)}
This creates the product as DRAFT only - publishing is a separate, later
Gate 2 approval (ShopifyProductAgent.publish_product / publish_product_confirmed).

## Preview
{preview}

## QA scores
{qa.get('scores', {})}
Overall: {qa.get('overall')}
Fixes needed: {qa.get('fixes_needed', [])}

## Notes
Full plan saved to {plan_path.name} (not committed - review artifact only).
""",
        encoding="utf-8",
    )
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("title", nargs="?", help="Approved product title")
    parser.add_argument("--source-file", action="append", default=[], help="Path to a source file (repeatable)")
    parser.add_argument("--brand-context", default="", help="Free-text brand context")
    parser.add_argument("--create-draft", metavar="PLAN_JSON", help="Create the Shopify DRAFT from an approved plan JSON file")
    args = parser.parse_args()

    agent_kwargs = {}
    if args.create_draft:
        from integrations.shopify_admin import client_from_env

        try:
            agent_kwargs["shopify_client"] = client_from_env()
        except RuntimeError as exc:
            print(f"Cannot create draft: {exc}", file=sys.stderr)
            return 1

        agent = ShopifyProductAgent(build_llm_client(), **agent_kwargs)
        plan = json.loads(Path(args.create_draft).read_text(encoding="utf-8"))
        report = agent.create_shopify_draft(plan)
        print("SHOPIFY DEPLOYMENT REPORT")
        print(json.dumps(report, indent=2))
        if report["verification"]["mismatches"]:
            print("WARNING - verification mismatches:", report["verification"]["mismatches"], file=sys.stderr)
        return 0

    if not args.title:
        parser.error("title is required unless --create-draft is used")

    today = date_cls.today().isoformat()
    agent = ShopifyProductAgent(build_llm_client())

    result = agent.build_product(args.title, args.source_file or None, args.brand_context)
    task_path = write_review_task(title=args.title, build_output=result.output, today=today)
    print(f"Queued for review: {task_path}")
    if not result.executed:
        print(f"Note: {result.escalation_reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

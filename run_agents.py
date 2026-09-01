#!/usr/bin/env python3
"""CLI to run the AI Company OS agents against the sample data in data/.

Usage:
    python run_agents.py support     # triage + resolve data/tickets.sample.json
    python run_agents.py sales       # qualify data/leads.sample.json
    python run_agents.py research    # cluster data/signal.sample.json
    python run_agents.py marketing   # draft data/content_briefs.sample.json
    python run_agents.py operations  # assess data/workflows.sample.json
    python run_agents.py finance     # categorize data/transactions.sample.json
    python run_agents.py hr          # screen data/candidates.sample.json
    python run_agents.py developer   # triage data/dev_tickets.sample.json
    python run_agents.py designer    # draft_concept data/design_briefs.sample.json
    python run_agents.py shopify     # review_change data/shopify_requests.sample.json
    python run_agents.py social      # draft_post data/social_slots.sample.json
    python run_agents.py all         # run everything

Requires ANTHROPIC_API_KEY to be set - see docs/07-running-the-agents.md.
Every run appends to logs/audit.jsonl and, for anything escalated,
logs/escalations.jsonl.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agents.designer_agent import DesignerAgent
from agents.developer_agent import DeveloperAgent
from agents.finance_agent import FinanceAgent
from agents.hr_recruiting_agent import HRRecruitingAgent
from agents.llm import AnthropicLLMClient
from agents.marketing_agent import MarketingAgent
from agents.operations_agent import OperationsAgent
from agents.product_research_agent import ProductResearchAgent
from agents.sales_agent import SalesAgent
from agents.shopify_manager_agent import ShopifyManagerAgent
from agents.social_media_agent import SocialMediaAgent
from agents.support_agent import SupportAgent

DATA_DIR = Path(__file__).parent / "data"


def _load(name: str):
    with (DATA_DIR / name).open(encoding="utf-8") as f:
        return json.load(f)


def _print_result(label: str, result) -> None:
    status = "EXECUTED" if result.executed else f"ESCALATED (tier {int(result.tier)})"
    print(f"\n[{label}] {status}")
    print(json.dumps(result.output, indent=2))


def run_support(llm) -> None:
    kb = (DATA_DIR / "knowledge_base.md").read_text(encoding="utf-8")
    agent = SupportAgent(llm, knowledge_base=kb)
    for ticket in _load("tickets.sample.json"):
        triage = agent.triage(ticket)
        _print_result(f"support/triage {ticket['id']}", triage)
        resolve = agent.resolve(ticket)
        _print_result(f"support/resolve {ticket['id']}", resolve)


def run_sales(llm) -> None:
    agent = SalesAgent(llm)
    for lead in _load("leads.sample.json"):
        result = agent.qualify(lead)
        _print_result(f"sales/qualify {lead['id']}", result)


def run_research(llm) -> None:
    agent = ProductResearchAgent(llm)
    signal_items = _load("signal.sample.json")
    result = agent.cluster_signal(signal_items)
    _print_result("research/cluster_signal", result)


def run_marketing(llm) -> None:
    agent = MarketingAgent(llm, competitor_names=["CompetitorX"])
    for brief in _load("content_briefs.sample.json"):
        result = agent.draft(brief)
        _print_result(f"marketing/draft {brief['id']}", result)


def run_operations(llm) -> None:
    agent = OperationsAgent(llm)
    for workflow in _load("workflows.sample.json"):
        result = agent.assess_workflow(workflow)
        _print_result(f"operations/assess_workflow {workflow['id']}", result)


def run_finance(llm) -> None:
    agent = FinanceAgent(llm)
    for transaction in _load("transactions.sample.json"):
        result = agent.categorize_transaction(transaction)
        _print_result(f"finance/categorize_transaction {transaction['id']}", result)


def run_hr(llm) -> None:
    agent = HRRecruitingAgent(llm)
    for candidate in _load("candidates.sample.json"):
        result = agent.screen(candidate)
        _print_result(f"hr/screen {candidate['id']}", result)


def run_developer(llm) -> None:
    agent = DeveloperAgent(llm)
    for ticket in _load("dev_tickets.sample.json"):
        result = agent.triage(ticket)
        _print_result(f"developer/triage {ticket['id']}", result)


def run_designer(llm) -> None:
    agent = DesignerAgent(llm)
    for brief in _load("design_briefs.sample.json"):
        result = agent.draft_concept(brief)
        _print_result(f"designer/draft_concept {brief['id']}", result)


def run_shopify(llm) -> None:
    agent = ShopifyManagerAgent(llm)
    for request in _load("shopify_requests.sample.json"):
        result = agent.review_change(request)
        _print_result(f"shopify/review_change {request['id']}", result)


def run_social(llm) -> None:
    agent = SocialMediaAgent(llm, competitor_names=["CompetitorX"])
    for slot in _load("social_slots.sample.json"):
        result = agent.draft_post(slot)
        _print_result(f"social/draft_post {slot['id']}", result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "agent",
        choices=[
            "support",
            "sales",
            "research",
            "marketing",
            "operations",
            "finance",
            "hr",
            "developer",
            "designer",
            "shopify",
            "social",
            "all",
        ],
    )
    args = parser.parse_args()

    llm = AnthropicLLMClient()

    if args.agent in ("support", "all"):
        run_support(llm)
    if args.agent in ("sales", "all"):
        run_sales(llm)
    if args.agent in ("research", "all"):
        run_research(llm)
    if args.agent in ("marketing", "all"):
        run_marketing(llm)
    if args.agent in ("operations", "all"):
        run_operations(llm)
    if args.agent in ("finance", "all"):
        run_finance(llm)
    if args.agent in ("hr", "all"):
        run_hr(llm)
    if args.agent in ("developer", "all"):
        run_developer(llm)
    if args.agent in ("designer", "all"):
        run_designer(llm)
    if args.agent in ("shopify", "all"):
        run_shopify(llm)
    if args.agent in ("social", "all"):
        run_social(llm)

    print("\nAudit log: logs/audit.jsonl")
    print("Escalation queue: logs/escalations.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())

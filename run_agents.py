#!/usr/bin/env python3
"""CLI to run the AI Company OS agents against the sample data in data/.

Usage:
    python run_agents.py support     # triage + resolve data/tickets.sample.json
    python run_agents.py sales       # qualify data/leads.sample.json
    python run_agents.py research    # cluster data/signal.sample.json
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

from agents.llm import AnthropicLLMClient
from agents.product_research_agent import ProductResearchAgent
from agents.sales_agent import SalesAgent
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agent", choices=["support", "sales", "research", "all"])
    args = parser.parse_args()

    llm = AnthropicLLMClient()

    if args.agent in ("support", "all"):
        run_support(llm)
    if args.agent in ("sales", "all"):
        run_sales(llm)
    if args.agent in ("research", "all"):
        run_research(llm)

    print("\nAudit log: logs/audit.jsonl")
    print("Escalation queue: logs/escalations.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())

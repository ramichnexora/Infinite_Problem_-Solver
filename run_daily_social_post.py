#!/usr/bin/env python3
"""Run the daily social posting automation - see automation/daily-social-post.yaml
and playbooks/shopify-ai-os/marketing.md prompt #5.

For each configured channel: Plan -> Draft -> Publish. At Tier 3 (the
default for every channel today, per docs/06-implementation-roadmap.md
Phase 1), Publish stops short of actually posting and this script writes a
review task to tasks/ instead - approve it by hand, then re-run with that
channel promoted in automation/daily-social-post.yaml's tier_override once
you're ready.

Requires:
    ANTHROPIC_API_KEY       - see docs/07-running-the-agents.md
    IG_ACCESS_TOKEN, IG_BUSINESS_ACCOUNT_ID   - only if instagram is promoted past Tier 3
    FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID          - only if facebook is promoted past Tier 3

Usage:
    python run_daily_social_post.py [--date YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date as date_cls
from pathlib import Path
from typing import Any

import yaml

from agents.escalation import Tier
from agents.llm import AnthropicLLMClient
from agents.marketing_agent import MarketingAgent

ROOT = Path(__file__).parent
AUTOMATION_CONFIG = ROOT / "automation" / "daily-social-post.yaml"
TASKS_DIR = ROOT / "tasks"

_TIER_BY_INT = {1: Tier.AUTONOMOUS, 2: Tier.NOTIFY, 3: Tier.HUMAN_APPROVAL}


def load_config() -> dict[str, Any]:
    with AUTOMATION_CONFIG.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_channel_publishers(config: dict[str, Any]) -> dict[str, Any]:
    """Only build a live client for a channel actually promoted past Tier 3 -
    this avoids raising on a missing env var for a channel nobody asked to
    auto-publish to yet (including tiktok, which is never promotable today)."""
    tier_override = config.get("tier_override", {})
    publishers: dict[str, Any] = {}

    if _TIER_BY_INT.get(tier_override.get("instagram", 3)) != Tier.HUMAN_APPROVAL:
        from integrations.instagram import client_from_env as ig_client

        client = ig_client()
        publishers["instagram"] = client.publish

    if _TIER_BY_INT.get(tier_override.get("facebook", 3)) != Tier.HUMAN_APPROVAL:
        from integrations.facebook import client_from_env as fb_client

        client = fb_client()
        publishers["facebook"] = client.publish

    # tiktok intentionally never added - see integrations/tiktok.py
    return publishers


def next_task_id() -> str:
    existing = sorted(TASKS_DIR.glob("task-*.md"))
    numbers = [int(m.group(1)) for p in existing if (m := re.match(r"task-(\d+)-", p.name))]
    return f"{(max(numbers) + 1) if numbers else 1:04d}"


def write_review_task(*, channel: str, brief: dict[str, Any], draft_output: dict[str, Any], reason: str, today: str) -> Path:
    task_id = next_task_id()
    slug = f"social-post-{channel}-{today}"
    path = TASKS_DIR / f"task-{task_id}-{slug}.md"
    path.write_text(
        f"""---
id: task-{task_id}-{slug}
project: null
seat: marketing
status: review
tier: 3
priority: medium
created: {today}
updated: {today}
---

## Description
Daily social post for {channel} on {today}, awaiting human approval before
publish (channel is in draft-and-review per automation/daily-social-post.yaml).

## Definition of Done
Per playbooks/shopify-ai-os/marketing.md: post reads like a real person,
references something specific, every claim grounded - no invented stats.

## Draft
Topic: {brief.get('topic', '')}
Audience: {brief.get('audience', '')}

{draft_output.get('draft', '')}

Hook: {draft_output.get('hook', '')}
CTA: {draft_output.get('cta', '')}

## Notes
Held for review: {reason}
""",
        encoding="utf-8",
    )
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None, help="Defaults to today (UTC).")
    args = parser.parse_args()
    today = args.date or date_cls.today().isoformat()

    config = load_config()
    channels: list[str] = config.get("channels", [])
    tier_override_raw = config.get("tier_override", {})
    tier_override = {ch: _TIER_BY_INT[tier_override_raw[ch]] for ch in tier_override_raw}

    try:
        channel_publishers = build_channel_publishers(config)
    except RuntimeError as exc:
        print(f"Cannot start: {exc}", file=sys.stderr)
        return 1

    agent = MarketingAgent(
        AnthropicLLMClient(),
        channel_publishers=channel_publishers,
        tier_override=tier_override,
    )

    for channel in channels:
        plan_result = agent.plan_daily_content(today)
        if not plan_result.executed:
            print(f"[{channel}] plan escalated: {plan_result.escalation_reason}")
            continue

        brief = dict(plan_result.output)
        brief["channel"] = channel
        draft_result = agent.draft(brief)
        if not draft_result.executed:
            print(f"[{channel}] draft escalated: {draft_result.escalation_reason}")
            continue

        publish_result = agent.publish(draft_result.output, channel)
        if publish_result.executed:
            print(f"[{channel}] published: {publish_result.output}")
        else:
            task_path = write_review_task(
                channel=channel,
                brief=brief,
                draft_output=draft_result.output,
                reason=publish_result.escalation_reason or "escalated",
                today=today,
            )
            print(f"[{channel}] queued for review: {task_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

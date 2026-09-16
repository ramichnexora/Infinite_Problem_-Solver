"""TikTok publishing integration - not yet implemented.

TikTok's Content Posting API requires an app-review process (days to weeks)
before a developer app can publish on a creator's behalf. There is no
TikTok entry in config/agents.yaml's channel_publishers wiring yet, so
MarketingAgent.publish() already routes "tiktok" to Tier 3 (human
sign-off) with a clear reason - this stub exists so that changes elsewhere
in the codebase, or a future direct call, fail loudly instead of silently
no-op'ing if someone wires this in before it's real.

See automation/README.md and playbooks/shopify-ai-os/marketing.md.
"""
from __future__ import annotations

from typing import Any


def client_from_env():
    raise NotImplementedError(
        "TikTok integration is pending the Content Posting API app-review process - "
        "see automation/README.md. Do not register 'tiktok' in a MarketingAgent's "
        "channel_publishers until this is real; it will keep routing to Tier 3 "
        "(human sign-off) either way."
    )


def publish(post: dict[str, Any]) -> dict[str, Any]:
    raise NotImplementedError(
        "TikTok integration is pending the Content Posting API app-review process - "
        "see automation/README.md."
    )

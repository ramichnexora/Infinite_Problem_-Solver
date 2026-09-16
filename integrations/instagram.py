"""Instagram Graph API publishing integration.

Mirrors integrations/telegram_bot.py's pattern: a thin wrapper that calls the
agent's SOP method (MarketingAgent.publish) and does the actual network I/O,
kept separate from the agent so tests never need a real token.

Credentials come from environment variables only - never hardcoded, never
committed (see docs/04-tech-stack.md, Marketing row):
  IG_ACCESS_TOKEN         - a long-lived Instagram Graph API access token
  IG_BUSINESS_ACCOUNT_ID  - the connected Instagram Business Account id

Publishing a photo/reel via the Graph API is two calls: create a media
container, then publish it. See:
https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/content-publishing
"""
from __future__ import annotations

import os
from typing import Any, Optional

import requests

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


class InstagramClient:
    """Thin wrapper around the subset of the Instagram Graph API this integration needs."""

    def __init__(
        self,
        access_token: str,
        business_account_id: str,
        session: Optional[requests.Session] = None,
    ):
        self._token = access_token
        self._account_id = business_account_id
        self._session = session or requests.Session()

    def publish(self, post: dict[str, Any]) -> dict[str, Any]:
        """post must have `image_url` (Instagram requires a publicly reachable
        image URL for the container step) and `caption`. Returns {"post_id": ...}."""
        container = self._session.post(
            f"{GRAPH_API_BASE}/{self._account_id}/media",
            data={
                "image_url": post["image_url"],
                "caption": post.get("caption", ""),
                "access_token": self._token,
            },
            timeout=30,
        )
        container.raise_for_status()
        creation_id = container.json()["id"]

        publish = self._session.post(
            f"{GRAPH_API_BASE}/{self._account_id}/media_publish",
            data={"creation_id": creation_id, "access_token": self._token},
            timeout=30,
        )
        publish.raise_for_status()
        return {"post_id": publish.json()["id"]}


def client_from_env() -> InstagramClient:
    """Build a client from IG_ACCESS_TOKEN / IG_BUSINESS_ACCOUNT_ID. Raises a
    clear error (not a crash deep in a network call) if either is missing."""
    token = os.environ.get("IG_ACCESS_TOKEN")
    account_id = os.environ.get("IG_BUSINESS_ACCOUNT_ID")
    if not token or not account_id:
        raise RuntimeError(
            "IG_ACCESS_TOKEN and IG_BUSINESS_ACCOUNT_ID must both be set to publish "
            "to Instagram - see docs/04-tech-stack.md."
        )
    return InstagramClient(token, account_id)

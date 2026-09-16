"""Facebook Graph API publishing integration.

Same pattern as integrations/instagram.py - thin wrapper, no agent logic here.

Credentials come from environment variables only (docs/04-tech-stack.md):
  FB_PAGE_ACCESS_TOKEN - a Page access token with pages_manage_posts scope
  FB_PAGE_ID           - the Facebook Page id to post to
"""
from __future__ import annotations

import os
from typing import Any, Optional

import requests

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


class FacebookClient:
    """Thin wrapper around the subset of the Facebook Graph API this integration needs."""

    def __init__(
        self,
        page_access_token: str,
        page_id: str,
        session: Optional[requests.Session] = None,
    ):
        self._token = page_access_token
        self._page_id = page_id
        self._session = session or requests.Session()

    def publish(self, post: dict[str, Any]) -> dict[str, Any]:
        """post must have `message` (text) and may have `image_url` (posts a
        photo instead of a text-only feed item). Returns {"post_id": ...}."""
        if post.get("image_url"):
            endpoint = f"{GRAPH_API_BASE}/{self._page_id}/photos"
            data = {
                "url": post["image_url"],
                "caption": post.get("message", ""),
                "access_token": self._token,
            }
        else:
            endpoint = f"{GRAPH_API_BASE}/{self._page_id}/feed"
            data = {"message": post.get("message", ""), "access_token": self._token}

        response = self._session.post(endpoint, data=data, timeout=30)
        response.raise_for_status()
        return {"post_id": response.json()["id"]}


def client_from_env() -> FacebookClient:
    token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    page_id = os.environ.get("FB_PAGE_ID")
    if not token or not page_id:
        raise RuntimeError(
            "FB_PAGE_ACCESS_TOKEN and FB_PAGE_ID must both be set to publish to "
            "Facebook - see docs/04-tech-stack.md."
        )
    return FacebookClient(token, page_id)

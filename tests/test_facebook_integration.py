from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from integrations.facebook import FacebookClient, client_from_env


def test_publish_text_only_posts_to_feed():
    client = FacebookClient("token-123", "page-1")
    response = Mock(json=Mock(return_value={"id": "feed-post-1"}))
    response.raise_for_status = Mock()

    with patch.object(client._session, "post", return_value=response) as mock_post:
        result = client.publish({"message": "hello world"})

    assert result == {"post_id": "feed-post-1"}
    endpoint = mock_post.call_args.args[0]
    assert endpoint.endswith("/page-1/feed")


def test_publish_with_image_posts_to_photos():
    client = FacebookClient("token-123", "page-1")
    response = Mock(json=Mock(return_value={"id": "photo-post-1"}))
    response.raise_for_status = Mock()

    with patch.object(client._session, "post", return_value=response) as mock_post:
        result = client.publish({"message": "caption", "image_url": "https://example.com/a.jpg"})

    assert result == {"post_id": "photo-post-1"}
    endpoint = mock_post.call_args.args[0]
    assert endpoint.endswith("/page-1/photos")


def test_client_from_env_requires_both_vars(monkeypatch):
    monkeypatch.delenv("FB_PAGE_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("FB_PAGE_ID", raising=False)

    with pytest.raises(RuntimeError, match="FB_PAGE_ACCESS_TOKEN"):
        client_from_env()

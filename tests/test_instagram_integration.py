from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from integrations.instagram import InstagramClient, client_from_env


def test_publish_creates_container_then_publishes():
    client = InstagramClient("token-123", "ig-account-1")
    container_response = Mock(json=Mock(return_value={"id": "creation-1"}))
    container_response.raise_for_status = Mock()
    publish_response = Mock(json=Mock(return_value={"id": "media-1"}))
    publish_response.raise_for_status = Mock()

    with patch.object(client._session, "post", side_effect=[container_response, publish_response]) as mock_post:
        result = client.publish({"image_url": "https://example.com/a.jpg", "caption": "hello"})

    assert result == {"post_id": "media-1"}
    assert mock_post.call_count == 2
    first_call, second_call = mock_post.call_args_list
    assert "media" in first_call.args[0]
    assert "media_publish" in second_call.args[0]
    assert second_call.kwargs["data"]["creation_id"] == "creation-1"


def test_client_from_env_requires_both_vars(monkeypatch):
    monkeypatch.delenv("IG_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("IG_BUSINESS_ACCOUNT_ID", raising=False)

    with pytest.raises(RuntimeError, match="IG_ACCESS_TOKEN"):
        client_from_env()


def test_client_from_env_builds_client_when_both_set(monkeypatch):
    monkeypatch.setenv("IG_ACCESS_TOKEN", "tok")
    monkeypatch.setenv("IG_BUSINESS_ACCOUNT_ID", "acct")

    client = client_from_env()

    assert isinstance(client, InstagramClient)

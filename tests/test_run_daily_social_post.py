"""Regression test: a promoted (Tier 2) channel with missing credentials must
fall back to Tier 3, never crash the whole run. Reproduces the 2026-09-06
daily-trigger failure: 'Cannot start: IG_ACCESS_TOKEN and IG_BUSINESS_ACCOUNT_ID
must both be set...' aborted every channel, not just instagram."""
from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from run_daily_social_post import build_channel_publishers


class TestBuildChannelPublishers(unittest.TestCase):
    def test_promoted_channel_without_credentials_falls_back_not_raises(self):
        config = {"tier_override": {"instagram": 2, "facebook": 2}}
        env = {k: v for k, v in os.environ.items() if k not in ("IG_ACCESS_TOKEN", "IG_BUSINESS_ACCOUNT_ID", "FB_PAGE_ACCESS_TOKEN", "FB_PAGE_ID")}
        with patch.dict(os.environ, env, clear=True):
            publishers = build_channel_publishers(config)
        self.assertEqual(publishers, {})

    def test_promoted_channel_with_credentials_registers_publisher(self):
        config = {"tier_override": {"instagram": 2}}
        env = {"IG_ACCESS_TOKEN": "tok", "IG_BUSINESS_ACCOUNT_ID": "acct"}
        with patch.dict(os.environ, env, clear=False):
            publishers = build_channel_publishers(config)
        self.assertIn("instagram", publishers)

    def test_non_promoted_channel_never_touches_credentials(self):
        config = {"tier_override": {"instagram": 3, "facebook": 3}}
        publishers = build_channel_publishers(config)
        self.assertEqual(publishers, {})


if __name__ == "__main__":
    unittest.main()

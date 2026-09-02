# Decision: promote Instagram + Facebook to Tier 2 (autonomous + notify)

**Date:** 2026-09-03
**Decided by:** founder (confirmed via AskUserQuestion in the MILI session)

## What changed
`automation/daily-social-post.yaml`'s `tier_override` for `instagram` and
`facebook` moved from `3` (human sign-off) to `2` (autonomous + notify).
`tiktok` stays at `3`.

## Why
Store analytics showed $0 gross sales in the last 30 days — the founder
wants the daily posting pipeline actually publishing, not just drafting,
once credentials are wired up. IG/FB credentials were confirmed available
to set up; TikTok's are not (its Content Posting API also requires app
review, independent of credentials).

## Safety note
Promoting the tier alone does not cause an accidental post: `publish()`
still falls back to Tier 3 for a channel with no registered
`channel_publishers` entry, which only happens once
`IG_ACCESS_TOKEN`/`IG_BUSINESS_ACCOUNT_ID` (or the FB equivalents) are set
in the environment that runs `run_daily_social_post.py`. Until then this
promotion is a no-op in practice.

## Follow-up
Founder to set the 4 required env vars in the environment that will
actually run the script (not pasted into a chat session — see
`docs/04-tech-stack.md`), then run `run_daily_social_post.py` once and
review the first live post by hand.

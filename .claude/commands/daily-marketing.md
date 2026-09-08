---
name: daily-marketing
description: Build today's time-scheduled post queue across X, LinkedIn, Instagram, YouTube. Draft + queue only, never publishes.
---

Run the `cmo` lead agent, delegating to `mktg-daily-publisher` and (as needed)
`mktg-storyteller` / `mktg-shortform-scriptwriter`.

1. Check `marketing/published/` for the last 14 days of angles already used —
   do not repeat one.
2. Pull today's real signal to build from: the actual product catalog
   (`src/roles/ai-digital-product.md`'s precedent products, or whatever is
   live on Shopify right now), not an invented topic.
3. Produce one post per channel (X, LinkedIn, Instagram, YouTube), each with:
   hook, body, CTA, suggested post time.
4. Write the full day's queue to `marketing/queue/<date>.md` as a single
   file, one section per channel. Do NOT publish anything — this command's
   entire job ends at a reviewable draft.
5. Tell the founder the queue is ready for review at that path.

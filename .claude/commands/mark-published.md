---
name: mark-published
description: Move a queued post to marketing/published/ and log it. Usage: /mark-published <file>
---

Takes one argument: the path to a queued post file (e.g.
`marketing/queue/2026-09-08.md`).

1. Confirm the founder has actually published it externally — this command
   only ever runs AFTER a real, founder-done publish action, never before.
2. Move the file from `marketing/queue/` to `marketing/published/`, keeping
   the same filename.
3. Append a one-line entry to `marketing/published/log.md`: date, channel(s),
   angle/topic, and the file path — so `mktg-daily-publisher` can read this
   log next time to avoid repeating angles.
4. Confirm the move to the founder.

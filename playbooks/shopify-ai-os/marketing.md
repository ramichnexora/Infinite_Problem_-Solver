# Playbook: Marketing — content that sells the next guide

Promoted from the delivered Shopify AI Operating System artifact. Owning
seat: `marketing` (`agents/marketing_agent.py`, `docs/roles/ai-marketing.md`).

## Objective
Produce content (short-form scripts, hook banks, product copy, newsletter)
that drives traffic and conversion for the guide catalog.

## Trigger
New guide launch, weekly content cadence, or a founder request.

## Inputs
Guide title/outline, target audience segment, existing reviews/DM language,
`memory/preferences/voice.md`.

## Preconditions
`master-prompt.md` loaded.

## Step-by-step process
1. **Short-form hook generator (PSL)** — Role: short-form video coach.
   Context: guide title, audience, CTA. Command: 3 scripts, Point-Story-
   Lesson, sharp pain -> true mini-story -> 1 lesson -> CTA. Format: Hook (1
   line), Story (3-5 lines), Lesson (3 steps).
2. **Hook bank from customer language** — Role: voice-of-customer analyst.
   Context: DM screenshots/reviews/comments. Command: extract 25 hooks in
   the customer's own words, tagged to pain/desire. Format: table (Hook,
   Pain/Desire, Source, Best use).
3. **Product-page copy from the outcome** — Role: direct-response copywriter.
   Context: guide title, contents, price, real outcome. Command: lead with
   outcome not feature list, every claim grounded. Format: headline, hook,
   "what's inside," "who it's for," CTA.
4. **Weekly newsletter (Story-Lesson-Offer)** — Role: newsletter editor.
   Context: list size, topic, featured guide. Command: personal win, one
   lesson, one CTA. Format: subject, preview, body.

## Tools
`marketing` agent seat; Claude for drafting; Canva for visuals (see
`docs/04-tech-stack.md`).

## Quality standards
Every claim grounded in a real number or review; no invented stats
(per artifact's "never invent fake stats" rule).

## Decision rules
Escalate (Tier 2 notify) any content referencing a specific customer by name
before it's used publicly.

## Failure handling
If output reads generic/off-voice, re-check `memory/preferences/voice.md`
was loaded; don't publish, regenerate.

## Definition of Done
Draft matches the requested format exactly and passes the QA 3-point check
from the master prompt.

## Output format
Per prompt above — scripts, tables, or structured copy blocks.

---
**Owner (human):** founder (Marketing Leader)
**Version:** v1 — promoted from Shopify AI OS artifact
**Status:** active

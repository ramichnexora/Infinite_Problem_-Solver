# Worked Example: An AI-Education Content & Commerce Brand

This is a worked instantiation of `docs/roles/ai-marketing.md` for a specific kind of
business: an AI-education brand that sells through content (Shopify store, PDF guides,
templates, prompt libraries, courses, memberships) rather than through outbound sales.
It exists to show how the generic seat model in this repo maps onto a real,
demanding content operation — it is not a new seat, and it is not required reading to
use the rest of `docs/`.

If you're standing up this kind of business, read this after `docs/roles/ai-marketing.md`,
not instead of it. Everything below is the AI Marketing Agent's mandate, made concrete.

## Business context

- **Model**: Shopify store selling premium PDF guides, AI templates/systems, prompt
  libraries, courses, memberships, and community access.
- **Mission**: help people solve real problems faster with AI.
- **What actually gets measured**: not views. Customer transformation, brand trust,
  audience loyalty, email subscribers, Shopify revenue, returning customers, community
  growth. A viral post that doesn't move any of those numbers is a cost, not a win —
  see "Optimize for business growth" below.

## Optimize for business growth, not views

`docs/roles/ai-marketing.md`'s KPIs are pipeline/leads and engagement-as-a-leading-
indicator, deliberately in that order. For a content-commerce brand, "pipeline" reads
as: email subscribers, store visits, product sales, returning customers, community
growth. Views and reach are instrumentation, not the goal — a content piece that gets
views but drives none of the business metrics should be treated as a miss, not a win,
when reviewed in the weekly KPI cycle (`docs/02-org-chart.md` reporting rhythm).

## The audience framework (fill in before drafting)

Every content brief handed to the AI Marketing Agent should answer:

| Question | Example |
|---|---|
| Who is this for? | Solo founders new to AI tools |
| What problem are they solving? | Wasting hours on manual setup |
| Why do they care right now? | Launching this month, feeling behind |
| What objection do they have? | "I've tried AI tools before and they didn't stick" |
| What outcome do they want? | A working setup in under 30 minutes |

`agents/marketing_agent.py`'s `draft()` passes `audience`, `pain_point`, and
`desired_outcome` fields from the brief straight into the model prompt when present —
fill them in on the brief rather than leaving the model to guess.

## The content value test

A piece only ships if it does at least one of: teach, save time, make money, reduce
stress, increase productivity, help avoid a mistake, solve a real problem, simplify AI,
or build confidence. Entertainment with no value-test hit doesn't get published under
this brand.

This is a judgment call, not a regex, so it's enforced the way
`docs/01-principles.md` principle 3 says uncertainty should be handled: the model is
instructed (see `DRAFT_SYSTEM_PROMPT` in `agents/marketing_agent.py`) to set
`"escalate": true` and explain why when a brief doesn't clear the test, and that
routes through the same confidence gate as any other low-confidence draft — a human
reviews it before anything publishes.

## Daily content factory

One flagship piece, adapted per platform rather than re-created per platform:

| Format | Platform | Notes |
|---|---|---|
| Flagship vertical video (~31s) | Instagram Reels, TikTok, YouTube Shorts, Facebook | Same script, platform-native captions/hashtags |
| Idea Pin | Pinterest | Search-intent title, not just a repost |
| Thread | X | Broken into the same hook → problem → solution → example → CTA beats |
| Email teaser | Email list | Drives back to the full piece or the store |
| Blog outline (optional) | Owned site | For SEO-driven topics, not every day |

Publishing/scheduling to each of these is a **tooling** decision, not a framework one —
scope it per `docs/04-tech-stack.md`'s "adding a new integration" section before
granting the agent write access to any of them.

## The 31-second structure

| Time | Beat |
|---|---|
| 0–2s | Pattern interrupt (the hook) |
| 3–8s | Problem |
| 9–20s | Solution |
| 21–27s | Concrete example |
| 28–31s | Single, clear CTA |

The same beats compress into a thread, an email teaser, or a Pin title — the hook is
still line one, the CTA is still the last line.

## Quality gate (ask before publishing)

- Would I save this?
- Would I share this?
- Would I follow this account because of it?
- Does it solve a real problem?
- Does it increase trust in the brand?

If the honest answer to any of these is no, it goes back for another pass rather than
shipping on schedule for its own sake.

## Brand/avatar consistency

If the brand uses a consistent AI avatar (from provided photos/voice), lock and reuse:
face, voice, personality, color palette, background, clothing style, and energy level
across every piece. Inconsistency here reads as an unfinished brand faster than almost
anything else — treat drift in any of these as a defect, not a stylistic choice.

## SEO checklist per piece

- Primary keyword (passed through as `primary_keyword` on the brief)
- 2–3 secondary/long-tail keywords
- Clear search intent match (informational vs. commercial)
- Natural keyword placement — not stuffed
- Optimized title and description
- Platform-appropriate hashtags

## The funnel (educate first, sell second)

```
content -> follow -> email subscriber -> free resource -> store visit -> product purchase -> returning customer -> community
```

Every piece should nudge toward the next step in this chain, never jump straight to a
hard sell. A piece that's 100% pitch with no teaching has failed the content value test
above before it fails the funnel.

## Reporting cadence

This slots directly into the existing rhythm in `docs/02-org-chart.md` and
`docs/05-metrics-dashboard.md` — nothing new to build, just what goes in each cadence:

- **Daily** — status digest: what published, what's queued, what escalated (already
  the standard digest format every seat uses).
- **Weekly** — top/worst performing content, lessons learned, algorithm observations,
  new content ideas, customer questions that surfaced, product opportunities.
- **Monthly** — growth dashboard, content audit, SEO audit, competitor scan, audience
  insights, revenue attribution by content piece, next month's plan.
- **Annual** — a 365-day content roadmap (topic, objective, audience, hook, CTA, KPIs
  per day) reviewed and re-planned quarterly, not written once and left static — stale
  plans get overridden by real weekly/monthly signal, per
  `docs/01-principles.md` principle 7 ("optimize the system, not the seat").

## Mapping the "14 departments" onto real seats

A content-commerce brand often gets pitched as needing a dozen-plus specialist roles
(CMO, social media, SEO, email, Pinterest, TikTok, analytics, etc.). Per
`docs/01-principles.md` principle 8, that's seat sprawl, not org design. In this
framework it collapses to:

| Pitched role | Actual owner here |
|---|---|
| CMO, Social Media, SEO, Email Marketing, Pinterest/IG/TikTok/FB/YouTube strategist | `docs/roles/ai-marketing.md` (one seat, one mandate) |
| Shopify Growth, Conversion Rate Optimizer | `docs/roles/ai-marketing.md` (funnel above) + human Shopify owner for storefront changes |
| Product Research, Trend Researcher | `docs/roles/ai-product-research.md` |
| Customer Support, Community Manager | `docs/roles/ai-support.md` |
| Analytics, Data Analyst | Folded into each seat's KPI reporting (`docs/05-metrics-dashboard.md`); no separate seat |
| Competitor Research | Feeds `docs/roles/ai-marketing.md`'s planning SOP as an input, not a seat |
| Finance | `docs/roles/ai-finance.md` |
| Automation, QA | `docs/roles/ai-operations.md` |

If, after running the Marketing seat for a while, one function genuinely outgrows what
one seat can own (e.g., SEO becomes a full-time, high-stakes body of work), split it
out the same way any new seat gets added: `docs/06-implementation-roadmap.md`,
"Adding a new AI seat later."

## The golden rule

Every piece should make the audience say "this actually helped me." That's the bar —
above engagement, above reach, above any single vanity number.

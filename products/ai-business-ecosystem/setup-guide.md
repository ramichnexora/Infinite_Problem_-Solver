# Setup Guide (written walkthrough)

The sales page promises a "Setup Video Library." I can't record screen video, so this
is a written substitute covering the same connections: Notion, Make.com, OpenAI,
Slack, and (optionally) Buffer. If you ship this product to buyers, either record real
videos from this outline or adjust the sales copy to describe a written guide instead
— don't ship the "video library" claim without actual videos.

Total time: 60-90 minutes, matching the sales page's estimate, assuming you already
have accounts on the tools below (all have free tiers to start).

## 1. Notion (5 minutes)

1. If you don't already have a Notion account, sign up free at notion.so.
2. Get access to the workspace in `notion-workspace.md`, or recreate the 4 databases
   there manually using the schema tables in that doc.
3. Add the 4 named views (Pipeline Board, Timeline, Publish Calendar, Revenue This
   Month) per the instructions in that doc's "Known follow-up" section.
4. Note your workspace's integration token if you'll be connecting Make.com to it
   (Settings → Connections → Develop or manage integrations → create a new internal
   integration, copy the token). Share each of the 4 databases with that integration
   (··· menu on each database → Connections → add your integration).

## 2. OpenAI (5 minutes)

1. Sign up at platform.openai.com if you don't have an account.
2. Add a payment method (the automations run on pay-as-you-go API usage, separate
   from any ChatGPT subscription).
3. Create an API key (API keys → Create new secret key). Copy it somewhere safe — it's
   shown once.
4. Estimate cost: with `gpt-4o-mini`-class models, each lead costs roughly $0.01-0.03
   in API calls (2 short completions), and each content-multiplication run costs
   roughly $0.02-0.05 (3 completions). Budget accordingly for volume.

## 3. Make.com (20-30 minutes — the bulk of setup)

1. Sign up at make.com. The free tier (1,000 operations/month) is enough to test; the
   sales page recommends a paid tier for real volume.
2. Create a new scenario for the Lead Capture & Enrichment Engine. Follow
   `make-automations/lead-capture-enrichment.md` module by module — add each module in
   order, connect your OpenAI and Notion accounts when prompted (Make will ask you to
   authorize each app the first time you add one of its modules).
3. Create a second scenario for the Content Multiplication Engine, following
   `make-automations/content-multiplication.md` the same way.
4. Test each scenario using the checklists at the bottom of each spec file before
   turning them on for real traffic.
5. Turn scenario scheduling to "Immediately" (or the shortest interval your plan
   allows) so leads/content get processed close to real-time.

## 4. Slack (5 minutes)

1. If you don't already have a workspace, create one free at slack.com.
2. Create two channels: `#new-leads` and `#hot-leads` (or reuse one channel if you
   don't need the score-based split — adjust the Router step in the Lead Capture spec
   accordingly).
3. When you add the Slack module in Make.com, it'll walk you through authorizing
   Make's Slack app for your workspace and picking the channel.

## 5. Buffer (optional, 5 minutes)

Only needed if you want the Content Multiplication automation to auto-schedule posts
rather than leaving them as approved drafts for manual scheduling.

1. Sign up at buffer.com if you want this.
2. Connect your LinkedIn/X/Facebook accounts to Buffer.
3. Add the optional Buffer module described at the bottom of
   `make-automations/content-multiplication.md`.

## 6. End-to-end test

1. Send a test lead through your webhook (curl, Postman, or an actual test form
   submission). Confirm within ~60 seconds: a new CRM row appears with AI-populated
   Pain Points, Company Research, and Lead Score, and a Slack message lands in the
   right channel.
2. Create a test row in the Content Calendar with `Platform = Original Draft` and some
   body text, then flip `Status` to `Approved`. Confirm 3 new rows appear (LinkedIn, X,
   Facebook), each linked back via `Source Post`.

If either test doesn't work, check the module-by-module specs' "Testing checklist"
sections first — they call out the most common break points (malformed JSON from the
model, field-name mismatches between your form and the webhook payload).

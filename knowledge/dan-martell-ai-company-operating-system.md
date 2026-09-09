---
title: The AI Operating System for Business Owners (Dan Martell)
source: Dan Martell — 'AI Company Operating System Playbook' (PDF, 20 pages, distributed as a free playbook: 'Make this your playbook… Copy, paste, ship.')
imported: 2026-09-09
format: text extracted from PDF; layout simplified, wording unchanged
---

# The AI Operating System for Business Owners (Dan Martell)

> Why it is here: this playbook is the origin of this repo's org design — the Replacement Ladder rungs (Gatekeeper / Concierge / Storyteller / Deal Maker / Chief), the RCCF prompt shape and the department prompt library that `.claude/agents/*` implement. `knowledge/ai-replacement-ladder.md` is the condensed version; this is the full source. Tool recommendations in it are the author's own affiliations — evaluate on merit.

NOTE: This document is part of my Elite Coaching Program.
This SOP can help you integrate AI across your business without needing to hire additional
staff, learn technical skills, or build complex systems.
Our approach is implementing AI in a simple, practical way that enhances your existing
operations, team, and workflows.
This process is not just about automation but creating an operating system where AI works
alongside your team, driving results that feel effortless and sustainable, ultimately leading to
growth without more cost or chaos.
And that’s exactly what my Elite Coaching Program offers!
Message me on Instagram “ELITE” if you’re interested in learning more:
https://www.instagram.com/danmartell/
THE AI OPERATING SYSTEM FOR
BUSINESS OWNERS
Roll out AI across every department without hiring or getting technical.
Make this your playbook. It is simple, fast, and real. Copy, paste, ship.

## What you get

- The AI Buyback Loop so you can get your own time back immediately.
- The AI Replacement Ladder to know how to embed AI at every rung.
- A 4-Part AI Deployment Playbook
- A Master Prompt Template you can edit and use in your team.
- The RCCF Prompt format I use for all my departments.
- Prompts your team can reuse for every department.

## The AI Buyback Loop: Audit → Transfer → Fill

Buying back your time isn't a one-time event. It's a loop. You audit where your time goes, you
transfer the low-value work off your plate, and you fill the space you just created with
higher-leverage work. Then you run it again. Each pass moves you closer to a calendar full of
green.


### 1. Audit

You can't buy back time you can't see. Most people think they know where their week goes —
they're wrong. Your calendar reveals your real priorities far more accurately than your stated
intentions, and the gap between the two is where the leak is.

A calendar audit is simple: pull your last 7–14 days, color-code every block by energy (🟢
energizes you, 🟡 neutral, 🔴 drains you), and sort each task by whether you should be the one
doing it. The reds and the low-value tasks are your transfer list. The goal is a calendar full of
green.

Don't do this by hand. Connect an AI to your calendar (or paste the events) and run the prompt
below. It takes about 15 minutes and gives you a ranked list of what to stop, delegate, and
protect.

**SYSTEM PROMPT — The Sunday Calendar & Energy Audit**

```

You are my Time & Energy Auditor. You operate from one belief: time management
is a lie — energy management is the truth. Two tasks can take the same hour and
have opposite effects on my performance. Your job is to look at my actual calendar
and tell me the truth about where my time goes, where my energy leaks, and what I
should stop, delegate, or protect. Core belief: "I can tell you everything about a
person's life by looking at their calendar." Be direct. No hedging. Frameworks first.
You are not here to make me feel good about a busy week.

INPUT: I'll give you my calendar for the last 7–14 days (titles, durations, attendees).
Ask once for anything missing, then proceed. Also confirm up front: (1) my #1 goal
this quarter, (2) my Buyback Rate ≈ (annual income ÷ 2,000) ÷ 4 — the threshold
for what I should pay someone else to do, (3) the work I'm uniquely great at and
want more of.

STEP 1 — Reconstruct the week. Categorize every block (Meeting / Admin /
Deep Work / Sales / Content / Family-Personal / Recharge / Travel / Reactive).
Surface total scheduled hours vs. available hours, unplanned/reactive time, and
commitments I said mattered but bumped.

STEP 2 — Energy Audit. Color-code every task: 🟢 Energize (I'd do it for free), 🟡
Neutral, 🔴 Drain (I dread it). Output my % split. "Your reds are someone else's
greens."

STEP 3 — DRIP Matrix. Sort each task on money × energy: Delegate (low value +
draining), Replace (high value + draining), Invest (energizing + low value today),
Produce (high value + energizing). Flag everything below my Buyback Rate. Aim to
trend 95% toward Produce.

STEP 4 — 2×2 Truth Grid. Score each block on two axes: Right direction? (moves
my #1 goal) × Right person? (should I do it). No-direction + yes-person = stop.
Yes-direction + no-person = delegate. No + no = eliminate. Tell me which bucket
eats the most hours — that's my biggest leak.

STEP 5 — Insights. Give me the headline (where my time really goes vs. where I
say it should), my energy verdict and what it predicts for the next 90 days, the 3
biggest leaks with dollar cost, whether I had a time problem or a compliance
problem, and what Greens never made it onto the calendar at all.

STEP 6 — Action list. End with decisions, not suggestions: STOP →
DELEGATE/REPLACE (lowest-value reds first, name the first hire if a pattern is
clear) → AUTOMATE → PROTECT (lock my greens and personal blocks into next
week first) → DESIGN next week's Perfect Week (everything goes in — deep work,
sales, content, workouts, family, date night, recharge, even meals).

OUTPUT: Summary on top, body bucketed by section (most immediate first),
priority action list at the bottom. Use 🟢🟡🔴 throughout so I can scan it in
seconds.

TONE: Founder-to-founder. High conviction. No "try," "maybe," or "hope" — replace
them with decisions. "Stop managing time. Start managing energy. The goal is a
calendar full of green."
```


### 2. Transfer

Once the audit tells you what to offload, you transfer it. There are two levels.

Level 1 — The Camcorder Method (transfer to a human). The next time you do the task,
record yourself doing it and narrate as you go — like you're filming a how-to. Drop the transcript
into AI and have it write the SOP for you: clean steps, checklists, edge cases. You've just turned
a 20-minute task you'll never do again into a document a team member can follow. The
camcorder does the documentation work; the human takes the task.

Level 2 — Transfer to AI (skip the human). The higher level isn't handing the task to a person
— it's handing the outcome to your agent. Instead of documenting the steps, you describe the
result you want and let the AI do the entire task. No SOP, no hire, no handoff. You define
success and your agent produces the work. This is where the real leverage compounds: every
task you can describe by outcome is a task you no longer touch.


### 3. Fill

Buying back the time is only half of it. If you don't intentionally fill the space, it gets eaten by
reactive work and you're right back where you started. Fill it on three levels.

Skills. The first thing to do with new space is upgrade your AI skills — that's what makes every
future transfer faster and more powerful. The fastest way to learn is to follow the people actually
building at the edge and copy what they do. Pick a handful of operators on X (Twitter),
Instagram, and YouTube who ship real workflows — not hype — and study their prompts, their
agents, and their automations. Bookmark what works, rebuild it yourself, and adapt it to your
business.

Habits. Make creation a daily and weekly habit. Build one new automation every day, or at
minimum one every week. Treat it like reps in the gym — the point isn't any single automation,
it's that you become someone who compounds leverage as a default. Growth comes from the
habit, not the highlight.

Beliefs. The world is changing faster than most people's beliefs about what's possible. The
biggest constraint isn't your tools — it's an outdated mental model of what one person can do.
With AI in your hands, you can create, build, and produce at a scale that was impossible a year
ago. Upgrade what you believe is possible, then aim your newly bought-back time at it. The loop
only works as far as your beliefs let it.

Audit. Transfer. Fill. Run it again.


## The AI Replacement Ladder

The Replacement Ladder tells you who to hire and in what order to get the most value back:
Admin → Delivery → Marketing → Sales → Leadership. Climb it out of order and you stay stuck
doing low-value work.

The AI Replacement Ladder runs the same five rungs, but flips the move. Before you hire a
person, you hire tokens.

Tokens first, hire later.

The rule is simple: at every rung, hand off as much as possible to AI before you bring on a
human. Tokens are cheaper than payroll, available 24/7, and scale instantly. You only hire a
person once AI has absorbed everything it can, and even then, that person manages the AI, not
the busywork. Here's the AI fix for each rung.


### Rung 1 — Admin → The Gatekeeper

Use AI as your inbox and calendar manager, an auditor that protects your time. It triages every
email, drafts replies in your voice, routes what can be delegated, and surfaces only what truly
needs you. This is the first and highest-leverage rung because admin is what buries most
founders.

**System prompt — The Gatekeeper (inbox manager):**

```

You are my Gatekeeper, my inbox and calendar manager. You operate as me, in my
voice, and your job is to protect my time and get my inbox to zero.

Process, in this exact sequence:

1. Pull everything. Read ALL emails in the inbox, do not pre-filter by
Promotions / Social / Updates. Filtering too early hides high-priority items. I
want every message in front of you.
2. Strip the noise first. Identify automated mail, spam, receipts, and tool
alerts. Auto-archive or label them. (In a typical day this is ~60–65% of
volume, FYI noise + tool alerts.)
3. Triage the rest by intent into five buckets:

Reply (me) — needs my voice or my decision. Draft the reply for me.

Delegate — route to my assistant with a one-line instruction.

Monitor / FYI — no action, just awareness. Summarize in one line.

Schedule — turns into a calendar event; propose the block.

No reply needed — archive.
4. Draft in my voice. For every Reply item, write the full draft using prior
thread context and how I've answered similar messages before. Direct,
warm, no fluff. Never send. Draft only.
5. Present for review. Output a structured table: Sender | Subject | Intent |
Suggested action | Draft (if any). Most immediate at top. I review, approve,
and you send the approved ones.

Calendar duties: Flag any meeting with no agenda, no buffer, or that conflicts with
my protected blocks (deep work, family, workouts). Protect those blocks first;
everything else schedules around them.

Rules: Never send or schedule without my approval. Capture useful info (contacts,
commitments, decisions) to memory as you go. When unsure, ask once, then
proceed.
```

### Rung 2 — Delivery → The Concierge

Use AI as a customer support and onboarding system. Through chat or voice AI, it triages
incoming issues, answers questions, walks customers through onboarding, and resolves
problems, often with zero human interaction. Your customers get instant, 24/7 help; your team
only touches the edge cases AI escalates. Delivery stops depending on your calendar.

### Rung 3 — Marketing → The Storyteller

Success leaves clues.

The hardest part of marketing isn't production, it's knowing what to make. The Storyteller studies
what's already working online, then remixes it with your own insights, stories, and perspective.
AI is built for exactly this: spot the pattern, then make it yours. (Note: thumbnails and titles
deserve as much creative time as the content itself. They're the primary lever for click-through.)

**System prompt — The Storytell (viral YouTube ideas):**

```

You are my Storyteller. Principle: success leaves clues. Find what's working, then
help me remix it with my own angle.

1. Given my niche [TOPIC] and audience [WHO], find 10 recent outlier
YouTube videos. Ones whose views massively outperform the channel's
subscriber count (the clearest signal an idea is hot).
2. For each, extract the pattern: the hook/angle, the title structure, the
thumbnail concept, and why it worked psychologically (curiosity gap, stakes,
contrarian take, transformation promise).

3. Remix, don't copy. Generate 10 new video concepts that apply those
proven patterns to MY expertise and stories. For each: a working title, a
one-line thumbnail concept, and the 3-second hook.
4. Rank them by predicted click-through and how uniquely I can tell that story.

Never invent fake stats or stories. Use my real frameworks and experiences as the
raw material.
```

### Rung 4 — Sales → The Deal Maker

Use AI to support every sales activity… especially Selling by Chat. This doesn’t mean AI is
chatting for you, but it can summarize each conversation so you can pick up exactly where you
left off, captures key info just from the dialogue (objections, budget, timeline, next steps), and
turns every conversation into data for training and improvement. You close faster, forget nothing,
and your whole process gets smarter with every deal.

The best example of this in action is Winly, software I built to solve this exact problem for
myself: AI-assisted chat-based selling that summarizes, captures, and improves with every
conversation.

### Rung 5 — Leadership → The Chief

This is the super move. At the top of the ladder you build a digital brain than any AI or agent
can work with. Mine is called APEX (learn more at apex.host).

A digital brain holds your knowledge, perspectives, decisions, and frameworks in one place.
Then you give your whole team access to it. Your admin, support, marketing, and sales people
ask it their questions instead of asking you. AI becomes the first line of response for anyone
who needs your insight.

That's what makes it a super move: it doesn't replace one rung, it amplifies all of them. Every
other rung gets smarter and more self-sufficient because the answers people used to need from
you now come from your digital brain. You stop being the bottleneck.

Climb it in order. At every rung: tokens first, hire later.


## The 4-Part AI Deployment Playbook

Remove Costs • Move Faster • Scale Without Adding Headcount

Most founders buy AI like it’s a shiny object.
Smart founders use AI like it’s a competitive weapon.
If you want to scale without burning cash, this is the exact process I use with 8-figure operators.

### Step 1: Audit the Business & Expose the Opportunities
Goal: Pinpoint where AI can immediately reclaim time, eliminate errors, and
multiply output.
AI only creates leverage when it’s applied to bottlenecks.
So before you buy a single tool, you need a brutally honest operational audit.

### Start With a Full Process Sweep

List out every recurring task in each department. Rank them by:
- Time investment

- Money investment
Look for processes that are repetitive, rules-based, or rely on data that already exists.
Those are your leverage points.

### Where AI Usually Delivers the Fastest Wins

Sales
- AI qualifies leads automatically (You can use tool like Winly to do this in your DM’s)

- Predicts which prospects will close

- Auto-summarizes calls into CRM-ready notes
Customer Success
- Automates onboarding

- Create follow-up sequences

- Auto-route customer support tickets

Operations
- Auto-generate schedules, assign tasks, and predict workload surges

- Inventory automation + demand forecasting

- Internal AI helpdesk answers team questions instantly

Finance (you can use tools like Frank)
- Scan invoices, categorize expenses, chase missing receipts

- Detect anomalies or fraud patterns

- Predict cash shortages before they happen

HR & Recruiting
- Automated resume filtering and candidate scoring

- AI assistants handling interview scheduling

- Sentiment analysis on employee feedback

Marketing & Content
- AI-written ads, posts, emails, blogs, video scripts

- Predictive targeting for the highest-converting audiences

- Automated content repurposing + scheduling


### Outcome

Walk away with 3–5 high-ROI opportunities where AI will instantly save time or money.


### Step 2: Choose the Right Tools & Build the Workflow
Goal: Integrate AI into your existing systems so it feels seamless—not
chaotic.
AI tools don’t create leverage… workflows do.
Here’s how to build them like a pro.

### Recommended Tools by Function

Function
Tools
What It Enables
Content
Creation
Copy.ai, Socialsweep.ai ,
Claude.ai
High-quality content at scale
Automation
Zapier, Make.com, n8n.io,
manus.im, code.claude.com
Connect systems without code
CRM & Sales
HubSpot.com, GetWinly.ai,
YourAtlas.com
Lead scoring, auto-replies, call
summaries
Support &
Success
Zendesk AI, Intercom, Chatbase,
Buddypro.ai
24/7 FAQ bots + routing + customer
delivery
Analytics
Precision.co, Hellofrank.ai
Predictive dashboards & insights
Voice/Video
ElevenLabs.io, Heygen
AI voices, video generation, clipping
Hiring & HR
Trainual.com
Screening + candidate communication


### Map the Workflow

Your AI system should follow this pattern:
1. Trigger: A lead opts in or a customer asks a question

2. Artificial Intelligence: AI labels, evaluates, drafts, or routes

3. Automation: Data moves into CRM, Slack, or task systems

4. Human in The Loop: Team reviews only the exceptions
AI should take 80-90% of the repetitive work off your team’s plate.

### Outcome

A clean, visual workflow showing exactly where AI steps in and where humans take over.

### Step 3: Test, Automate & Measure Goal: Prove ROI fast and scale only what works.
Most companies over-engineer.
You’re going to start tiny and scale up only after the data says yes.
1. Start With One High-Value Process
Examples: lead qualification, appointment setting, content repurposing.
Document the before numbers:
- Hours spent

- Monthly cost

- Output quality
2. Automate the Repetitive Steps
Example system:
Lead fills Typeform → AI drafts personalized email → CRM updates automatically
→ Slack pings sales rep
3. Weekly Feedback Loops
- Review outputs

- Fix tone issues

- Improve prompts

- Tighten logic
4. Track These Core Metrics

Metric
Measures
Time Saved
Hours eliminated per task
Cost
Labor vs automation cost
Output
Consistency
Percentage approved without edits
ROI
(Savings + Revenue Lift – AI Cost) ÷ AI Cost
5. Scale What Works
Once a workflow proves ROI, replicate it in other departments.

### Outcome

A battle-tested AI system that runs reliably, improves over time, and prints operational efficiency.

### Step 4: Scale Your AI Deployment Goal: Turn AI from a tool into a company-wide operating system.
This is how you go from “We’re trying AI” to “We’re an AI-driven company.”
1. Standardize the Wins
Turn successful workflows into SOPs.
Document in Notion, Google Drive, or Asana.
This makes AI scalable.
2. Build a Team That Thinks in Automations
- Run monthly AI “Show & Tell” sessions

- Assign an AI Champion in each department

- Encourage bottom-up automation ideas
3. Measure Quarterly Gains & Reinvest
Track savings, output gains, and speed improvements.
Then reinvest those gains into more AI automation.
AI is a flywheel - keep feeding it.

## Ready to Deploy Business Prompts

Want AI to work like a top hire in every part of your business?

Start with your Master Prompt - it tells the AI exactly how to show up for you.

Paste it once per chat and your voice, style, and priorities stay locked in.

Then use the RCCF format to guide any task with role, context, command, and format.

From there, this library gives you ready-to-run prompts for Marketing, Sales, Success, Product,
etc.

Each one is built to save time, cut waste, and drive revenue today.

You get scripts, outlines, angles, call plans, playbooks, specs, tests, releases, and more.

No fluff. No buzzwords. Just tools that help you act fast and act smart.

Run these prompts to scale your business today.

## Company Master Prompt Template

Paste this once per chat. Keep it at the top of your project chat.
"Hey, here is how to show up for me every time:
My name is [NAME]. I run [COMPANY], a [BUSINESS TYPE] that sells [OFFER] to
[AUDIENCE]. I am an entrepreneur and operator. I like fast, clear answers that help me act
today.
Voice and style: energetic, motivational, casual. Short sentences. Punchy lines. Conversational
flow. Keep it PG. Use American spelling. Use simple words. Grade 5 to 7 reading level.

Hooks: use questions to pull me in. Highlight key ideas with caps, bold, or italics. End sections
on a strong line that pushes action.
Analogies: use restaurants, laundromats, grocery lines, airplanes, and sports teams when
helpful.
Formatting: lots of line breaks. Numbered steps. Bullets. Tables when we compare options.
Straight quotes only. No em dashes.
My priorities: grow revenue, cut waste, free up time. I value leverage, speed, and clarity. I prefer
concrete examples over theory.
When you write for me: give me 3 options when choosing. Push back if my ask is weak. Offer a
better path and say why.
Constraints: avoid buzzwords. Avoid vague claims. If a claim needs proof, cite a simple number
or show a test to run.
QA: before you finish, do a 3 point quality check. 1) Is it simple. 2) Is it useful today. 3) Is the
next step clear.
If info is missing, ask me up to 3 short questions. If you have enough to act, act. Do not stall.
Remember this style for future chats. If you are unsure, ask clarifying questions first."

## RCCF Prompt Format:

- Role: [ROLE]
- Context: [GOAL]. Audience: [AUDIENCE]. Inputs: [NUMBERS/LINKS]. Constraints:
[RULES].
- Command: [ACTION]. Give 3 options and a better path if you see one.
- Format: [OUTPUT FORMAT]. End with a CTA. Run the 3-point QA.

## MARKETING PROMPTS TO USE


### Setup

- Create a shared Project named “Marketing”.
- Paste the Master Prompt.
- Edit the variables to match your business.
- Start using prompts below to generate outputs.

### Prompts to Use

1. Short-Form Script Generator (Point • Story • Lesson)

   a. Role: Act as a short-form video coach.
   b. Context: Topic is [TOPIC]. Audience is [AUDIENCE]. Desired action is
[CTA_LINK OR DM].
   c. Command: Write 3 scripts using PSL. Open with a sharp pain, add a true story,
end with 1 actionable lesson and CTA.
   d. Format: For each script: Hook (1 line), Story (3–5 lines), Lesson (3 steps).
2. YouTube Long-Form Outline (Open Loops + Proof)
   a. Role: Act as a YouTube showrunner.
   b. Context: Offer [OFFER]. Avatar [AVATAR]. Core promise [PROMISE].
   c. Command: Outline a 10–12 minute video with a cold open hook, 3 loops, proof
beats, and a soft DM CTA. Include b-roll ideas.
   d. Format: Sections: Cold Open, Big Promise, Loop 1, Loop 2, Loop 3, Proof Stack,
CTA, End Card.
3. Hook Bank from Customer Language
   a. Role: Act as a voice-of-customer analyst.
   b. Context: Inputs: call notes, reviews, comments at [LINKS].
   c. Command: Extract 25 hooks in the customer’s own words. Tag each hook to a
pain or desire.
   d. Format: Table with Hook, Pain/Desire, Source link, Use cases (Short, Email, Ad).
4. Ad Angles and Variations
   a. Role: Act as a media buyer.
   b. Context: Platform [META or YOUTUBE or GOOGLE]. Audience [AUDIENCE].
Budget [BUDGET].
   c. Command: Create 10 angles. Each angle includes 3 copy lines and 1 visual idea.
Keep claims grounded in proof.
   d. Format: Table: Angle name, Lines (1–2 sentences each), Visual idea, Proof note.
5. Creator-CEO Newsletter (Story • Lesson • Offer)
   a. Role: Act as a newsletter editor.
   b. Context: List size [SIZE]. Topic [TOPIC]. Offer [OFFER]. Voice [TONE].
   c. Command: Write a concise email using a personal story, one lesson, one CTA.
   d. Format: Subject, Preview, Body (Story, Lesson, CTA link).

## SALES PROMPTS TO USE


### Setup

- Create a shared Project named “Sales”.
- Paste the Master Prompt.
- Edit the variables to match your business.
- Start using prompts below to generate outputs.

### Prompts to Use

1. Speed-to-Lead Callback Script

   a. Role: Act as a sales responder.
   b. Context: Offer [OFFER]. ICP [ICP]. Qual rules [QUAL_RULES]. Tool
[VOICE_AGENT or DIALER].
   c. Command: Write a fast callback script that confirms need, qualifies lightly, and
sets the next step.
   d. Format: Open (10s), Qual (3 points), Close (next step + time), Notes (CRM
fields).
2. Sell-By-Chat DM Starters
   a. Role: Act as a social seller.
   b. Context: Platform [INSTAGRAM/LINKEDIN]. Audience [AUDIENCE]. Proof
[PROOF_LINKS].
   c. Command: Write 10 human DM openers that invite a reply without pressure;
include light personalization tokens. Example: Hey [NAME], noticed you’re into
cars as well. Wondering, are you here for the vids are looking to grow your
business?
   d. Format: Bullets with Token, Opener, Follow-up nudge, “If no reply” line.
3. Discovery Call Prep
   a. Role: Act as a sales coach.
   b. Context: Prospect [NAME], company [COMPANY], pains [PAIN1/PAIN2], desired
outcome [OUTCOME].
   c. Command: Draft a short discovery plan that confirms goals, budget fit, and
decision process.
   d. Format: 2-min opener, 5 discovery questions, success criteria, red-flag checklist.
4. Objection Handling Playbook
   a. Role: Act as an objection-handling strategist.
   b. Context: Segment [SEGMENT]. Common objection “[OBJECTION]”. Proof
[PROOF_ASSET].
   c. Command: Create 3 talk tracks using different frames (data, story, future-pace)
that stay empathetic and honest.
   d. Format: Track name, When to use, Script (4–6 lines), Optional proof.

## CUSTOMER SUCCESS PROMPTS TO USE


### Setup

- Create a shared Project named “Customer Success”.
- Paste the Master Prompt.
- Edit the variables to match your business.
- Start using prompts below to generate outputs.

### Prompts to Use

1. Day-0 Quick-Start Plan
   a. Role: Act as an onboarding lead.

   b. Context: Account [ACCOUNT]. Goal [VALUE]. Deadline [DATE]. Tier [TIER].
   c. Command: Build a simple plan that gets one meaningful win in week one.
   d. Format: Checklist (3–5 steps), Owners, Acceptance criteria, Welcome note.
2. Risk Radar
   a. Role: Act as a retention analyst.
   b. Context: Usage [USAGE SIGNALS], tickets [TICKETS], sentiment [NOTES],
health rules [HEALTH_SCORE_RULES].
   c. Command: Score risk and propose save plays that are specific and time-bound.
   d. Format: Table with Risk level, Signal, Save play, Owner, Due date.
3. QBR Outline
   a. Role: Act as a CSM.
   b. Context: Account [ACCOUNT]. Last 90-day outcomes [METRICS]. Upcoming
goals [GOALS].
   c. Command: Draft a QBR flow that highlights wins, insights, and a 90-day plan.
   d. Format: Sections: Wins, Insights, Roadmap, Asks, Next steps.
4. Expansion Moment Script
   a. Role: Act as a success-led seller.
   b. Context: Milestone hit [MILESTONE]. Relevant offer [UPSELL].
   c. Command: Create a brief outreach that anchors on earned results and proposes
a next step.
   d. Format: 3-line message + calendar link line.

## PRODUCT PROMPTS TO USE


### Setup

- Create a shared Project named “Product”.
- Paste the Master Prompt.
- Edit the variables to match your business.
- Start using prompts below to generate outputs.

### Prompts to Use

1. Opportunity Ranking
   a. Role: Act as a product strategist.
   b. Context: Candidate ideas [LIST]. Constraints [RESOURCES]. Strategy
[THEMES/OKRs].
   c. Command: Rank opportunities by impact, confidence, and effort with a one-line
rationale.
   d. Format: Table: Idea, Impact, Confidence, Effort, Rationale.
2. One-Page Product Management Sheet
   a. Role: Act as a product manager.
   b. Context: Problem [PROBLEM]. Users [USERS]. Success metric [METRIC].
   c. Command: Write a one-page spec that is problem-first and minimal.

   d. Format: Problem, Users, Scope, User stories, Acceptance, Risks, Success
metric.
3. Experiment Design
   a. Role: Act as a growth PM.
   b. Context: Hypothesis [HYPOTHESIS], sample [SEGMENT], constraint
[BUDGET/TIME].
   c. Command: Design a simple test with pass/fail and decision rule.
   d. Format: Hypothesis, Metric, Threshold, Steps, Decision rule, Next action.
4. Voice-of-Customer Digest
   a. Role: Act as an insights analyst.
   b. Context: Sources [CALLS/REVIEWS/TICKETS LINKS].
   c. Command: Summarize top 5 themes with quotes and suggested product actions.
   d. Format: Table: Theme, Quote, Source, Action idea.
5. Release Notes (Plain English)
   a. Role: Act as a release editor.
   b. Context: Feature [FEATURE]. Benefits [BENEFITS]. Affected users
[SEGMENTS].
   c. Command: Write short notes that explain what changed and why it matters.
   d. Format: Title, What’s new, Why it matters, How to use it, Links.

## ENGINEERING PROMPTS TO USE


### Setup

- Create a shared Project named “Engineering”.
- Paste the Master Prompt.
- Edit the variables to match your business.
- Start using prompts below to generate outputs.

### Prompts to Use

1. PR Review Summary
   a. Role: Act as a senior reviewer.
   b. Context: Repo [REPO]. Stack [STACK]. PR title [TITLE]. Diff notes [NOTES].
   c. Command: Produce a concise review that surfaces risks, tests to add, and merge
readiness.
   d. Format: Risks, Suggestions, Tests, Merge checklist.
2. Bug Triage
   a. Role: Act as a triage lead.
   b. Context: Steps to reproduce [STEPS], expected [EXPECTED], actual [ACTUAL],
severity [SEV].
   c. Command: Draft reproducible steps, likely root causes, and a minimal fix plan.
   d. Format: Repro, Suspects, Fix plan, Acceptance test.
3. Doc Update

   a. Role: Act as a docs scribe.
   b. Context: Feature [FEATURE], entry points [FILES/LINKS].
   c. Command: Update README/guide with setup, usage, and examples.
   d. Format: Section headings with short instructions and example blocks.
4. Test Plan Scaffold
   a. Role: Act as a QA lead.
   b. Context: Component [COMPONENT], behavior [BEHAVIOR], edge cases
[EDGES].
   c. Command: Outline a pragmatic test plan that prevents regressions.
   d. Format: Unit cases, Integration cases, Edge cases, Data/fixtures.
5. Release Checklist
   a. Role: Act as a release manager.
   b. Context: Version [VERSION], envs [ENVS], CI/CD [TOOL].
   c. Command: Provide a pre-release checklist that is safe and fast.
   d. Format: Pre-checks, Steps, Rollback notes, Owner.

## OPERATIONS PROMPTS TO USE


### Setup

- Create a shared Project named “Ops & Finance Implementation”.
- Paste the Master Prompt.
- Edit the variables to match your business.
- Start using prompts below to generate outputs.

### Prompts to Use

1. Weekly KPI Pack
   a. Role: Act as an operator-analyst.
   b. Context: Sources [CRM/ADS/BILLING]. Targets [TARGETS].
   c. Command: Create a one-page scorecard with trends and red flags.
   d. Format: Table: KPI, Current, Trend, Target, Note, Action.
2. Month-End Close Checklist
   a. Role: Act as a finance ops lead.
   b. Context: Accounts [ACCOUNTS], deadlines [DATES], tool
[ACCOUNTING_TOOL].
   c. Command: Draft a close checklist with dependencies and controls.
   d. Format: Steps, Owner, Due date, Control, Evidence link.
3. Daily Cash & Anomalies
   a. Role: Act as a finance sentinel.
   b. Context: Data [BANKS/STRIPE], thresholds [ALERT_RULES].
   c. Command: Generate a daily summary with anomalies and a simple next action.
   d. Format: Cash by account, In/Out, Anomalies, Action.


## FINAL MESSAGE

Pick one department.
Deploy AI today.
Paste the Master Prompt.
Run one of the Role, Context, Command & Format Prompts.
And ship one asset today.
If you want more support implementing AI in your business…
and scaling past $10M+
apply for coaching here and I’ll see if I can help.
DM

P.S.

If you’re looking for the tools I use to run my companies, here’s what I
recommend:

Sell by Chat AI Powered CRM https://getwinly.ai

AI CFO www.hellofrank.ai

AI Clone for Clients or Team www.buddypro.ai

AI Powered Social Search Engine www.socialsweep.ai

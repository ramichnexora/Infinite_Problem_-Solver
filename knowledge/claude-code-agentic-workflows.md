---
title: Build Your First AI Agents with Claude Code
source: AI Automation School — 'Build Your First AI Agents with Claude Code' (PDF, 5 pages)
imported: 2026-09-09
format: text extracted from PDF; layout simplified, wording unchanged
---

# Build Your First AI Agents with Claude Code

> Why it is here: this is the working model for `.claude/agents/` and `CLAUDE.md` in this repo — workflows as plain-English files, plan before build, ask before assuming.

Build Your First AI Agents with Claude Code Claude Code · VS Code · Agentic
Workflows


## Intro

Last time it did what you told it. Today it figures things out. One sentence — it plans,
asks questions, searches the web, and writes a full report. That's an agentic workflow.
Example: You: "Research AI agents in 2026." → Asking clarifying questions... → Searching
the web... → Organising findings... ✓ Report saved to /output/ai-agents-2026.md



## The Framework: Three Levels of Working with AI

Most people never get past level one.
Today you're jumping to three.
1. Chat — You ask. It answers. One question, one response. AI as a smarter search
engine.
2. Build — You direct. It builds. You guide every step; AI executes. You're still doing all
the thinking.
3. Agentic (Today) — You give the goal. It figures out the rest. Describe the outcome,
and the AI plans, picks tools, asks when unsure, and adapts when things change.
The shift: Micromanaging a new employee → trusting an experienced one.

The Definition: Three Things That Make Something Agentic
1. It follows a process. Works through a series of steps, not just answering one
question.
2. It makes decisions. Adapts when things change; pivots when an approach isn't
working.
3. It asks before it assumes. Clarifying questions before starting. This one thing makes
output 10× better.


## Use Cases

- Research & Reports: Multi-source research compiled into a structured report.
- File Organisation: Analyse a folder and sort by category automatically.
- Personalised Outreach: Draft personalised emails for a full list of contacts.
- Competitor Analysis: Side-by-side breakdown built from live research.

Environment: VS Code Setup (2 Minutes)
1. Download VS Code — code.visualstudio.com → pick your OS → download → install.
(Skip if you already have it.)

2. Install the Claude Code extension — Extensions panel → search "claude code" →
Install → Trust publisher.
3. Create your project folder — Open Folder → Documents → New Folder →
"my-first-agent" → Select.
4. Open Claude Code → New Session — Left sidebar → Claude Code icon → New
Session.
Why VS Code instead of raw terminal? File explorer, code view, and Claude Code all in one
window. When the agent creates multiple files, seeing them appear in real time makes a
huge difference.



## The Most Important File: claude.md — Set It Up First

A markdown file in your project
root. Claude reads it automatically every startup. Think of it as an onboarding doc for a new
employee.
1. Project Context — What the workspace is for. "This is my AI agent workspace. I use
it for research, content creation, and productivity workflows."
2. About Me — Who you are and what you care about. "I create content about
technology. My audience wants practical, jargon-free output."
3. Rules (the guardrails):
  - Always ask clarifying questions before starting a complex task
  - Show your plan and steps before executing
  - Keep output concise — bullet points over paragraphs
  - Save all output files to the /output folder
  - Cite sources when doing research
4. Project Structure — /workflows (instruction files) · /output (finished deliverables) ·
/resources (reference docs)
Without claude.md: Generic wall of text, one vague question, no structure, no sources, not
saved anywhere useful. With claude.md: Clarifying questions asked, output in bullet points,
sources cited, file saved to /output exactly as instructed.
Automatic memory (new in 2026): Claude Code now records what it learns as it works and
recalls it in future sessions. The more you use it in a folder, the smarter it gets about your
preferences.

The Mental Model: Three Layers That Make Agentic Workflows Work
- Layer 1 — Workflows: Plain-English markdown files describing a process step by
step. Like a recipe the agent reads and follows — but smart enough to adapt.
- Layer 2 — The Agent: Claude Code itself. Reads your workflows, thinks through
steps, makes decisions. You don't program it; you give it clear instructions.
- Layer 3 — Tools: Read/write files, run terminal commands, search the web. Web
search is built in — no plugins, API keys, or extra setup.

The insight most people miss: A well-written workflow with basic tools outperforms a sloppy
prompt with every plugin in the world. The workflow is where the magic lives.



## Before You Build Anything: Plan Mode — Always Use It First

Claude thinks and plans
but doesn't touch any files. A dry run before anything gets built.
1. Activate Plan Mode — In the chat input, press Shift + Tab twice. (Once = Edit mode,
twice = Plan mode, again = back to normal.)
2. Describe your goal, not the steps — Tell it what you want to accomplish; watch it
break the task into phases on its own.
3. Refine before building — Add or change requirements. It folds them into the existing
plan instead of starting over.
4. Then build — Click "Yes — auto accept" or "Yes — manually approve" to begin.
Switch out of plan mode and watch the File Explorer as files appear.
Plan Mode example (no files changed): You: "I want to research a topic and produce a
structured report." Claude's plan:
1. Ask clarifying questions (scope, audience, depth)
2. Confirm research plan before starting
3. Search and gather sources
4. Write structured report
5. Save to /output with sources cited → Keep planning or proceed?



## The Build: Building the Research Workflow

The workflow file is just plain English. Every
word is editable. No code, no special syntax.
1. Start in Plan Mode + describe the goal: "I want to build a workflow where I can give
you any topic. You research it thoroughly, organise the findings, and produce a clean
structured report. Ask me clarifying questions before starting."
2. Watch it plan the phases — Clarifying questions → research → synthesis → output
→ quality check. You didn't name these steps; it figured them out.
3. Add anything you want: "Also include key takeaways and recommended next steps
at the end." It folds it in — no restart.
4. Build it — the file appears in /workflows/research-report.md. To change anything, just
edit the text; the agent adapts instantly.
What the workflow includes: Clarifying questions to ask · how to confirm the plan · research
rules (sources, date range) · writing tone and format · where to save the output · error
handling if the topic is too broad.
Why this matters: Once written, you can reuse this workflow forever — any topic, any
audience, any depth. The agent follows the same process every time.

The Demo: Running the Agent from Start to Finish
1. Give it a real task: "Research the current state of AI agents in 2026. What are people
using them for? What's working, what's overhyped, where are things heading?"
2. It asks clarifying questions first — Audience · scope · depth · date range · format
preference (because the workflow says to).
3. Answer naturally, like talking to a colleague: "Keep it broad. Hype vs reality
breakdown. Tech-savvy audience, not developers. Medium depth. Last 6–12 months.
Structured with bullet points."
4. Watch the to-do list as it works — Each step ticked off in real time. Web search
happening live, no plugins or API keys needed.
5. Report saved to /output — Press Ctrl + Shift + V to preview the markdown as a
formatted document. Includes executive summary, key findings, sources cited, key
takeaways, and recommended next steps.

## Iteration — the real power:

- "The executive summary is too long. Trim to 3 bullet points." → It edits only that
section.
- "Add a comparison table of the top 5 AI tools mentioned." → It scans its own
research and builds the table. No starting over. Targeted edits. Context remembered
across the whole session.
Honest stat from the report itself: "Even the best models only succeed 45.7% of the time on
real-world tasks." Human oversight isn't optional yet — but that number is changing fast.

Save Yourself Time: 5 Mistakes, 5 Fixes
1. Skipping claude.md — 2 minutes of setup saves hours of repeated instructions. Just
do it.
2. Being too vague — "Do some research" gives garbage. "Research X for [audience],
focus on [Y], last 6 months, bullet points" gives gold.
3. Not using plan mode — Skip planning, go the wrong direction, waste time. 30 extra
seconds of planning saves 20 minutes of cleanup.
4. Not telling it to ask questions — If your workflow doesn't say "ask clarifying questions
first," the agent assumes. Assumptions = mediocre output.
5. Trying to build everything at once — One workflow. Get it working. Refine it. Then
build the next. Don't automate your whole life in a weekend.


## Pro Tips

- Keep all workflow files in a /workflows folder. Stays organised as you build more.
- Read the agent's to-do list as it works — the best tool for catching mistakes before
they snowball.

- When output isn't right, say specifically what to fix. Don't start over; targeted
feedback is faster.
- Save your best claude.md and workflow files. Copy them into new projects as
starting points.
- Hover over any previous message → Roll back to undo file changes. No manual
cleanup needed.
- Type effort:low / effort:medium / effort:high to control how deeply the agent thinks
before responding.



## Your Next Step: Build One Workflow This Week

Just one. Pick something you do
regularly — research, writing, organising, analysis — and turn it into a workflow file. It
doesn't have to be perfect. Just get it running.
The agent did all the thinking, organising, and writing. Now you know how. One workflow.
This week. See what it can do.
Ideas to start: 🔍 Research workflow · ✍️ Writing workflow · 📊 Analysis workflow

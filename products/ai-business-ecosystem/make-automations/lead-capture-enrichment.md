# Lead Capture & Enrichment Engine — Make.com Build Spec

**What it does:** every new lead is researched, scored, logged in the CRM, and pushed
to Slack in under 60 seconds. This is a module-by-module spec to recreate it in
Make.com's visual builder — there is no importable `.blueprint.json` here because it
was never test-imported against a real Make.com account (see the product README for
why). Follow this top to bottom and it maps 1:1 onto Make's scenario editor.

Target CRM: the **CRM (Leads)** Notion database, schema in `products/ai-business-ecosystem/notion-workspace.md`.

## Scenario overview

```
[1] Webhook (lead in) → [2] OpenAI: Company Research → [3] OpenAI: Score + Pain Points
    → [4] Notion: Create CRM row → [5] Router (score gate)
        ├─ High score  → [6a] Slack: priority ping in #hot-leads
        └─ Normal score → [6b] Slack: standard post in #new-leads
```

## Module 1 — Webhooks › Custom webhook

- **Type:** Instant trigger (Custom webhook)
- Create a new webhook, copy its URL, and point your lead source at it:
  - A native form tool (Typeform, Tally, your website's contact form) — most support
    "send to webhook" or "send to Zapier/Make" directly.
  - If your form tool only supports Zapier, add a 1-step Zapier "Webhooks by Zapier →
    POST" as a relay into this same URL.
- **Expected payload (JSON):**
  ```json
  {
    "name": "Jane Doe",
    "company": "Acme Roofing",
    "email": "jane@acmeroofing.com",
    "phone": "+1-555-0100",
    "source": "Inbound Form",
    "message": "Looking for help with scheduling and follow-up."
  }
  ```
- If your form sends different field names, add a **Tools › Set multiple variables**
  module right after the webhook to normalize field names before Module 2.

## Module 2 — OpenAI (ChatGPT) › Create a Chat Completion (Company Research)

- **Model:** `gpt-4o-mini` or equivalent (cheap, this call doesn't need the top model)
- **Limitation to know before you build this:** without a live web-search integration,
  this step reasons from what the lead submitted (company name, message, email domain)
  — it is not a real-time web lookup. For genuinely current company research, insert an
  **HTTP › Make a request** or a search-app module (e.g. SerpApi, Perplexity) *before*
  this one, and paste its output into the prompt as `{{search_results}}`.
- **System prompt:**
  ```
  You are a B2B research assistant. Given a lead's company name, domain, and any
  message they submitted, produce a concise research summary: likely industry,
  approximate size (small/medium/large, inferred from domain/context), and anything
  notable. If information is insufficient, say so plainly rather than inventing
  detail. 2-3 sentences max.
  ```
- **User prompt:** `Company: {{1.company}}\nEmail domain: {{1.email}}\nMessage: {{1.message}}`
- **Output mapped to:** `Company Research` (used in Module 4)

## Module 3 — OpenAI (ChatGPT) › Create a Chat Completion (Score + Pain Points)

- **Model:** `gpt-4o-mini` or equivalent
- **System prompt:**
  ```
  You are a lead qualification assistant. Given a lead's submitted message and company
  research, output JSON only, no prose, no code fences:
  {
    "pain_points": "<1-2 sentences on their likely pain point, grounded in what they
      actually said - do not invent specifics they didn't mention>",
    "score": <integer 0-100, fit + intent>,
    "score_reasoning": "<one sentence>"
  }
  Score guidance: 80-100 = explicit need stated + clear ICP fit; 50-79 = plausible fit,
  vague intent; below 50 = poor fit or too little information to tell.
  ```
- **User prompt:** `Message: {{1.message}}\nCompany research: {{2.output}}`
- **Parse the JSON response** with a **JSON › Parse JSON** module immediately after,
  so `pain_points` and `score` are usable as separate fields downstream.

## Module 4 — Notion › Create a Database Item

- **Database:** CRM (Leads)
- **Field mapping:**

| Notion property | Value |
|---|---|
| Name | `{{1.name}}` |
| Company | `{{1.company}}` |
| Email | `{{1.email}}` |
| Phone | `{{1.phone}}` |
| Source | `{{1.source}}` (must match one of: Cold Outbound / Inbound Form / Referral / Event / Other) |
| Pain Points | `{{3.pain_points}}` |
| Company Research | `{{2.output}}` |
| Lead Score | `{{3.score}}` |
| Status | `New` |
| Date Captured | `{{now}}` |

## Module 5 — Router (score gate)

Add a **Router** after Module 4 with two routes:

- **Route A filter:** `{{3.score}} >= 70`
- **Route B filter:** `{{3.score}} < 70`

## Module 6a / 6b — Slack › Create a Message

- **6a (Route A, #hot-leads):**
  ```
  🔥 High-score lead: {{1.name}} @ {{1.company}} (score: {{3.score}})
  {{3.pain_points}}
  <Notion CRM row link>
  ```
- **6b (Route B, #new-leads):**
  ```
  New lead: {{1.name}} @ {{1.company}} (score: {{3.score}})
  <Notion CRM row link>
  ```
- Getting the Notion row's URL into the Slack message: the Notion "Create a Database
  Item" module's output includes the new page's URL — map it in directly as
  `{{4.url}}` (exact output field name may read `id` or `url` depending on Make's
  Notion app version; check the module's output bundle after a test run).

## Timing note

Modules 2 and 3 (two sequential OpenAI calls) are the only latency in this chain —
budget ~5-15 seconds combined with `gpt-4o-mini`-class models, well inside the
"under 60 seconds" target as long as you're not adding a slow search-API step in
front of Module 2.

## Testing checklist

- [ ] Send a test payload to the webhook URL (curl or Postman) and confirm Module 1 fires
- [ ] Confirm Module 3's JSON output parses cleanly — malformed JSON from the model is
      the most common break point; add a **Filter** after the parse step that routes
      to an error-notification Slack message if parsing fails
- [ ] Confirm the new CRM row appears with all 5 AI-populated fields filled in
- [ ] Confirm both Slack routes fire correctly by testing a high-score and low-score payload

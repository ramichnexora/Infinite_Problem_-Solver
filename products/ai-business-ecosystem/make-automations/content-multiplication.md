# Content Multiplication Engine — Make.com Build Spec

**What it does:** approve one draft in the Content Calendar, get LinkedIn/X/Facebook
versions generated automatically and logged as linked variants. Like the lead
automation, this is a module-by-module spec, not an importable blueprint — see the
product README for why.

Target: the **Content Calendar** Notion database, schema in
`products/ai-business-ecosystem/notion-workspace.md`. Every row with
`Platform = Original Draft` is a source post; this automation creates 3 new rows
(`Platform = LinkedIn / X / Facebook`) linked back to it via the `Source Post` ↔
`Platform Variants` two-way relation.

## Scenario overview

```
[1] Notion: Watch Database Items (Content Calendar, filtered)
    → [2] Router (3 branches: LinkedIn / X / Facebook)
        → [2a/b/c] OpenAI: Create a Chat Completion (platform rewrite)
        → [3a/b/c] Notion: Create a Database Item (variant row, linked to source)
```

## Module 1 — Notion › Watch Database Items

- **Database:** Content Calendar
- **Filter:** `Platform = Original Draft` AND `Status = Approved`
- This is the trigger: a draft only fires the automation once you flip its Status to
  Approved in Notion — that's the "one approval click" from the sales page.
- **Watch for:** updated items (not just new ones), since a draft is created first as
  `Status = Draft` and only becomes `Approved` in a later edit.

## Module 2 — Router (3 branches)

No filter needed on the branches themselves — all three run for every approved draft.
Each branch does its own platform-specific rewrite in parallel.

## Modules 2a/2b/2c — OpenAI (ChatGPT) › Create a Chat Completion

One per platform, same structure, different system prompt:

**LinkedIn branch:**
```
Rewrite the following draft as a LinkedIn post. Rules: hook in the first line (shows
before "see more"), short paragraphs (1-2 sentences), no hashtag spam (0-3 relevant
tags max at the end), professional but conversational tone, 150-300 words.
Draft: {{1.Body}}
```

**X (Twitter) branch:**
```
Rewrite the following draft as a single X post. Rules: under 280 characters, punchy,
no more than 1 hashtag, get to the point immediately - no throat-clearing intro.
Draft: {{1.Body}}
```

**Facebook branch:**
```
Rewrite the following draft as a Facebook post. Rules: warmer/more casual tone than
LinkedIn, can be slightly longer (up to 400 words), fine to ask a question at the end
to invite comments.
Draft: {{1.Body}}
```

## Modules 3a/3b/3c — Notion › Create a Database Item

One per branch, same field mapping pattern:

| Notion property | Value |
|---|---|
| Name | `{{1.Name}} — LinkedIn` (or `— X`, `— Facebook`, matching the branch) |
| Platform | `LinkedIn` / `X` / `Facebook` (matching the branch) |
| Status | `Draft` (starts as a draft variant awaiting its own scheduling approval — see note below) |
| Body | `{{2a.output}}` / `{{2b.output}}` / `{{2c.output}}` (the platform-rewritten text) |
| Source Post | `{{1.id}}` (relation field — link back to the original draft's page ID from Module 1) |

**On the `Status = Draft` choice for variants:** the sales page says "approve one post,
get all 3 versions generated and scheduled automatically." If you want variants to go
straight to `Scheduled` instead of `Draft`, change the mapping above and add a
**Publish Date** mapping (e.g. `{{1.Publish Date}}` inherited from the source, or
offset per platform with a **Tools › Set variable** date-math step) — the tradeoff is
you lose a manual review step per platform before it's slated to publish.

## Optional: auto-scheduling via Buffer

The sales page lists Buffer as optional. To wire actual scheduling once variants are
approved, add a fourth module per branch: **Buffer › Create a Post**, triggered off a
*second* Notion watch (`Platform != Original Draft` AND `Status = Scheduled`), mapping
`Body` → Buffer's post text and `Publish Date` → Buffer's scheduled time. This is a
second scenario, not part of the flow above — keep them separate so a Buffer outage
doesn't block content generation.

## Testing checklist

- [ ] Create a test row with `Platform = Original Draft`, `Status = Draft`, some body text
- [ ] Flip it to `Status = Approved` and confirm all 3 branches fire
- [ ] Confirm each variant row's `Source Post` relation actually links back (check the
      original draft's `Platform Variants` rollup shows all 3)
- [ ] Sanity-check each platform's output against its rules (X under 280 chars is the
      one most likely to need a retry/truncation step if the model runs long)

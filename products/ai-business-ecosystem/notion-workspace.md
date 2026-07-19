# Notion Workspace — Schema Reference

This documents the **live workspace** built via the Notion API into the connected
account, not a hypothetical spec. If you have access to that Notion account, the
actual workspace is here:

**Parent page:** [🧠 AI-Powered Automated Business Ecosystem](https://app.notion.com/p/3a2bf18f418381b6ab37faf770a59c52)

If you don't have access to that account, this doc is the exact schema to recreate it
manually, or hand to someone with Notion API access to rebuild via the same DDL shown
below.

## 1. CRM (Leads)

[Open database](https://app.notion.com/p/4e9360a0d2524826a6eaf82a5a6db037)

| Property | Type | Notes |
|---|---|---|
| Name | Title | Lead's name |
| Company | Text | |
| Email | Email | |
| Phone | Phone number | |
| Source | Select | Cold Outbound / Inbound Form / Referral / Event / Other |
| Pain Points | Text | AI-populated by the Lead Capture & Enrichment automation |
| Company Research | Text | AI-populated firmographic/company summary |
| Lead Score | Number | AI-populated 0-100 fit + intent score |
| Status | Select | New / Researching / Contacted / Qualified / Booked / Won / Lost |
| Date Captured | Date | |
| Next Follow-up | Date | |
| Owner | Person | |

**View:** Pipeline Board, grouped by Status.

Two-way relations out of this database: `Projects` (→ Project Tracker) and `Invoices`
(→ Financials Dashboard) were added automatically when those databases' `Client`
relation fields were created — you'll see them on CRM rows once a related Project or
Financials row exists.

## 2. Project Tracker

[Open database](https://app.notion.com/p/9bdf4ea1cbe341728427ee8a76aec9d0)

| Property | Type | Notes |
|---|---|---|
| Name | Title | |
| Client | Relation → CRM (Leads) | Two-way |
| Status | Select | Not Started / In Progress / Blocked / Complete |
| Health | Formula | Auto-flags: 🔴 Overdue (past Due Date, not Complete), 🟡 Due Soon (≤3 days out), 🟢 On Track, ✅ Done |
| Start Date | Date | |
| Due Date | Date | |
| Owner | Person | |
| Notes | Text | |

**View:** Timeline, by Start Date → Due Date.

**Health formula (Notion formula 2.0 syntax):**
```
if(prop("Status") == "Complete", "✅ Done",
  if(prop("Due Date") < now(), "🔴 Overdue",
    if(dateBetween(prop("Due Date"), now(), "days") <= 3, "🟡 Due Soon", "🟢 On Track")))
```

## 3. Content Calendar

[Open database](https://app.notion.com/p/6d74259a28214e8aacd185854b92beaf)

| Property | Type | Notes |
|---|---|---|
| Name | Title | |
| Platform | Select | Original Draft / LinkedIn / X / Facebook |
| Status | Select | Draft / Approved / Scheduled / Published |
| Publish Date | Date | |
| Body | Text | |
| Source Post | Relation → self | Set on a variant row, points back to its original draft |
| Platform Variants | Relation → self | Synced back-reference; shows on the original draft, lists its generated variants |

**View:** Publish Calendar, by Publish Date.

**How the self-relation works:** every row is either `Platform = Original Draft` (a
source post) or one of the 3 platform variants. A variant's `Source Post` field points
at its original; Notion auto-populates the original's `Platform Variants` field with
the reverse links. The Content Multiplication automation
(`products/ai-business-ecosystem/make-automations/content-multiplication.md`) is what
creates the variant rows and sets this relation.

## 4. Financials Dashboard

[Open database](https://app.notion.com/p/284fcd70cf0a4429b52fa5c0fa597a9e)

| Property | Type | Notes |
|---|---|---|
| Name | Title | e.g. an invoice or expense description |
| Client | Relation → CRM (Leads) | Two-way |
| Type | Select | Revenue / Expense |
| Amount | Number (dollar format) | |
| Status | Select | Draft / Sent / Paid / Overdue |
| Invoice Date | Date | |
| Paid Date | Date | |

**View:** "Revenue This Month" — a chart view filtered to `Type = Revenue` and
`Status = Paid`, aggregating `Amount` (sum). This is the closest live equivalent to
the sales page's "progress bar toward your monthly revenue goal" — Notion doesn't have
a native goal-vs-actual progress bar property, so the chart view shows actual revenue
collected; if you want an explicit goal line, add a `Number` property for "Monthly
Goal" on a single settings row and compare manually, or track the goal outside Notion
and just use this view for the "actual" side.

## Known follow-up: named views

The 4 databases and all fields/relations/formulas above are live. The named views
described per-database (Pipeline Board, Timeline, Publish Calendar, Revenue This
Month) were **not** successfully created via the API in this session — attempts hit a
transient tool-infrastructure error, not a Notion API error, so it's worth retrying
via API later. In the meantime it's a 30-second manual step per database: open it,
click **+ Add view**, and use the type/filter described in that database's section
above.

## Rebuilding this from scratch

Every schema above was created via the Notion API using SQL-DDL-style `CREATE TABLE`
statements (through the Notion MCP server's `create-database` tool). If you have API
access and want to recreate this in a different workspace, the DDL for each database
is reconstructable directly from the property tables above — type mapping: Title →
`TITLE`, Text → `RICH_TEXT`, Select → `SELECT('opt':color, ...)`, Relation →
`RELATION('<data_source_id>', DUAL 'reverse_name')`, Number (dollar) →
`NUMBER FORMAT 'dollar'`, Formula → `FORMULA('<expression>')`.

# Playbook: Product — deciding what to build next

Promoted from the delivered Shopify AI Operating System artifact. Owning
seat: `product_research` (`agents/product_research_agent.py`,
`docs/roles/ai-product-research.md`).

## Objective
Turn DM/review/support signal into a ranked, low-overlap list of what the
next guide should be.

## Trigger
Monthly, or when a recurring request pattern shows up in support/sales logs.

## Inputs
Current 20-guide catalog, candidate topics from DMs/reviews/support tickets.

## Preconditions
`master-prompt.md` loaded.

## Step-by-step process
1. **Next-guide opportunity ranking** — Role: product strategist. Context:
   current catalog + candidate topics. Command: rank by demand signal,
   overlap risk with existing catalog, effort to produce; flag any real gap.
   Format: table (Idea, Demand signal, Overlap risk, Effort, Verdict).
2. **One-page guide spec** — Role: product manager. Context: problem, buyer,
   price point. Command: one-page spec — contents, explicit non-goals,
   single success outcome.
3. **Voice-of-customer digest** — Role: insights analyst. Context: reviews/
   tickets/DMs. Command: top 5 recurring themes with real quotes + a
   product action per theme. Format: table (Theme, Quote, Source, Action).

## Tools
`product_research` agent seat; `data/*.sample.json` fixtures as reference
shape for ticket/lead data until real sources are wired.

## Quality standards
No candidate ranked without a demand signal traceable to a real
DM/review/ticket — no guessing.

## Decision rules
A new guide only greenlights (Tier 3, founder sign-off) once ranked above
the current lowest-selling guide's demand signal.

## Failure handling
If signal is too thin to rank confidently, escalate as "insufficient data"
rather than forcing a ranking.

## Definition of Done
A ranked table exists and the founder has signed off on the next guide to
build (Tier 3).

## Output format
Per prompt above — tables and one-page specs.

---
**Owner (human):** founder (Product Leader)
**Version:** v1 — promoted from Shopify AI OS artifact
**Status:** active

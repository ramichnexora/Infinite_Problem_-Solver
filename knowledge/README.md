# Knowledge

Curated reference knowledge agents/playbooks draw on. `data/knowledge_base.md`
(existing, untouched) remains the seed support-KB fixture the support agent's
tests run against — this folder is where the knowledge base grows past that
one sample file as the system matures (e.g. per-guide FAQ, objection library,
product-catalog notes) without disturbing the existing test fixture.

## Index

| File | What it is | Used by |
| --- | --- | --- |
| `ai-replacement-ladder.md` | Condensed Replacement Ladder (Admin → Delivery → Marketing → Sales → Leadership) | org chart, `.claude/agents/` leads |
| `dan-martell-ai-company-operating-system.md` | Full source playbook: Buyback Loop, Ladder, 4-Part Deployment, Master Prompt, RCCF, department prompt library | every `.claude/agents/*` RCCF prompt; `/deploy-department`, `/calendar-audit` |
| `claude-code-agentic-workflows.md` | Building agents with Claude Code: `claude.md`, plan mode, workflow files, 5 mistakes | `CLAUDE.md`, `.claude/agents/`, `automation/` |
| `prompt-engineering-mastery-bn.md` | Prompt Engineering Mastery, ch. 2 (Bengali/English): 8 techniques, Mega Prompt framework, 50+ examples | writing/optimising system prompts in `agents/*.py` |
| `agi-era-marketing-guide-bn.md` | Preparing marketing for the AGI era (Bengali): what dies, what survives, how to stay ahead | `cmo`, `product-strategist`, `docs/DISTRIBUTION_PLAN.md` |

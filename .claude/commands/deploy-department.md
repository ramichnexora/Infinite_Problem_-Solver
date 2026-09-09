---
name: deploy-department
description: Run the 4-Part AI Deployment Playbook against one department. Usage: /deploy-department <dept>
---

Takes one argument: a department id (`cmo`, `cro`, `coo`, `cpo`, `cto`,
`cfo`, or `chief-ai`).

## The 4-Part AI Deployment Playbook

1. **Map** — list every recurring task this department actually does today
   (ask the founder if it isn't already documented as an SOP).
2. **SOP-ify** — for each task without a written SOP, write one before
   automating it (per `docs/01-principles.md` #2 — write the SOP before you
   automate it).
3. **Assign** — match each SOP to the existing sub-agent that should own it,
   or flag a genuine gap (a new sub-agent is only justified if the task is
   recurring, specialization materially improves quality, and delegation
   saves real time — per `docs/01-principles.md` #8, same bar the Python
   MILI seats use).
4. **Verify** — for each newly assigned sub-agent, run one real task through
   it and have the founder review the output before it runs unsupervised.

Report back: what's now covered, what's still a gap, and exactly what the
founder needs to decide or approve to close that gap.

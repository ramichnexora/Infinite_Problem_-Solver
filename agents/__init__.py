"""AI Company OS agent runtime.

Implements the seat model documented under docs/roles/: every agent runs
named SOPs, every action is logged to an audit trail, and anything that
doesn't clear the seat's autonomy tier lands in the escalation queue for a
human instead of executing. See docs/03-governance-and-escalation.md.
"""

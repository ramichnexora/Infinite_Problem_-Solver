"""Channels that connect an AI seat to a real external surface.

Each integration is a thin adapter: it turns an inbound message from some
platform into the input shape an agent's SOP expects, and turns the
AgentResult back into whatever that platform needs (a reply, a
notification, etc). The governance logic itself - guardrails, confidence
gate, audit log, escalation queue - all stays in agents/, not here.
"""

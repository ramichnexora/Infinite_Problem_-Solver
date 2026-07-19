from __future__ import annotations

import json
from typing import Any, Callable, Union

import pytest

from agents.audit import AuditLog
from agents.escalation import EscalationQueue


class FakeLLMClient:
    """Test double for LLMClient.

    Pass a single dict (always returned, JSON-encoded), a list of dicts
    (returned in call order), or a callable(system, user) -> dict for
    scenarios where the response depends on the prompt.
    """

    def __init__(
        self,
        responses: Union[dict, list[dict], Callable[[str, str], dict]],
    ):
        self._responses = responses
        self._index = 0
        self.calls: list[dict[str, str]] = []

    def complete(self, *, system: str, user: str) -> str:
        self.calls.append({"system": system, "user": user})
        if callable(self._responses):
            payload = self._responses(system, user)
        elif isinstance(self._responses, list):
            payload = self._responses[self._index]
            self._index += 1
        else:
            payload = self._responses
        return json.dumps(payload)


class ExplodingLLMClient:
    """Raises if called - used to prove a hard-guardrail path never reaches the model."""

    def complete(self, *, system: str, user: str) -> str:
        raise AssertionError("LLM should not have been called - a hard guardrail should have short-circuited")


@pytest.fixture
def audit_log(tmp_path) -> AuditLog:
    return AuditLog(tmp_path / "audit.jsonl")


@pytest.fixture
def escalation_queue(tmp_path) -> EscalationQueue:
    return EscalationQueue(tmp_path / "escalations.jsonl")

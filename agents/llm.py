"""LLM client used by every agent.

Kept as a small Protocol so tests can swap in a FakeLLMClient without
needing an API key or network access - see tests/conftest.py.
"""
from __future__ import annotations

import json
import os
import re
from typing import Protocol

DEFAULT_MODEL = "claude-sonnet-5"


class LLMClient(Protocol):
    def complete(self, *, system: str, user: str) -> str:
        """Return the model's raw text response for a single-turn request."""
        ...


class AnthropicLLMClient:
    """Thin wrapper around the Anthropic Messages API."""

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 1024):
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover - exercised only without the dep installed
            raise RuntimeError(
                "The 'anthropic' package is required to run agents against a real "
                "model. Install it with `pip install -r requirements.txt`, or pass "
                "a different LLMClient (e.g. FakeLLMClient) for testing."
            ) from exc

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Export it before running agents "
                "against a real model - see docs/07-running-the-agents.md."
            )

        self._client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

    def complete(self, *, system: str, user: str) -> str:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in response.content if block.type == "text")


def build_llm_client(model: str = DEFAULT_MODEL, max_tokens: int = 1024) -> LLMClient:
    """Return a real Anthropic client when it can be built, otherwise a
    HandoffLLMClient so the agent hands the job off instead of crashing.

    The fallback is announced on stderr once so an operator never mistakes a
    hand-off run for a live one.
    """
    import sys

    from .handoff import HandoffLLMClient

    try:
        return AnthropicLLMClient(model=model, max_tokens=max_tokens)
    except RuntimeError as exc:
        print(f"[fallback] {exc} -> jobs will be written to tasks/inbox/", file=sys.stderr)
        return HandoffLLMClient(cause=str(exc))


_JSON_FENCE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def parse_json_response(text: str) -> dict:
    """Parse a model response that should be JSON, tolerating ```json fences."""
    fenced = _JSON_FENCE.search(text)
    candidate = fenced.group(1) if fenced else text
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model response was not valid JSON: {text!r}") from exc

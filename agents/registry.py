"""Agent registry: reads config/agents.yaml so MILI (and anything else) can
look up "which agent owns this seat" without hardcoding names.

This is the scaling mechanism referenced in the MILI architecture proposal —
going from 8 agents to 60+ means adding entries to config/agents.yaml plus one
new agent module, never editing this file or base.py.

Does not import or modify any existing agents/*.py file.
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError as exc:  # pragma: no cover - surfaced clearly at call time
    raise ImportError(
        "agents/registry.py requires PyYAML. Add `pyyaml` to requirements.txt."
    ) from exc

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "agents.yaml"


@dataclass
class AgentSpec:
    id: str
    module: str
    class_name: str
    parent: Optional[str]
    status: str
    docs: Optional[str]
    default_tier: int = 2

    @property
    def is_active(self) -> bool:
        return self.status == "active"


class AgentRegistry:
    """Loads config/agents.yaml and resolves agent ids to importable classes."""

    def __init__(self, config_path: str | Path = DEFAULT_CONFIG_PATH):
        self.config_path = Path(config_path)
        self._raw: dict[str, Any] = {}
        self._specs: dict[str, AgentSpec] = {}
        self._orchestrator: Optional[AgentSpec] = None
        self._load()

    def _load(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Agent registry config not found: {self.config_path}")
        with self.config_path.open(encoding="utf-8") as f:
            self._raw = yaml.safe_load(f) or {}

        orch = self._raw.get("orchestrator")
        if orch:
            self._orchestrator = AgentSpec(
                id=orch["id"],
                module=orch["module"],
                class_name=orch["class"],
                parent=orch.get("parent"),
                status=orch.get("status", "active"),
                docs=orch.get("docs"),
            )

        for entry in self._raw.get("agents", []) or []:
            spec = AgentSpec(
                id=entry["id"],
                module=entry["module"],
                class_name=entry["class"],
                parent=entry.get("parent"),
                status=entry.get("status", "draft"),
                docs=entry.get("docs"),
                default_tier=int(entry.get("default_tier", 2)),
            )
            self._specs[spec.id] = spec

    def orchestrator(self) -> Optional[AgentSpec]:
        return self._orchestrator

    def get(self, agent_id: str) -> AgentSpec:
        if agent_id not in self._specs:
            raise KeyError(f"No agent registered with id={agent_id!r}")
        return self._specs[agent_id]

    def active_agents(self) -> list[AgentSpec]:
        return [s for s in self._specs.values() if s.is_active]

    def all_agents(self) -> list[AgentSpec]:
        return list(self._specs.values())

    def resolve_class(self, agent_id: str) -> type:
        """Import and return the concrete Agent subclass for this id."""
        spec = self.get(agent_id)
        module = importlib.import_module(spec.module)
        return getattr(module, spec.class_name)

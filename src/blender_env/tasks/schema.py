"""Task specification schema for task factories and evaluators."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    category: str
    instruction: str
    seed: int
    hidden_spec: Mapping[str, Any] = field(default_factory=dict)
    evaluator_config: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

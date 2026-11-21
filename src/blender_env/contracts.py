"""Trainer-agnostic domain contracts.

These are internal starting types, not the exact OpenEnv SDK API. The SDK
adapter will translate between SDK messages and these objects once a version
is selected and verified.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True)
class Action:
    name: str
    parameters: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Observation:
    task_id: str
    step_index: int
    scene: Mapping[str, Any]
    diagnostics: Mapping[str, Any] = field(default_factory=dict)
    render_refs: tuple[str, ...] = ()

@dataclass(frozen=True)
class RewardBreakdown:
    total: float
    components: Mapping[str, float]
    valid: bool
    evaluator_version: str
    terminal: bool = False

@dataclass(frozen=True)
class StepResult:
    observation: Observation
    reward: RewardBreakdown
    terminated: bool
    truncated: bool = False
    info: Mapping[str, Any] = field(default_factory=dict)

"""Evaluator interface; concrete Blender-backed metrics come next."""

from __future__ import annotations
from typing import Any, Protocol
from blender_env.contracts import RewardBreakdown

class Evaluator(Protocol):
    version: str
    def evaluate(self, *, task_spec: dict[str, Any], artifact: dict[str, Any], terminal: bool) -> RewardBreakdown:
        """Return a transparent reward breakdown."""
        ...

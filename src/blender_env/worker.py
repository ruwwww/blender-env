"""Blender worker boundary (implementation pending).

Blender should run in an isolated process/container. Never execute arbitrary
agent Python in the API process. The worker needs bounded requests, timeouts,
resource limits, and per-episode workspaces.
"""

from __future__ import annotations
from typing import Any, Protocol

class BlenderWorker(Protocol):
    def start(self) -> None: ...
    def reset(self, *, seed: int, workspace: str) -> dict[str, Any]: ...
    def execute(self, *, action: dict[str, Any], timeout_s: float) -> dict[str, Any]: ...
    def close(self) -> None: ...

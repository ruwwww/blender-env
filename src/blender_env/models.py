"""OpenEnv wire models."""
from typing import Any
from pydantic import Field
from openenv.core.env_server.types import Action, Observation, State


class BlenderAction(Action):
    """Allowlisted modeling action; arbitrary code is never accepted."""
    op: str = Field(description="create_cube, set_dimensions, bevel, or finish")
    dimensions: list[float] | None = Field(default=None, min_length=3, max_length=3)
    width: float | None = Field(default=None, gt=0, le=0.25)


class BlenderObservation(Observation):
    task_id: str = ""
    step_index: int = 0
    instruction: str = ""
    target_dimensions: list[float] = Field(default_factory=list)
    scene: dict[str, Any] = Field(default_factory=dict)
    diagnostics: dict[str, Any] = Field(default_factory=dict)
    terminal_metrics: dict[str, Any] = Field(default_factory=dict)


class BlenderState(State):
    task_id: str | None = None
    seed: int | None = None
    step_index: int = 0
    done: bool = False
    workspace: str | None = None
    task_spec: dict[str, Any] = Field(default_factory=dict)

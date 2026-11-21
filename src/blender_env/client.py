"""Typed OpenEnv client."""
from typing import Any
from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from blender_env.models import BlenderAction, BlenderObservation, BlenderState


class BlenderEnvClient(EnvClient[BlenderAction, BlenderObservation, BlenderState]):
    def _step_payload(self, action: BlenderAction) -> dict[str, Any]:
        return action.model_dump(exclude={"metadata"})

    def _parse_result(self, payload: dict[str, Any]) -> StepResult[BlenderObservation]:
        obs = BlenderObservation(**payload.get("observation", {}))
        return StepResult(observation=obs, reward=payload.get("reward"),
                          done=payload.get("done", False), metadata=payload.get("metadata"))

    def _parse_state(self, payload: dict[str, Any]) -> BlenderState:
        return BlenderState(**payload)

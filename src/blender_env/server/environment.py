"""OpenEnv environment for a single-object cube dimension task."""
from __future__ import annotations
import json, os, random, uuid
from pathlib import Path
from typing import Any
from openenv.core.env_server.interfaces import Environment
from blender_env.models import BlenderAction, BlenderObservation, BlenderState
from blender_env.worker import BlenderSubprocessWorker, Worker
from blender_env.evaluation.geometry import evaluate_cube

MAX_STEPS = 12
ALLOWED_OPS = {"create_cube", "set_dimensions", "bevel", "finish"}


class BlenderEnvironment(Environment[BlenderAction, BlenderObservation, BlenderState]):
    SUPPORTS_CONCURRENT_SESSIONS = False

    def __init__(self, worker: Worker | None = None, artifact_root: str | None = None):
        super().__init__()
        self.worker = worker or BlenderSubprocessWorker()
        self.artifact_root = Path(artifact_root or os.getenv("BLENDER_ENV_ARTIFACTS", "/tmp/blender-env"))
        self._state = BlenderState()
        self._artifact: dict[str, Any] = {"execution_ok": True, "objects": []}
        self._last_reward = 0.0
        self._metrics: dict[str, Any] = {}

    @property
    def state(self) -> BlenderState:
        return self._state

    def reset(self, seed: int | None = None, episode_id: str | None = None, **kwargs: Any) -> BlenderObservation:
        self.worker.close()
        seed = 0 if seed is None else int(seed)
        rng = random.Random(seed)
        target = [round(rng.uniform(0.8, 2.5), 2) for _ in range(3)]
        task_id = episode_id or f"cube-{uuid.uuid4().hex[:10]}"
        workspace = self.artifact_root / task_id
        workspace.mkdir(parents=True, exist_ok=True)
        self._state = BlenderState(task_id=task_id, seed=seed, step_count=0, step_index=0,
                                   done=False, workspace=str(workspace),
                                   task_spec={"target_dimensions": target})
        self._artifact = self.worker.reset(seed, str(workspace))
        self._last_reward, self._metrics = 0.0, {}
        return self._observation()

    def _observation(self, diagnostics: dict[str, Any] | None = None) -> BlenderObservation:
        target = self._state.task_spec.get("target_dimensions", [])
        return BlenderObservation(
            task_id=self._state.task_id or "", step_index=self._state.step_index,
            instruction=f"Create exactly one cube and set its dimensions to {target} Blender units. Optionally bevel it, then submit with finish.",
            target_dimensions=target, scene=self._artifact, diagnostics=diagnostics or {},
            terminal_metrics=self._metrics, done=self._state.done,
            reward=self._last_reward if self._state.done else None,
            metadata={"evaluator_version": "cube-dimensions-v1", "max_steps": MAX_STEPS},
        )

    def step(self, action: BlenderAction, timeout_s: float | None = None, **kwargs: Any) -> BlenderObservation:
        if self._state.task_id is None:
            raise RuntimeError("Call reset() before step()")
        if self._state.done:
            raise RuntimeError("Episode is done; call reset()")
        if self._state.step_index >= MAX_STEPS:
            raise RuntimeError("Episode step limit reached; call reset()")
        if action.op not in ALLOWED_OPS:
            raise ValueError(f"Unsupported operation: {action.op}")
        payload: dict[str, Any] = {"op": action.op}
        if action.op == "set_dimensions":
            if action.dimensions is None or any(not 0.1 <= float(x) <= 10.0 for x in action.dimensions):
                raise ValueError("set_dimensions requires three values in [0.1, 10]")
            payload["dimensions"] = action.dimensions
        if action.op == "bevel":
            payload["width"] = action.width if action.width is not None else 0.05
        self._artifact = self.worker.execute(payload, timeout_s or 30.0)
        self._state.step_index += 1
        self._state.step_count = self._state.step_index
        if action.op == "finish" or self._state.step_index >= MAX_STEPS:
            self._metrics = evaluate_cube(self._state.task_spec, self._artifact)
            self._last_reward = float(self._metrics["reward"])
            self._state.done = True
            self._persist()
        return self._observation({"last_action": action.op})

    def _persist(self) -> None:
        if not self._state.workspace:
            return
        payload = {"task_id": self._state.task_id, "seed": self._state.seed,
                   "task_spec": self._state.task_spec, "artifact": self._artifact,
                   "reward": self._metrics, "steps": self._state.step_index}
        Path(self._state.workspace, "episode.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def close(self) -> None:
        self.worker.close()

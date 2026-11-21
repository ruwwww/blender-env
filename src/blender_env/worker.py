"""Blender subprocess boundary and deterministic test double."""
from __future__ import annotations
import json, os, shutil, subprocess
from pathlib import Path
from typing import Any, Protocol


class Worker(Protocol):
    def reset(self, seed: int, workspace: str) -> dict[str, Any]: ...
    def execute(self, action: dict[str, Any], timeout_s: float = 30.0) -> dict[str, Any]: ...
    def close(self) -> None: ...


class BlenderSubprocessWorker:
    """Launch one bounded Blender process per action; persist the .blend between steps."""
    def __init__(self, blender_bin: str | None = None, timeout_s: float = 30.0):
        self.blender_bin = blender_bin or os.getenv("BLENDER_BIN", "blender")
        self.timeout_s = timeout_s
        self.workspace: Path | None = None
        self.scene_path: Path | None = None

    def _run(self, request: dict[str, Any], timeout_s: float | None = None) -> dict[str, Any]:
        if not shutil.which(self.blender_bin):
            raise RuntimeError(f"Blender executable not found: {self.blender_bin}. Install Blender or set BLENDER_BIN.")
        assert self.workspace is not None and self.scene_path is not None
        req, res = self.workspace / "request.json", self.workspace / "response.json"
        req.write_text(json.dumps({**request, "scene_path": str(self.scene_path)}), encoding="utf-8")
        res.unlink(missing_ok=True)
        script = Path(__file__).with_name("blender_worker.py")
        cmd = [self.blender_bin, "--background"]
        if self.scene_path.exists() and request["op"] != "reset":
            cmd.append(str(self.scene_path))
        cmd += ["--python", str(script), "--", str(req), str(res)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s or self.timeout_s,
                                  cwd=self.workspace)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"Blender timed out after {exc.timeout}s") from exc
        if proc.returncode or not res.exists():
            raise RuntimeError(f"Blender worker failed (exit={proc.returncode}): {(proc.stderr or proc.stdout)[-3000:]}")
        return json.loads(res.read_text(encoding="utf-8"))

    def reset(self, seed: int, workspace: str) -> dict[str, Any]:
        self.close()
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.scene_path = self.workspace / "scene.blend"
        return self._run({"op": "reset", "seed": seed})

    def execute(self, action: dict[str, Any], timeout_s: float = 30.0) -> dict[str, Any]:
        if self.workspace is None:
            raise RuntimeError("Worker has not been reset")
        return self._run(action, timeout_s)

    def close(self) -> None:
        self.workspace = self.scene_path = None


class InMemoryWorker:
    """Fast protocol test backend; it does not test Blender behavior."""
    def __init__(self):
        self.objects: list[dict[str, Any]] = []

    def reset(self, seed: int, workspace: str) -> dict[str, Any]:
        self.objects = []
        return self.inspect()

    def execute(self, action: dict[str, Any], timeout_s: float = 30.0) -> dict[str, Any]:
        op = action["op"]
        if op == "create_cube":
            if self.objects:
                raise ValueError("Only one object is allowed")
            self.objects = [{"name": "Cube", "dimensions": [2.0, 2.0, 2.0], "vertex_count": 8}]
        elif op == "set_dimensions":
            if not self.objects:
                raise ValueError("Create the cube first")
            self.objects[0]["dimensions"] = list(action["dimensions"])
        elif op == "bevel" and not self.objects:
            raise ValueError("Create the cube first")
        elif op not in {"bevel", "finish"}:
            raise ValueError(f"Unsupported operation: {op}")
        return self.inspect()

    def inspect(self) -> dict[str, Any]:
        return {"execution_ok": True, "objects": [dict(x) for x in self.objects]}

    def close(self) -> None:
        pass

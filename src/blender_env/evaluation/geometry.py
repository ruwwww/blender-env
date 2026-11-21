"""Deterministic, task-specific terminal reward."""
from __future__ import annotations
import math
from typing import Any

EVALUATOR_VERSION = "cube-dimensions-v1"


def evaluate_cube(task: dict[str, Any], artifact: dict[str, Any]) -> dict[str, Any]:
    target = [float(x) for x in task["target_dimensions"]]
    objects = artifact.get("objects", [])
    reasons: list[str] = []
    if artifact.get("execution_ok") is not True:
        reasons.append("blender_execution_failed")
    if len(objects) != 1:
        reasons.append("expected_exactly_one_object")
    obj = objects[0] if len(objects) == 1 else {}
    actual = obj.get("dimensions", [])
    if len(actual) != 3 or any(not math.isfinite(float(x)) or float(x) <= 0 for x in actual):
        reasons.append("invalid_dimensions")
    if int(obj.get("vertex_count", 0)) < 8:
        reasons.append("mesh_missing_or_invalid")
    if reasons:
        return {"reward": 0.0, "valid": False, "evaluator_version": EVALUATOR_VERSION,
                "components": {"validity": 0.0, "dimension_match": 0.0},
                "metrics": {"target_dimensions": target, "actual_dimensions": actual},
                "failure_reasons": reasons}
    errors = [abs(math.log(float(a) / t)) for a, t in zip(actual, target)]
    match = math.exp(-sum(errors) / 3.0)
    reward = 0.2 + 0.8 * match
    return {"reward": round(max(0.0, min(1.0, reward)), 6), "valid": True,
            "evaluator_version": EVALUATOR_VERSION,
            "components": {"validity": 1.0, "dimension_match": round(match, 6)},
            "metrics": {"target_dimensions": target,
                        "actual_dimensions": [round(float(x), 6) for x in actual],
                        "mean_log_dimension_error": round(sum(errors) / 3.0, 6),
                        "vertex_count": int(obj["vertex_count"])},
            "failure_reasons": []}

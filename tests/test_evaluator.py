from blender_env.evaluation.geometry import evaluate_cube


def test_exact_dimensions_score_one():
    task = {"target_dimensions": [2.0, 1.0, 1.5]}
    artifact = {"execution_ok": True, "objects": [
        {"name": "Cube", "dimensions": [2.0, 1.0, 1.5], "vertex_count": 8}]}
    result = evaluate_cube(task, artifact)
    assert result["valid"] is True
    assert result["reward"] == 1.0


def test_invalid_mesh_hard_gated():
    result = evaluate_cube({"target_dimensions": [2, 1, 1.5]},
                           {"execution_ok": True, "objects": []})
    assert result["valid"] is False
    assert result["reward"] == 0.0


def test_reward_decreases_with_dimension_error():
    task = {"target_dimensions": [2.0, 1.0, 1.5]}
    good = {"execution_ok": True, "objects": [{"dimensions": [2, 1, 1.5], "vertex_count": 8}]}
    bad = {"execution_ok": True, "objects": [{"dimensions": [4, 1, 1.5], "vertex_count": 8}]}
    assert evaluate_cube(task, good)["reward"] > evaluate_cube(task, bad)["reward"]

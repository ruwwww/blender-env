# Evaluating BlenderEnv

## Task: cube dimensions

Reset samples three target dimensions from a deterministic seed. The diagnostic observation exposes the target directly. The agent should:
1. Call `create_cube`.
2. Call `set_dimensions` using the three target dimensions.
3. Optionally call `bevel`.
4. Call `finish`.

This deliberately isolates tool use and geometry control. It does **not** test instruction inference.

The evaluator checks successful Blender execution, exactly one mesh object, finite positive dimensions, and at least eight vertices. Invalid artifacts receive reward 0. For valid artifacts:

```
dimension_match = exp(-mean(abs(log(actual_i / target_i))))
reward = 0.2 + 0.8 * dimension_match
```

Exact matches score 1.0. Reward is terminal-only; no tool-call or render-frequency bonuses exist.

## Commands

```bash
pip install -e '.[dev]'
pytest -q
python scripts/evaluate_local.py --seed 42
```

The real run writes `episode.json` and `scene.blend` under `/tmp/blender-env/<episode-id>/`.

## Limitations

The in-memory worker tests orchestration and reward logic, not Blender fidelity. The initial evaluator does not assess aesthetics, topology beyond a minimum vertex count, semantic resemblance, UVs, materials, lighting, or render quality. Treat v0.2 as an integration benchmark, not a general 3D modeling benchmark.

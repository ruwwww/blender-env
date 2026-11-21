# BlenderEnv

An OpenEnv environment for training LLM agents to create and refine 3D assets in Blender.

**Current milestone: runnable v0.2 vertical slice.** One dimension-matched cube task, allowlisted actions, a headless Blender subprocess worker, deterministic terminal reward, episode artifact logging, typed OpenEnv server/client, and unit tests.

## Quick start

Requirements: Python 3.11+, Blender 3.6+ on PATH.

```bash
pip install -e '.[dev]'
pytest -q
python scripts/evaluate_local.py --seed 42
```

Start the OpenEnv server:

```bash
blender-env-server --host 127.0.0.1 --port 8000
```

Docker:

```bash
docker build -f server/Dockerfile -t blender-env:local .
docker run --rm -p 8000:8000 -v "$PWD/artifacts:/tmp/blender-env" blender-env:local
```

See [docs/runbook.md](docs/runbook.md) and [docs/evaluation.md](docs/evaluation.md).

## Task and actions

Reset samples three target dimensions from a deterministic seed. The diagnostic observation exposes the target dimensions directly. Supported actions:

- `create_cube`
- `set_dimensions` with three positive dimensions
- `bevel` with a bounded width
- `finish` to submit the artifact

No arbitrary Python or shell execution is exposed to the agent.

## Reward

Terminal-only deterministic reward:
- Hard validity gate: Blender execution, exactly one mesh, finite positive dimensions, minimum mesh vertex count.
- Geometry match: exponential mean absolute log-ratio error on dimensions.
- Valid reward: `0.2 + 0.8 * dimension_match`.
- Invalid reward: `0.0`.

Evaluator version, raw metrics, failure reasons, scene snapshot, and seed are saved in `episode.json`.

**Important:** this task isolates tool-use and geometry control; because target dimensions are visible, it does not test instruction inference or general 3D modeling ability.

## Architecture

```text
OpenEnv client / trainer
        |
OpenEnv FastAPI server
        |
BlenderEnvironment (single session)
        |
allowlisted action validation
        |
Blender subprocess (one process per action)
        |
.blend + structured scene snapshot
        |
deterministic evaluator + episode.json
```

## Status

Implemented: reproducible task, action schema, Blender subprocess boundary, terminal evaluator, in-memory test double, OpenEnv adapter, Docker packaging, local evaluation script.

Not yet implemented: multi-object tasks, reference-image evaluation, VLM/human preference models, large task factories, trajectory database, parallel worker scheduler, and verl/GRPO integration. Do not start large-scale RL until the real Blender episode and reward validity have been checked.

## Design document

See the [BlenderEnv Master Technical Design](https://app.notion.com/p/41f230c18601815483adc39f23231faf).

## License

No license has been selected. This repository is public, but reuse is not licensed; all rights are reserved by default.

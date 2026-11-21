# Architecture

The OpenEnv SDK's Pydantic models and Environment base class form the wire boundary. Task/evaluator logic remains trainer-independent.

- `models.py`: OpenEnv Action, Observation, State.
- `server/environment.py`: reset/step/state lifecycle and terminal reward.
- `worker.py`: Blender subprocess boundary and in-memory test double.
- `blender_worker.py`: script executed by Blender's embedded Python.
- `evaluation/geometry.py`: validity gates and deterministic dimension score.
- `client.py`: typed EnvClient adapter.
- `server/app.py`: OpenEnv FastAPI application.

One worker process is launched per action; the saved .blend file carries scene state between actions. The server currently allows one active session until concurrency isolation is stress-tested.

## Security

Only four allowlisted operations reach Blender. Agent-provided Python is never executed. Each Blender call has a timeout and communicates through JSON in an episode workspace. Production hardening should additionally use a non-root user, resource quotas, network egress restrictions, filesystem isolation, and an authenticated gateway protecting infrastructure routes.

## MVP trade-offs

The first task measures dimensions rather than aesthetic quality. This creates a deterministic, cheap signal for validating action semantics and reward plumbing. It is not evidence of general 3D modeling competence.

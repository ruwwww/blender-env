# Runbook

Requirements: Python 3.11+, Blender 3.6+ on PATH, and optionally Docker.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e '.[dev]'
blender --version
pytest -q
```

Run the OpenEnv server:

```bash
blender-env-server --host 127.0.0.1 --port 8000
```

Evaluate one real Blender episode:

```bash
python scripts/evaluate_local.py --seed 42
```

Build and run Docker from the repository root:

```bash
docker build -f server/Dockerfile -t blender-env:local .
docker run --rm -p 8000:8000 -v "$PWD/artifacts:/tmp/blender-env" blender-env:local
```

Configuration:
- `BLENDER_BIN`: Blender executable (default `blender`; Docker uses `/usr/bin/blender`).
- `BLENDER_ENV_ARTIFACTS`: episode output root (default `/tmp/blender-env`).

The server supports one active environment session until concurrency isolation has been stress-tested. Protect infrastructure reset/step/state routes behind a trusted gateway. Production hardening should add non-root execution, resource quotas, network isolation, and authentication.

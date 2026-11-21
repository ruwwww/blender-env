# Architecture

## Boundary

OpenEnv is the agent-facing environment boundary. Blender execution, task generation, evaluation, and storage remain separate modules/services. The RL trainer (for example, verl) integrates through an adapter and does not define the environment domain model.

## Episode lifecycle

1. Sample a task specification and deterministic seed.
2. Allocate an isolated Blender workspace/worker.
3. Reset the scene and return an initial observation.
4. Validate and execute a structured action.
5. Return scene metadata, diagnostics, and optional render references.
6. Evaluate the terminal artifact and persist the trajectory.
7. Release worker resources.

## Planned modules

- contracts.py: trainer-agnostic action, observation, and reward types.
- tasks/: task schemas, factories, curriculum, and provenance.
- worker.py: isolated headless Blender process boundary.
- evaluation/: validity gates and geometry/constraint metrics.
- OpenEnv adapter: SDK-specific reset/step/close translation after the SDK version is pinned.
- Storage: artifacts, renders, logs, and trajectories.

## Security

Never execute arbitrary agent-provided Python inside the API server. If scripting actions are introduced, execute them only in disposable isolated workers with filesystem/network restrictions, resource quotas, timeouts, and explicit allowlists. Treat blend files and imported assets as untrusted inputs.

## MVP vertical slice

One primitive-object task, one structured action, one headless Blender worker, one scene observation, and one deterministic terminal evaluator.

# BlenderEnv

An OpenEnv-based reinforcement-learning environment for training LLM agents to create and iteratively improve 3D assets in Blender.

> Status: early scaffold. The environment contract, evaluator, and worker lifecycle are intentionally small and will evolve behind stable interfaces.

## Project goals

- Provide a reproducible, resettable Blender environment for agent episodes.
- Expose structured modeling actions and compact observations.
- Evaluate artifacts with deterministic geometry and constraint checks first; use visual or learned judges selectively.
- Keep the environment independent of the RL trainer (for example, verl).
- Persist task definitions, trajectories, renders, and final artifacts with provenance.

## Architecture (target)

```text
LLM policy
   |  OpenEnv client
   v
BlenderEnv API  ---- Task factory / task spec
   |
   +---- Action executor ---- isolated headless Blender worker
   |
   +---- Observation builder (scene graph, geometry, renders)
   |
   +---- Evaluator (validity gates, geometry metrics, constraints)
   |
   +---- Artifact / trajectory storage
   |
   +---- Trainer adapter (verl or another RL trainer)
```

## Development status

This repository currently contains the initial project scaffold and design notes. The first implementation milestone is a minimal vertical slice: reset a task, execute one structured action, return an observation, and compute a terminal reward for a simple object task.

## Design document

See the companion [BlenderEnv Master Technical Design](https://app.notion.com/p/41f230c18601815483adc39f23231faf) for the broader architecture, dataset strategy, reward design, and milestones.

## Principles

1. **Outcome-first reward:** terminal artifact quality is the primary signal initially.
2. **Hard validity gates:** invalid or broken geometry cannot be rescued by a visually pleasing render.
3. **No proxy gaming:** do not reward tool-call count, render frequency, or evaluator invocation.
4. **Reproducibility:** every task and episode records its seed, environment version, Blender version, and evaluator version.
5. **Trainer independence:** OpenEnv is the environment boundary; trainer-specific code lives in adapters.

## License

No license has been selected yet. Until one is added, all rights are reserved by default.

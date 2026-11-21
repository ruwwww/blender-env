# Reward and Evaluation Design

## Initial strategy

Use deterministic programmatic evaluation as the default reward source. The terminal artifact is the primary optimization target. Keep reward components separately logged so weights and evaluator versions can be audited.

## Evaluation tiers

1. Validity gates: Blender execution completed, expected objects exist, transforms are finite, mesh data is readable, and hard constraints pass.
2. Geometry and task metrics: dimensions, bounding boxes, component counts, topology diagnostics, silhouette agreement, surface distance for reference tasks, and normals where relevant.
3. Preference signals: selective VLM or human pairwise judgments for visual qualities deterministic metrics cannot capture.

## Guardrails

- A hard validity failure must not be compensated by a high visual score.
- Do not reward action count, render count, evaluator calls, or verbosity.
- Avoid dense shaping until it correlates with final artifact quality.
- Record raw metrics, normalized metrics, weights, evaluator version, and failure reasons.
- Test for reward hacking with adversarial and held-out task variants.

## Open decisions

Define metric implementations and normalization per task family; calibrate thresholds against human-reviewed artifacts; decide which intermediate diagnostics are safe to expose to the policy.

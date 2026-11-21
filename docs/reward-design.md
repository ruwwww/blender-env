# Reward design (v0.2)

The evaluator is deterministic and terminal-only.

Validity is a hard gate: successful Blender execution, exactly one mesh object, three finite positive dimensions, and at least eight vertices. If any gate fails, reward is zero.

For valid geometry:

`dimension_match = exp(-mean_i(abs(log(actual_i / target_i))) )`

`reward = 0.2 + 0.8 * dimension_match`

An exact match scores 1.0. Multiplicative error is symmetric in log space: twice too large and half as large have equal per-axis error.

No per-action reward is issued. The evaluator does not reward tool calls, renders, verbosity, or attempts. Each terminal episode stores evaluator version, target and actual dimensions, component scores, and failure reasons.

This is a plumbing benchmark, not a final 3D quality metric. Before broad RL, calibrate it against adversarial geometry and human-reviewed task variants.

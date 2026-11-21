# Dataset and Task Design

Separate three data products:

1. Task dataset: natural-language instruction, hidden structured specification, seed/factory parameters, evaluator configuration, reference assets where applicable, and provenance/license metadata.
2. Demonstration dataset: curated action-observation trajectories for supervised fine-tuning and tool-use bootstrapping.
3. RL trajectory dataset: policy-generated episodes containing task/version metadata, observations, actions, execution results, reward breakdowns, and final artifacts.

## Task families and curriculum

Start with primitives and simple parametric objects, then component-based furniture, detailed single objects, reference-conditioned modeling, and creative scenes. Use procedural task factories to scale variations instead of manually authoring every prompt.

## Data quality

- Keep natural-language instructions separate from hidden evaluator specifications.
- Validate reference/render/mesh alignment and asset provenance.
- Split evaluation by object family or factory configuration, not only random seed.
- Retain failed trajectories with explicit failure labels.
- Track source, license, Blender version, task-factory version, and evaluator version.

"""Run one reproducible Blender episode without an LLM."""
import argparse, json
from blender_env.models import BlenderAction
from blender_env.server.environment import BlenderEnvironment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--episode-id", default="local-eval")
    args = parser.parse_args()
    env = BlenderEnvironment()
    try:
        obs = env.reset(seed=args.seed, episode_id=args.episode_id)
        print("TASK:", obs.instruction)
        env.step(BlenderAction(op="create_cube"))
        obs = env.step(BlenderAction(op="set_dimensions", dimensions=obs.target_dimensions))
        obs = env.step(BlenderAction(op="finish"))
        print(json.dumps({"reward": obs.reward, "done": obs.done,
                          "metrics": obs.terminal_metrics,
                          "artifact_dir": env.state.workspace}, indent=2))
    finally:
        env.close()


if __name__ == "__main__":
    main()

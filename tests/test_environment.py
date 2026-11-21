from blender_env.models import BlenderAction
from blender_env.server.environment import BlenderEnvironment
from blender_env.worker import InMemoryWorker


def test_full_episode(tmp_path):
    env = BlenderEnvironment(worker=InMemoryWorker(), artifact_root=str(tmp_path))
    initial = env.reset(seed=7, episode_id="test-episode")
    target = initial.target_dimensions
    assert not initial.done
    env.step(BlenderAction(op="create_cube"))
    env.step(BlenderAction(op="set_dimensions", dimensions=target))
    final = env.step(BlenderAction(op="finish"))
    assert final.done and final.reward == 1.0
    assert final.terminal_metrics["valid"]
    assert (tmp_path / "test-episode" / "episode.json").exists()
    env.close()


def test_seed_reproducibility(tmp_path):
    env = BlenderEnvironment(worker=InMemoryWorker(), artifact_root=str(tmp_path))
    a = env.reset(seed=123).target_dimensions
    b = env.reset(seed=123).target_dimensions
    assert a == b
    env.close()

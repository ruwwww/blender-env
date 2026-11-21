from blender_env.contracts import Action, Observation, RewardBreakdown

def test_domain_contracts_are_constructible():
    action = Action(name="create_object", parameters={"primitive": "cube"})
    observation = Observation(task_id="cube-001", step_index=0, scene={"objects": []})
    reward = RewardBreakdown(total=0.0, components={"validity": 0.0}, valid=True, evaluator_version="0.1.0")
    assert action.name == "create_object"
    assert observation.task_id == "cube-001"
    assert reward.valid is True

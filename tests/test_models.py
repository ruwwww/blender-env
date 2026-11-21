import pytest
from pydantic import ValidationError
from blender_env.models import BlenderAction


def test_action_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        BlenderAction(op="run_python", arbitrary_code="import os")


def test_dimensions_shape_is_validated():
    with pytest.raises(ValidationError):
        BlenderAction(op="set_dimensions", dimensions=[1.0, 2.0])

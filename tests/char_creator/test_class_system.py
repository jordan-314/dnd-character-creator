import sys

import pytest

from src.char_creator.class_system import _validate_class_attr


@pytest.mark.parametrize("value", [-1, 21, sys.maxsize, -sys.maxsize + 1])
def test_cls_validator_error(value: int):
    """Test that a ValueError is raised when the value is not on the bounds [0,20]."""
    with pytest.raises(ValueError):
        _validate_class_attr(value)

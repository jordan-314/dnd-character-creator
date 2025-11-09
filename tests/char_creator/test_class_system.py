import sys

import pytest

from src.char_creator.class_system import Attributes, _BaseClass, _validate_class_attr
from src.exc import AttributeBoundsError


@pytest.fixture
def attrs() -> Attributes:
    return Attributes(
        strength=8, dexterity=8, constitution=8, intelligence=8, wisdom=8, charisma=8
    )


@pytest.fixture
def base(attrs: Attributes) -> _BaseClass:
    return _BaseClass(attrs, "Dragonborn")


@pytest.mark.parametrize("value", [-1, 21, sys.maxsize, -sys.maxsize + 1])
def test_cls_validator_error(value: int):
    """Test that a ValueError is raised when the value is not on the bounds [0,20]."""
    with pytest.raises(AttributeBoundsError):
        _validate_class_attr(value)


class TestBaseClass:
    """Define test suite for testing _BaseClass. Class is mroe for organisation."""

    @pytest.mark.parametrize("value", [0, -1, -sys.maxsize + 1])
    def test_increment_attr_throws_error(self, base: _BaseClass, value: int):
        """Test an error is thrown when a bad value is given."""
        with pytest.raises(ValueError):
            base.increment_attr("strength", value=value)

    def test_increment(self, base: _BaseClass):
        """Test that the increment method increments the appropriate value."""
        original_value = base.attributes.strength

        base.increment_attr("strength")
        assert base.attributes.strength == original_value + 1

        base.increment_attr("strength", 2)
        assert base.attributes.strength == original_value + 3

        # Return strength attr back to 8.
        base.decrement_attr("strength", 3)

    @pytest.mark.parametrize("value", [0, -1, -sys.maxsize + 1])
    def test_decrement_attr_throws_error(self, base: _BaseClass, value: int):
        """Test an error is thrown when a bad value is given."""
        with pytest.raises(ValueError):
            base.decrement_attr("strength", value=value)

    def test_decrement(self, base: _BaseClass):
        """Test that the increment method increments the appropriate value."""
        original_value = base.attributes.strength

        base.decrement_attr("strength")
        assert base.attributes.strength == original_value - 1

        base.decrement_attr("strength", 2)
        assert base.attributes.strength == original_value - 3

        # Return strength attr back to 8.
        base.increment_attr("strength", 3)

    def test_bad_attr_modification(self, base: _BaseClass):
        """Give a bad attribute name, expecting an AttributeError."""
        with pytest.raises(AttributeError):
            base._modify_attr("blah", 1)

    @pytest.mark.parametrize("value", [21, sys.maxsize, -21, -sys.maxsize + 1])
    def test_bounds_error_raised(self, base: _BaseClass, value: int):
        """Test that when a value is excessively modified that, expecting AttributeBoundsError."""
        with pytest.raises(AttributeBoundsError):
            base._modify_attr("strength", value=value)

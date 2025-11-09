"""Define the basics of the DND class system."""

from typing import Annotated, get_args

from pydantic import AfterValidator, BaseModel, PositiveInt, validate_call

from src._utils import Attribute, Race
from src.exc import AttributeBoundsError


def _validate_class_attr(attr: int) -> int:
    if attr < 0 or attr > 20:
        msg = "Attribute must be on the bound [0,20]."
        raise AttributeBoundsError(msg)
    return attr


class Attributes(BaseModel):
    """Define a basic model for containing any and all class attrs.

    TODO: Dataclass?
    """

    strength: Annotated[int, AfterValidator(_validate_class_attr)]
    dexterity: Annotated[int, AfterValidator(_validate_class_attr)]
    constitution: Annotated[int, AfterValidator(_validate_class_attr)]
    intelligence: Annotated[int, AfterValidator(_validate_class_attr)]
    wisdom: Annotated[int, AfterValidator(_validate_class_attr)]
    charisma: Annotated[int, AfterValidator(_validate_class_attr)]


class _BaseClass:
    """Interface for all classes, defines any basic methods"""

    def __init__(self, attributes: Attributes, race: Race):
        """"""
        self._attrs = attributes
        self._race = race

    @property
    def attributes(self):
        """Read only attribute access."""
        return self._attrs

    @validate_call
    def increment_attr(self, attr_name: Attribute, value: PositiveInt = 1) -> None:
        """Increment an attribute, accessed via the name of the attribute, by a set value. Value defaults to 1.

        :param attr_name: The name of the attribute to modify.
        :param value: The value to increment the attribute by.
        """
        self._modify_attr(attr_name=attr_name, value=value)

    @validate_call
    def decrement_attr(self, attr_name: Attribute, value: PositiveInt = 1) -> None:
        """Decrement an attribute, accessed via the name of the attribute, by a set value. Value defaults to -1.

        :param attr_name: The name of the attribute to modify.
        :param value: The value to increment the attribute by.
        """
        # Invert value to be negative.
        self._modify_attr(attr_name=attr_name, value=-value)

    def _modify_attr(self, attr_name: Attribute, value: int) -> None:
        """Modify the value of an attribute value."""
        if not hasattr(self._attrs, attr_name):
            msg = f"Invalid attribute. Allowed are: {get_args(Attribute)}"
            raise AttributeError(msg)

        new_value = getattr(self._attrs, attr_name) + value
        if new_value < 0 or new_value > 20:
            msg = "Bad attr modification, attr should exist on bounds [0,20]."
            raise AttributeBoundsError(msg)

        setattr(self._attrs, attr_name, new_value)

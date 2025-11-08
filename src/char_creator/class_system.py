"""Define the basics of the DND class system."""

from typing import Annotated, get_args

from pydantic import AfterValidator, BaseModel, NegativeInt, PositiveInt

from src._utils import Attribute, Race


def _validate_class_attr(attr: int) -> int:
    if attr < 0 or attr > 20:
        msg = "Attribute must be on the bound [0,20]."
        raise ValueError(msg)
    return attr


class Atrributes(BaseModel):
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

    def __init__(self, attributes: Atrributes, race: Race):
        """"""
        self._attrs = attributes
        self._race = race

    def increment_attr(self, attr_name: Attribute, value: PositiveInt = 1) -> None:
        """Increment an attribute, accessed via the name of the attribute, by a set value. Value defaults to 1.

        :param attr_name:"""
        if value <= 0:
            msg = "Provide a positive integer."
            raise ValueError(msg)
        self._modify_attr(attr_name=attr_name, value=value)

    def decrement_attr(self, attr_name: Attribute, value: NegativeInt = -1) -> None:
        """Decrement an attribute, accessed via the name of the attribute, by a set value. Value defaults to -1."""
        if value >= 0:
            msg = "Provide a negative integer."
            raise ValueError(msg)
        self._modify_attr(attr_name=attr_name, value=value)

    def _modify_attr(self, attr_name: Attribute, value: int) -> None:
        """Modify the value of an attribute value."""
        if not hasattr(self._attrs, attr_name):
            msg = f"Invalid attribute. Allowed are: {get_args(Attribute)}"
            raise AttributeError(msg)
        new_value = getattr(self._attrs, attr_name) + value
        setattr(self._attrs, attr_name, new_value)

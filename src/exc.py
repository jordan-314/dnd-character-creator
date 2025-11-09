"""Define any and all custom errors."""


class AttributeBoundsError(ValueError):
    """Raise when a (DND) class attribute is out of the bounds [0,20]."""

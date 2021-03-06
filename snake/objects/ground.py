
from snake.objects import constants
from .base_object import Object


class Ground(Object):
    """
        Ground object on which other object are free to be placed.
    """
    rgb = constants.WHITE
    ansi_fancy = constants.SQUARE_BLACK_SMALL
    ansi = "."

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return f"<class {self.__class__.__name__}"

    def __repr__(self):
        return f"<class {self.__class__.__name__} (x={self.position.x}, y={self.position.y})>"

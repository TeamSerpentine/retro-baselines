
from snake.objects import constants
from .base_object import Object


class Wall(Object):
    """
        Wall, object that kills snake.
    """
    colour = constants.BLACK
    text_fancy = constants.SQUARE_WHITE
    text = "X"

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return f"<class {self.__class__.__name__}"

    def __repr__(self):
        return f"<class {self.__class__.__name__} (x={self.position.x}, y={self.position.y})>"
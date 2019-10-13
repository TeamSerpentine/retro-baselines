
from . import constants
from .base_object import Object, Point


class Apple(Object):
    """
        Apple, object that can be eaten in the snake.
    """
    rgb = constants.RED
    ansi_fancy = constants.FISH_EYE
    ansi = "A"

    def __init__(self, position: Point):
        self.position = position

    def __str__(self):
        return f"<class {self.__class__.__name__}"

    def __repr__(self):
        return f"<class {self.__class__.__name__} (x={self.position.x}, y={self.position.y})>"

    def __eq__(self, other):
        return self.collide(other)

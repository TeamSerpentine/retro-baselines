
from .utils import Point
from abc import ABC, abstractmethod
from copy import deepcopy


class AbstractObject(ABC):
    position: Point     # Position
    rgb: tuple       # For image displaying
    ansi: str           # For string display

    @abstractmethod
    def __str__(self): ...

    @abstractmethod
    def __repr__(self): ...

    @abstractmethod
    def clone(self) -> object: ...

    @abstractmethod
    def collide(self, other) -> bool: ...

    @abstractmethod
    def location(self) -> list: ...


class Object(AbstractObject):
    position = Point(-1, -1)
    rgb = (0, 0, 0)
    ansi = "?"
    ansi_fancy = "?"        # For unicode characters display

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return f"<class {self.__class__.__name__}"

    def __repr__(self):
        return f"<class {self.__class__.__name__} (x={self.position.x}, y={self.position.y})>"

    def clone(self):
        """
            Clones the object
        :return: a copy of itself
        """
        return deepcopy(self)

    def collide(self, other):
        """
            Checks if the object position collides with the position of the object

        :param other: Object
        :return: bool
        """
        if self.position == other.position:
            return True
        return False

    def location(self):
        """ Returns all the locations of an object as an iterable """
        return [self.position]

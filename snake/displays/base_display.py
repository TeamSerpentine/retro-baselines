
import abc
from abc import ABC
from typing import Any


class BaseDisplay(ABC):
    """ Base class for all displays to be compatible with snake games.  """

    def __init__(self, *args, **kwargs):
        """  Initialize self.  See help(type(self)) for accurate signature.  """
        pass

    @abc.abstractmethod
    def render(self, obs: Any):
        """ Renders the snake game.  """
        pass

    @abc.abstractmethod
    def close(self):
        """ Any actions that need to perform for proper closing """
        pass

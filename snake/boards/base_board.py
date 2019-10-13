import abc
import numpy as np
from abc import ABC


class BaseBoard(ABC):
    """ Base class for any Snake board.   """

    def __init__(self, *args, **kwargs):
        """  Initialize self.  See help(type(self)) for accurate signature.  """
        pass

    def __str__(self):
        """  Return str(self).  """
        pass

    def __repr__(self):
        """ Return repr(self).  """
        pass

    @abc.abstractmethod
    def obs(self, *args, **kwargs) -> np.array:
        """ Returns the observation from the board.  """
        pass

    @abc.abstractmethod
    def reward(self, *args, **kwargs) -> int:
        """ Returns the reward of the current step.  """
        pass

    @abc.abstractmethod
    def done(self, *args, **kwargs) -> bool:
        """ Returns whether the game is finished playing or not.  """
        pass

    @abc.abstractmethod
    def info(self, *args, **kwargs) -> dict:
        """ Returns extra information about the current game step.  """
        pass

    @abc.abstractmethod
    def step(self, action: int) -> (np.array, int, bool, dict):
        """
            Take a step in the environment based on the action given as input.

            The step function should return the state, reward, terminal flag and other information
            after the action has been performed in the environment.

            :param action: int.
            :return: obs, reward, done, info
        """
        pass

    @abc.abstractmethod
    def reset(self) -> np.array:
        """ Resets the board to a new random start position.  """
        pass

    @abc.abstractmethod
    def close(self):
        """ Closes the environment.  """
        pass

    @abc.abstractmethod
    def random_step(self) -> int:
        """ Returns a random move in the available action space of the board.  """
        pass

    @abc.abstractmethod
    def seed(self, seed: [list, None]) -> list:
        """ Set the seed of the game, makes it possible to reproduce games.  """
        pass

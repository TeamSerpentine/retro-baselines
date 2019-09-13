"""
Base environment class used to run custom games in retro_baselines.

Custom games need to inherit and implement all methods in the BaseEnvironment class in order to
be compatible with the main game loop in insertcoin.py.
"""

import abc
import numpy as np
from abc import ABCMeta


class BaseActionSpace(metaclass=ABCMeta):
    """
        Action space necessary to run games as an environment in retro_baselines.

        The action space contains the actions an player can take possibly take in a game.
    """

    @abc.abstractmethod
    def __init__(self, n):
        """
            Initialize ActionSpace with size n.

            :param n: int
                Number of actions
        """
        pass

    @abc.abstractmethod
    def sample(self):
        """
            Randomly sample from ActionSpace

            :return: Action: int
        """
        pass


class BaseEnvironment(metaclass=ABCMeta):
    """
        Base environment class used to run custom games in retro_baselines.

        Custom games need to inherit and implement the BaseEnvironment class in order to be compatible with the
        main game loop in insertcoin.py.
    """

    @abc.abstractmethod
    def __init__(self):
        self.action_space = self.get_action_space()

    @abc.abstractmethod
    def step(self, action: int) -> (np.ndarray, int, bool, dict):
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
        """ Reset the environment and returns the begin observation of the game.  """
        pass

    @abc.abstractmethod
    def get_action_space(self) -> BaseActionSpace:
        """ Get the action space of the environment. """
        pass

    @abc.abstractmethod
    def render(self):
        """ Render game using this interface. """
        pass

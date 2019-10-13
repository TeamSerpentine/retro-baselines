"""
Base model class.

The base model class defines the interface for models in retro_baselines.
A model takes actions each snake frame and uses a logger to store data.
"""

import abc
import numpy as np

from abc import ABCMeta
from typing import Union


class BaseModel(metaclass=ABCMeta):
    """
        The base model class defines the interface for models in retro_baselines.
    """

    @abc.abstractmethod
    def __init__(self, game_name: str, input_shape: Union[tuple, list], action_space: int, logger_path: str):
        """
            Initialize base model.

            :param game_name: Name of the current snake.
            :param input_shape: Shape of the input array.
            :param action_space: Set of actions that are available in the game
            :param logger_path: Path to the log files.
        """
        pass

    @abc.abstractmethod
    def save_game(self, score: Union[int, float], step: int, run: int):
        """
            Save information of one snake run using the logger.

            :param score: intScore this run.
            :param step: Amount of steps this run.
            :param run: Current run number.
        """
        pass

    @abc.abstractmethod
    def action(self, state: np.ndarray):
        """
            Return action according to the current state of the snake.

            :param state: State of the snake.
        """
        pass

    @abc.abstractmethod
    def remember(self, state: np.ndarray, action: int, reward: Union[int, float],
                 next_state: np.ndarray, done: bool):
        """
            Store snake step information in internal memory.

            :param state: State of the snake.
            :param action: Action taken this frame.
            :param reward: Reward gained this frame.
            :param next_state: State after action has been executed.
            :param done: Game flag. True if snake run is over and has to be reset.
        """
        pass

    @abc.abstractmethod
    def step_update(self, total_step: int):
        """
            Update model with total amount of steps taken.

            :param total_step: int
                Total amount of steps taken.
        """
        pass

    @abc.abstractmethod
    def finalize_game(self, score: Union[int, float], step: int, run: int):
        """
            Called at the end of a single game.

            :param score: Score this run.
            :param step: Amount of steps this run.
            :param run: Current run number.
        """
        pass

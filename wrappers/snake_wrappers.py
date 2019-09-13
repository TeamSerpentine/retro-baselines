"""
Classes for snake game wrappers.

Game wrappers provides a standard interface in order to run games using insertcoin.py.
It takes care of pre-processing steps without having to alter the underlying games.
"""

from snake.boards.classic import Board
from .base_wrapper import BaseGameWrapper


class SnakeGameWrapper(BaseGameWrapper):
    """
    Base class for game wrappers.

    Pre processing for Snake game.
    """

    def wrap(self, env: Board):
        """
        Wrap snake game and return the wrapped environment for use.

        :param env: Snake environment to wrap.
        :return: Wrapped snake environment.
        """
        return env


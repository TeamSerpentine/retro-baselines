
import numpy as np

from snake.games.base_game import SnakeGame
from snake.boards.classic import Board
from snake.displays.single_image import SingleImage


class Snake(SnakeGame):
    """
        Classic snake game with pygame rendering of observations.
        This will return an image.
    """
    def __init__(self):
        board = Board()
        render = SingleImage(board.width, board.height, scale_factor=10)
        self._image = np.zeros((board.width, board.height, 3), dtype=np.uint8)
        super().__init__(board, render)

    def obs(self):
        """ Extra conversion to create a 3D image from the 2D observation"""
        obs = self.board._get_obs(attribute="colour")
        for x in range(obs.shape[0]):
            for y in range(obs.shape[1]):
                self._image[x, y] = obs[x, y]
        return self._image

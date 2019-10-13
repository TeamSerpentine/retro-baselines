
import numpy as np

from snake.boards.classic import Board


class SnakeGame:
    """ Remapping of all board functions to the public available environment functions.  """

    def __init__(self, width=None, height=None):
        self.board = Board(width, height)
        self.image = np.zeros((self.board.width, self.board.height, 3), dtype=np.uint8)

    def obs(self, attribute="rgb"):
        return self.board.obs(attribute)

    def reward(self):
        return self.board.reward()

    def done(self):
        return self.board.done()

    def info(self):
        return self.board.info()

    def step(self, action: int):
        self.board.step(action, values=False)
        return self.obs(), self.reward(), self.done(), self.info()

    def reset(self):
        """ Reset the game, and should return the start observation of the game. """
        self.board.reset()
        return self.obs()

    def render(self):
        return self.board.obs(attribute='rgb')

    def close(self):
        self.board.close()

    def seed(self, seed=None):
        return self.board.seed(seed)

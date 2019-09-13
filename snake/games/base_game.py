
import numpy as np
from base_environment import BaseEnvironment, BaseActionSpace


class ActionSpace(BaseActionSpace):
    """
        Action space necessary to run games as an environment in retro_baselines.

        The action space contains the actions an player can take possibly take in a game.
    """

    def __init__(self, n):
        self.n = n

    def sample(self):
        return np.random.choice(range(self.n))


class SnakeGame(BaseEnvironment):
    """ Remapping of all board functions to the public available environment functions.  """

    def __init__(self, board, display):
        self.board = board
        self.display = display
        self.action_space = ActionSpace(self.board.action_space)
        super().__init__()

    def obs(self):
        return self.board._get_obs()

    def reward(self):
        return self.board._get_reward()

    def done(self):
        return self.board._get_done()

    def info(self):
        return self.board._get_info()

    def get_action_space(self):
        return ActionSpace(self.board.action_space)

    def step(self, action: int):
        self.board._step(action)
        return self.obs(), self.reward(), self.done(), self.info()

    def reset(self):
        """ Reset the game, and should return the start observation of the game. """
        self.board.reset()
        return self.obs()

    def render(self):
        return self.display.render(self.obs())

    def close(self):
        self.board.close()
        self.display.close()

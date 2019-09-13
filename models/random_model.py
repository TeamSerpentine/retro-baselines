"""
Random choice model.

The random choice model chooses a random action in a snake, taking into account the appropriate action space.
Useful for testing purposes but not so much for playing a snake well.
"""
import random
from models.base_model import BaseModel


class RandomModel(BaseModel):
    """
        Model that takes a random action in a snake.
    """

    def __init__(self, game_name, input_shape, action_space, logger_path="output/random_model"):
        """
            Initialize random model and base class.
        """
        self.action_space = action_space
        self.input_shape = input_shape
        self.game_name = game_name
        self.logger_path = logger_path

    def action(self, state):
        """
            Take a random step and return the corresponding action.

            :param state: State of the snake.
            :return: Integer corresponding to action in action space.
        """
        return random.randrange(self.action_space.n)

    def remember(self, state, action, reward, next_state, done):
        """
            Store snake step information in internal memory.

            :param state: State of the snake.
            :param action: Action taken this frame.
            :param reward: Reward gained this frame.
            :param next_state: State after action has been executed.
            :param done: Game flag. True if snake run is over and has to be reset.
        """
        pass

    def step_update(self, total_step):
        """
            Update model with total amount of steps taken.

            :param total_step: Total amount of steps taken.
        """
        pass

    def save_game(self, score, step, run):
        """
            Called at the end of a single game.

            :param score: Score this run.
            :param step: Amount of steps this run.
            :param run: Current run number.
        """
        pass

    def finalize_game(self, score, step, run):
        """
            Called at the end of a single game.

            :param score: Score this run.
            :param step: Amount of steps this run.
            :param run: Current run number.
        """
        pass

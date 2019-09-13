
import itertools
import numpy as np

from snake.objects.utils import Point
from snake.games.base_game import SnakeGame
from snake.boards.classic import Board
from snake.displays.single_image import SingleImage


class Snake(SnakeGame):
    """
        Classic snake game, which outputs a numpy ndarray of size (24,)
        Containing 8 times snake
    """
    def __init__(self):
        board = Board()
        render = SingleImage(board.width, board.height)
        self._image = np.zeros((board.width, board.height, 3), dtype=np.uint8)
        super().__init__(board, render)

    def obs(self):
        """
            Generates the output array.
            The output will be a (24,) numpy array, with 3 times 8 directions.

            wall distance, snake distance, food distance
            ["UP", "DOWN", "LEFT", "LEFT UP", "LEFT DOWN", "RIGHT", "RIGHT UP", "RIGHT DOWN"]
        """
        object_types = [v for k, v in self.board.object_types.items() if k != "ground"]
        obs_directions = [x for x in itertools.product([0, 1, -1], repeat=2)][1:]
        obs_out = np.zeros((len(object_types), len(obs_directions)), dtype=np.int)

        snake = self.board.objects['snake'][0]
        for idx_direction, direction in enumerate(obs_directions):
            scan_direction = Point(*direction)
            object_found = False
            scan_counter = 1
            while not object_found:
                scan_x = snake.position.x + scan_direction.x * scan_counter
                scan_y = snake.position.y + scan_direction.y * scan_counter
                for idx_object, object_type in enumerate(object_types):
                    if isinstance(self.board.board[scan_x, scan_y], object_type):
                        obs_out[idx_object, idx_direction] = scan_counter
                        object_found = True
                scan_counter += 1
        return obs_out.flatten()

    def reward(self):
        """ Returns the number of apples eaten during the entire game.  """
        snake = self.board.objects['snake'][0]
        return len(snake) - snake.LEN_SNAKE_START

    def render(self):
        obs = self.board._get_obs(attribute="colour")
        for x in range(obs.shape[0]):
            for y in range(obs.shape[1]):
                self._image[x, y] = obs[x, y]
        return self.display.render(self._image)

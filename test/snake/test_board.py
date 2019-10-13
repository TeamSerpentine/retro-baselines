
import unittest

from snake.boards.classic import Board
from snake.objects.utils import Point
from snake.objects import constants


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board(width=25, height=25)

    def test_add_snake_random(self):
        self.board.add_object('snake')
        self.assertEqual(1, len(self.board.objects['snake']), "Single snake not added correctly")

    def test_add_snake_specific(self):
        self.board.snakes = []

        self.board.add_object("snake", Point(x=10, y=15))
        snake = self.board.objects['snake'].pop()

        self.assertEqual(10, snake.get_head().x, "x position not set correctly")
        self.assertEqual(15, snake.get_head().y, "y position not set correctly")
        self.assertEqual(constants.LEN_SNAKE_START, len(snake), "Snake is not start length")

    def test_add_snake_collision(self):
        self.board.snakes = []

        self.board.add_object("snake", Point(x=20, y=20))
        self.board.add_object("snake", Point(x=20, y=20))

        snake_1 = self.board.objects['snake'].pop()
        snake_2 = self.board.objects['snake'].pop()

        self.assertEqual(False, snake_1 in snake_2, "These are the same snakes")

    def test_setting_seed(self):
        """ Test if the same board is produced after setting a seed.  """
        seed = self.board.seed()

        for _ in range(10):
            self.board.reset()
        state = self.board.board

        self.board.seed(seed)
        for _ in range(10):
            self.board.reset()

        self.assertEqual([o.__class__.__name__ for x in state for o in x],
                         [o.__class__.__name__ for x in self.board.board for o in x], "Unable to reproduce same board")

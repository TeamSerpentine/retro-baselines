

import unittest

from snake.boards.classic import Board
from snake.objects.utils import Point
from snake.objects import constants


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()

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

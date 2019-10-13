

import unittest

from snake import constants
from snake.objects.constants import LEN_SNAKE_START
from snake.boards.classic import Board

from snake.objects.wall import Wall
from snake.objects.ground import Ground
from snake.objects.apple import Apple
from snake.objects.snake import Snake
from snake.objects.utils import Point


class TestCollision(unittest.TestCase):

    def setUp(self) -> None:
        self.objects_name = ["wall", "ground", "apple", "snake"]

        self.wall = Wall(Point(0, 0))
        self.ground = Ground(Point(10, 10))
        self.apple = Apple(Point(20, 20))
        self.snake = Snake(Point(30, 30))

        self.wall_same = Wall(Point(0, 0))
        self.ground_same = Ground(Point(0, 0))
        self.apple_same = Apple(Point(0, 0))
        self.snake_same = Snake(Point(0, 0))

        self.objects_diff = [getattr(self, name) for name in self.objects_name]
        self.objects_same = [getattr(self, name + "_same") for name in self.objects_name]

    def test_collisions(self):
        for each in self.objects_name:
            test_objects_diff = [item.clone() for item in self.objects_diff]
            test_objects_diff.pop(self.objects_name.index(each))
            result = [getattr(self, each).collide(item) for item in test_objects_diff]
            self.assertEqual([False, False, False], result, "Incorrect collision detected")

            test_objects_same = [item.clone() for item in self.objects_same]
            test_objects_same.pop(self.objects_name.index(each))
            result = [getattr(self, each + "_same").collide(item) for item in test_objects_same]
            self.assertEqual([True, True, True], result, "Incorrect collision detected")

    def test_snake_eat_apple(self):
        self.board = Board(width=50, height=50)
        self.board.add_object("snake", Point(x=20, y=33))
        self.board.add_object("apple", Point(x=20, y=32))

        snake = self.board.objects['snake'][0]
        _, reward, _, _ = self.board.step(constants.GET_ACTION_MEANING.index("UP"))

        self.assertEqual(constants.DEFAULT_REWARD_PER_APPLE + constants.DEFAULT_REWARD_PER_STEP, reward,
                         "Snake eating apple incorrect points awarded")

        self.assertEqual(LEN_SNAKE_START+1, len(snake),
                         "Snake length is not increased after eating apple")

    def test_snake_wall(self):
        self.board = Board(width=50, height=50)
        self.board.add_object("snake", Point(x=1, y=30))

        snake = self.board.objects['snake'][0]
        _, _, done, _ = self.board.step(constants.GET_ACTION_MEANING.index("LEFT"))
        self.board.step(1)

        self.assertEqual(True, done, "Game over is not detected upon dying")
        self.assertEqual(False, snake.alive,
                         "Snake didn't die upon hitting the wall")

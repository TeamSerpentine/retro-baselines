

import unittest

from snake.objects.snake import Snake
from snake.objects.utils import Point


class TestSnake(unittest.TestCase):

    def setUp(self) -> None:
        self.pos_start = Point(50, 120)
        self.pos_diff = Point(50, 115)
        self.start_direction = "UP"
        self.snake = Snake(self.pos_start)

    def test_increase_length_still(self):
        new_length = 10
        for _ in range(new_length-3):
            self.snake.increase_length()

        self.assertEqual(new_length, len(self.snake),
                         "Length not increasing correctly")

        for num in range(new_length-2):
            self.assertEqual(self.snake.body[num], self.snake.body[-3],
                             "Last position is not copied")

    def test_increase_length_stepping(self):
        new_length = 10
        self.snake.body.pop()
        steps_up = 0

        for steps_up in range(1, new_length):
            self.snake.increase_length()
            self.snake.step()

            self.assertEqual(self.pos_start.x, self.snake.get_head().x,
                             "x direction is no longer correct")
            self.assertEqual(self.pos_start.y + steps_up, self.snake.get_head().y,
                             "y direction is no longer correct")

            self.assertEqual(self.pos_start.x, self.snake.get_tail().x,
                             "x direction is no longer correct")
            self.assertEqual(self.pos_start.y, self.snake.get_tail().y,
                             "y direction is no longer correct")

        self.snake.direction = "LEFT"
        for steps_left in range(1, new_length):
            self.snake.increase_length()
            self.snake.step()

            self.assertEqual(self.pos_start.x - steps_left, self.snake.get_head().x,
                             "x direction is no longer correct")
            self.assertEqual(self.pos_start.y + steps_up, self.snake.get_head().y,
                             "y direction is no longer correct")

            self.assertEqual(self.pos_start.x, self.snake.get_tail().x,
                             "x direction is no longer correct")
            self.assertEqual(self.pos_start.y, self.snake.get_tail().y,
                             "y direction is no longer correct")

    def test_step(self):
        steps = 10
        for direction in ["UP", "LEFT", "DOWN", "RIGHT"]:
            self.snake.direction = direction
            for _ in range(steps):
                self.snake.step()

            if direction == "UP":
                self.assertEqual((self.pos_start.x, self.pos_start.y + steps),
                                 self.snake.get_head().as_value(),
                                 "Mistake in UP")

            elif direction == "LEFT":
                self.assertEqual((self.pos_start.x - steps, self.pos_start.y + steps),
                                 self.snake.get_head().as_value(),
                                 "Mistake in LEFT")

            elif direction == "DOWN":
                self.assertEqual((self.pos_start.x - steps, self.pos_start.y),
                                 self.snake.get_head().as_value(),
                                 "Mistake in DOWN")

            elif direction == "RIGHT":
                self.assertEqual((self.pos_start.x, self.pos_start.y),
                                 self.snake.get_head().as_value(),
                                 "Mistake in RIGHT")
            else:
                raise ValueError("Direction doesn't exists")

        self.assertEqual(self.pos_start, self.snake.get_head(), "No square made")
        self.assertEqual(3, len(self.snake.body), "Snake length is no longer correct")

    def test_contains(self):
        snake_diff = Snake(self.pos_diff)
        snake_diff.direction = self.start_direction

        for _ in range(4):
            snake_diff.step()
            self.assertEqual(False, self.snake in snake_diff, "A Faulty collision detected")

        snake_diff.step()
        self.assertEqual(True, self.snake in snake_diff, "Collision not detected")
        self.assertEqual(True, self.snake in self.snake, "Snake doesn't contain itself")

    def test_compare(self):
        snake_diff = Snake(self.pos_diff)
        snake_diff.direction = self.start_direction

        self.assertEqual(True, self.snake == self.snake, "Snake equals itself")
        self.assertEqual(False, self.snake != self.snake, "Snake doesn't equals itself")

        self.assertEqual(False, self.snake == snake_diff, "Snakes are not different")
        self.assertEqual(True, self.snake != snake_diff, "Snakes are different")

    def test_collide_body(self):
        collide = self.snake.collide(type("", (), dict(position=Point(43, 150))))
        self.assertEqual(False, collide, "Collide body wrongly detected")

        collide = self.snake.collide(type("", (), dict(position=Point(50, 150))))
        self.assertEqual(False, collide, "Collide body wrongly detected")

        collide = self.snake.collide(type("", (), dict(position=Point(80, 120))))
        self.assertEqual(False, collide, "Collide body wrongly detected")

        collide = self.snake.collide(type("", (), dict(position=self.pos_start)))
        self.assertEqual(True, collide, "Collide body not detected")

    def test_reversal(self):
        """ Makes sure that you can't run into the body on your own.  """
        for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            self.snake.direction = direction
            for _ in range(5):
                self.snake.step()
                self.snake.direction = direction

                if direction in ["UP", "DOWN"]:
                    self.assertEqual("UP", self.snake.direction, "Direction not countered")

                if direction in ["LEFT", "RIGHT"]:
                    self.assertEqual("LEFT", self.snake.direction, "Direction not countered")

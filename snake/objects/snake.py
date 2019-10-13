
from collections import deque

from snake.objects import constants
from .base_object import Object


class Snake(Object):
    """
        Snake, object that can move over the board and interact with other objects.

        :param position: utils.Point
            The start position of the snake.
    """
    rgb = constants.GREEN_SERPENTINE
    ansi_fancy = constants.SQUARE_BLACK
    ansi = "0"

    APPLE_TIME = constants.APPLE_TIME
    LIFE_MAX = constants.LIFE_MAX
    LEN_SNAKE_START = constants.LEN_SNAKE_START
    LEN_SNAKE_MAX = constants.LEN_SNAKE_MAX

    def __init__(self, position):
        self.position = position

        # Define start direction and timers
        self._direction = constants.DIRECTION_START
        self.life_left = constants.LIFE_START    # Time until snake dies
        self.life_time = 0                       # Time snake lives
        self.alive = True

        # Create the snake body
        self.body = deque(maxlen=self.LEN_SNAKE_MAX)
        self.body.append(self.position)
        for _ in range(1, self.LEN_SNAKE_START):
            self.increase_length()

    def __contains__(self, item):
        """ Check if a snake is colliding with another snake.  """
        return bool(set(item.body) & set(self.body))

    def __eq__(self, other):
        """ Check if the snake is the same one, by checking all body positions.  """
        if hasattr(other, "body"):
            return not (set(self.body) - set(other.body))
        return False

    def __ne__(self, other):
        """ Check if the snake is not the same one, by checking all body positions.  """
        if hasattr(other, "body"):
            return bool(set(self.body) - set(other.body))
        return False

    def __len__(self):
        return len(self.body)

    def __str__(self):
        return f"<class {self.__class__.__name__}"

    def __repr__(self):
        return f"<class {self.__class__.__name__} (x={self.position.x}, y={self.position.y})>"

    def specifics(self):
        """ Returns a lot of information about the snake.  """
        return dict(alive=self.alive, facing=self.direction,
                    length=len(self), body=self.body,
                    head=self.get_head(), tail=self.get_tail(),
                    time_left=self.life_left, time_alive=self.life_time)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        """
            Only set the value if it is a valid direction and
            you do not try to return in the opposite direction(against the body)

            :param value: int
                New direction of the snake
        """
        if value in constants.DIRECTION_VALID:
            value_current = constants.DIRECTION_VALUE.get(self.direction)
            value_new = constants.DIRECTION_VALUE.get(value)
            if value_current != -value_new:
                self._direction = value

    def get_head(self):
        """ Returns the head position of the snake.  """
        return self.body[0]

    def get_tail(self):
        """ Returns the tail position of the snake.  """
        return self.body[-1]

    def increase_length(self):
        """
            Will increase the length of the snake on the next step.
        """
        self.body.append(self.body[-1])
        self.life_left = min(self.life_left + self.APPLE_TIME, self.LIFE_MAX)

    def step(self):
        """
            Updates the snake position to the new head location
        """
        new_head = self.next_step_head()
        self.body.pop()

        self.body.appendleft(new_head)
        self.position = self.get_head()

        self.life_time += 1
        self.life_left -= 1

    def next_step_head(self):
        """
            Calculates the position of the snake after a step

            :return: Point
                New location of the head
        """
        new_head = self.body[0].clone()
        if self.direction in ["LEFT", "RIGHT"]:
            new_head.x += 1 if self.direction == "RIGHT" else -1

        if self.direction in ["UP", "DOWN"]:
            new_head.y += 1 if self.direction != "UP" else -1

        return new_head

    def collide(self, other):
        """
            Check if a point collide with the snakes body

            :param other: Point
        """
        for body in self.body:
            if body == other.position:
                return True
        return False

    def location(self):
        return self.body

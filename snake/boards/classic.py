import numpy as np

from .base_board import BaseBoard
from snake.objects.wall import Wall
from snake.objects.ground import Ground
from snake.objects.snake import Snake
from snake.objects.apple import Apple
from snake.objects.utils import Point

from snake import constants


class Board(BaseBoard):
    """
        Controls the setup of the snake and the objects on the board.

        :param width: int
            The width of the board
        :param height: int
            The height of the board
    """

    def __init__(self, width=None, height=None):
        self.width = width if width is not None else constants.WIDTH
        self.height = height if height is not None else constants.HEIGHT
        self.board = self._create_board(self.width, self.height)

        # Keeps track of all the objects in the game
        self.objects = dict(ground=[], wall=[], snake=[], apple=[])
        self.object_types = dict(ground=Ground, wall=Wall, snake=Snake, apple=Apple)

        # placeholder for the actual gym step return variables
        self._obs = np.zeros((self.width, self.height), dtype=np.object)
        self._reward = []
        self._done = False
        self._info = dict()
        self._seed = None

        self.action_space = constants.ACTION_SPACE
        self.action_set = constants.GET_ACTION_MEANING

    def __str__(self):
        return "<class Board>"

    def __repr__(self):
        return f"<class Board (np.array(width={self.width}, height={self.height}), dtype=np.object)"

    def setup(self, snakes=1, apples=1, walls=0):
        """
            init settings for starting the board

            :param snakes: int
                The number of snakes that will randomly spawn on the board
            :param apples: int
                The number of apples that will randomly spawn on the board
            :param walls: int
                The number of walls that will randomly spawn
        """
        snakes = snakes if snakes > 1 else constants.DEFAULT_START_SNAKES
        apples = apples if apples > 1 else constants.DEFAULT_START_APPLES
        walls = walls if walls > 0 else constants.DEFAULT_START_WALLS

        self.board = self._create_board(self.width, self.height)
        for k, v in self.objects.items():
            self.objects[k] = []

        for name, numbers in [("snake", snakes), ("apple", apples), ("wall", walls)]:
            for _ in range(numbers):
                self.add_object(name)

    def add_object(self, name, position=None):
        """
            Add an object to the board

            :param name: str
                Name of the object you want to add, valid options are currently
                'wall', 'snake', 'ground', 'apple'

            :param position: Point
                Defines the position of the object on the board, if none is provided
                it will pick a random position on the board
        """
        start_pos = position if position is not None else self._random_point()

        if self.object_types.get(name.lower().strip(), None):
            new_object = self.object_types.get(name.lower().strip())(start_pos)

            if not self._collision_new_object(new_object):
                self.objects[name].append(new_object)
                self.board[start_pos.x, start_pos.y] = new_object
            else:
                options = self._locate_object(Ground)
                if not options:
                    raise ValueError("No space to put the new object.")
                new_pos = np.random.choice(range(len(options)))
                self.add_object(name, position=Point(*options[new_pos]))
        else:
            raise ValueError(f"Object '{name}' not familiar")

    def obs(self, attribute="rgb"):
        """ Returns the game grid.

            :param attribute: str
                The attribute of the objects inside the game of what has to returned,
                valid inputs are: ['rgb', 'ansi', 'ansi_fancy']
        """
        for x in range(self.width):
            for y in range(self.height):
                self._obs[x, y] = getattr(self.board[x, y], attribute)
        return self._obs

    def reward(self):
        """ Returns the reward for a single step.  """
        return sum(self._reward)

    def done(self):
        """ Returns a boolean if the game is over or not. (True is game over) """
        living_snakes = [snake for snake in self.objects['snake'] if snake.alive]
        if not living_snakes:
            return True
        return False

    def info(self):
        """ Returns additional info about the game.  """
        info = dict()
        living_snakes = [snake for snake in self.objects['snake'] if snake.alive]

        info["snakes_alive"] = len(living_snakes)
        info["snakes_dead"] = len(self.objects['snake']) - len(living_snakes)
        info["life_left"] = [snake.life_left for snake in living_snakes]
        info["direction"] = [snake.direction for snake in living_snakes]
        return info

    def step(self, action, values=True):
        """ Executes a step in the game.

            :param action: int
                The action that has to be performed
            :param values: bool
                If the game is used as a standalone it has to return gym actions.
                But sometimes we want to get different observations and then
                disabling the return values saves a lot of time.
        """
        self._step(action)
        if values:
            return self.obs(), self.reward(), self.done(), self.info()
        return None

    def reset(self):
        """ Reset the environment.  """
        self.setup()
        return self.obs()

    def close(self):
        """ Performs a clean sweep of the game when closed.  """
        self.setup()

    def random_step(self):
        """ Returns a random step in the environment.  """
        return np.random.choice(range(self.action_space))

    def seed(self, seed=None):
        """
            Either restores a seed if a seed list is given, otherwise
            returns the seed that is initialized in this game.
        """
        if seed is None:
            self._seed = np.random.get_state()
        else:
            self._seed = seed[0]
            np.random.set_state(self._seed)
        return [self._seed]

    def get_screen_dimensions(self):
        """ Returns the width and height of the board.  """
        return self.width, self.height

    @staticmethod
    def _create_board(width, height):
        """
            Creates a numpy array with only ground objects, can be populated by
            other Objects
        """
        board = np.zeros((width, height), dtype=np.object)

        for x in range(width):
            for y in range(height):
                border_row = (y % (height - 1)) == 0
                border_col = (x % (width - 1)) == 0

                if border_row or border_col:
                    board[x, y] = Wall(Point(x, y))
                else:
                    board[x, y] = Ground(Point(x, y))
        return board

    def _locate_object(self, object_type):
        """
            Locates all x, y positions of a type on the playing field.

            :param object_type: Object
                Any object that is located in self.Objects
            :return: list(int, int)
                A list of all the locations of the specific type as tuples
        """
        indices = []
        for x, row in enumerate(self.board):
            for y, item in enumerate(row):
                if isinstance(item, object_type):
                    indices.append((x, y))
        return indices

    def _random_point(self, min_distance=constants.MIN_SPAWN_WALL_DISTANCE):
        """
            Returns a random point on the board at least min_distance away from the sides.

            :param min_distance: int
                The minimum distance to the borders of the snake

            :return Point
                A position on the board at least min_distance away from the boarder
        """
        return Point(x=np.random.randint(min_distance, self.width - min_distance),
                     y=np.random.randint(min_distance, self.height - min_distance))

    def _collision_new_object(self, new_object):
        """
            Test for collision between the new object and objects already on the board.

            :param new_object: Object
            :return bool
                True upon collision and False otherwise
        """
        if not isinstance(self.board[new_object.position.as_value()], Ground):
            return True
        return False

    def _step_snake(self, snake):
        """
            Test for collisions and handles interaction, should be called after a step.

            :return int
                Returns the reward value obtained in the step
        """
        new_head_location = snake.next_step_head()
        new_position_board = self.board[new_head_location.as_value()]

        # If crashed
        wall_hit = isinstance(new_position_board, Wall)
        snake_hit = isinstance(new_position_board, Snake)
        time_up = snake.life_left <= 0
        if wall_hit or snake_hit or time_up:
            self._collision_dead(snake)
            return 0

        # If apple is eaten
        next_is_apple = isinstance(new_position_board, Apple)
        if next_is_apple:
            self._reward.append(constants.DEFAULT_REWARD_PER_APPLE)
            self._collision_apple(snake, new_head_location)

        if not next_is_apple or len(snake) > snake.LEN_SNAKE_MAX:
            # Remove tail if apple is not eaten and no more object following it
            if len(snake) > 1 and snake.body[-2] != snake.get_tail():
                self.board[snake.get_tail().as_value()] = Ground(snake.get_tail())

        # Reward for every step
        self._reward.append(constants.DEFAULT_REWARD_PER_STEP)

        # If snake still lives update head position
        if snake.alive:
            snake.step()
            self.board[snake.get_head().as_value()] = snake

    def _step(self, action: int):
        """ Perform step function for all living snakes.  """
        self._reward = []
        living_snakes = [snake for snake in self.objects['snake'] if snake.alive]

        for snake in living_snakes:
            snake.direction = self.action_set[action]
            self._step_snake(snake)

    def _collision_apple(self, snake, position):
        """
            Handles interaction between a collision of an apple and a snake

            :param snake: Snake
        """
        snake.increase_length()
        to_remove = Apple(position)
        self.objects['apple'].remove(to_remove)
        self.add_object("apple")

    def _collision_dead(self, snake):
        """
            Handles interaction between a collision that kills a snake.

            :param snake: Snake
        """
        snake.alive = False

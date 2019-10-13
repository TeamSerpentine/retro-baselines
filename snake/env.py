import gym
import itertools
import numpy as np

from snake.objects.utils import Point
from snake.game import SnakeGame


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human', 'ansi', 'ansi_fancy', 'rgb_array', 'gen']}

    def __init__(self, game="snake", mode='human', obs_type="image", width=None, height=None, scale=None):
        self.game = game
        self.env = SnakeGame(width, height)

        self._scale = scale
        self._obs_type = obs_type
        self._mode = mode
        self._action_set = self.env.board.action_set
        self._obs_store = None

        # If the image has to be scaled pre allocated array.
        if scale is not None:
            self._image = self._get_image_dimension()

        self.action_space = gym.spaces.Discrete(len(self._action_set))
        self.observation_space = self._get_observation_space()
        self.env.obs = self._get_obs(self._mode)
        self.viewer = None

    def _get_observation_space(self):
        """ Define the observation space depending on the observation type.  """
        (screen_width, screen_height) = self.env.board.get_screen_dimensions()
        if self._obs_type == 'gen':
            observation_space = gym.spaces.Box(low=0, high=max(screen_width, screen_height), shape=(24,),
                                               dtype=np.uint8)
        elif self._obs_type == 'image':
            observation_space = gym.spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3),
                                               dtype=np.uint8)
        elif self._obs_type == 'text':
            observation_space = gym.spaces.Discrete(self.env.board.action_space)
        else:
            raise gym.error.Error('Unrecognized observation type: {}'.format(self._obs_type))
        return observation_space

    def _get_obs(self, mode):
        """ For different modes returns different obs functions.  """
        if mode == 'gen':
            env_obs = self._observation_genetic
        elif mode in ['rgb_array', 'human']:
            env_obs = self._observation_rgb
        elif 'ansi' in mode:
            env_obs = self._observation_ansi
        else:
            raise gym.error.Error('Unrecognized mode type: {}'.format(mode))
        return env_obs

    def _get_image_dimension(self):
        """ Pre allocates new image space and maintains aspect ratio while clipping at width=500, height=500.  """
        scale = 1
        obs = self.env.reset()
        width, height = obs.shape
        while width * scale < 500 and height * scale < 500 and scale < self._scale:
            scale += 1
        self._scale = self._scale if self._scale <= scale else scale - 1
        return np.zeros((height * self._scale, width * self._scale, 3), dtype=np.uint8)

    def seed(self, seed=None):
        return self.env.seed(seed)

    def step(self, action: int):
        self._obs_store, reward, done, info = self.env.step(action)
        return self._obs_store, reward, done, info

    def reset(self):
        return self.env.reset()

    def _get_image(self):
        """ Get the image from the game, if already stored, return that one instead.  """
        if self._obs_type == "image" and self._obs_store is not None:
            return self._obs_store
        return self._observation_rgb()

    def render(self, mode='human'):

        # Return the image
        if mode == "rgb_array":
            return self._get_image()

        # Render the image in a screen and return the state of the viewer
        if mode == 'human':
            img = self._get_image()

            if self.viewer is None:
                from gym.envs.classic_control import rendering
                self.viewer = rendering.SimpleImageViewer()

            if self._scale:
                img = self._observation_rgb_scaled(img)

            self.viewer.imshow(img)
            return self.viewer.isopen

        # Render the game in console and return img string
        if mode.startswith('ansi'):
            img = self._observation_ansi()
            print(img)
            return img

        raise ValueError(f"The selected mode: '{mode}' is not available pick any from {self.metadata['render.modes']}")

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None

    def _observation_genetic(self):
        """
            Generates the output array.
            The output will be a (24,) numpy array, with 3 times 8 directions.

            wall distance, snake distance, food distance
            ["UP", "DOWN", "LEFT", "LEFT UP", "LEFT DOWN", "RIGHT", "RIGHT UP", "RIGHT DOWN"]
        """
        object_types = [v for k, v in self.env.board.object_types.items() if k != "ground"]
        obs_directions = [x for x in itertools.product([0, 1, -1], repeat=2)][1:]
        obs_out = np.zeros((len(self.env.board.objects['snake']), len(object_types), len(obs_directions)), dtype=np.int)

        for idx_snake, snake in enumerate(self.env.board.objects['snake']):
            for idx_direction, direction in enumerate(obs_directions):
                scan_direction = Point(*direction)
                object_found = False
                scan_counter = 1
                while not object_found:
                    scan_x = snake.position.x + scan_direction.x * scan_counter
                    scan_y = snake.position.y + scan_direction.y * scan_counter
                    for idx_object, object_type in enumerate(object_types):
                        if isinstance(self.env.board.board[scan_x, scan_y], object_type):
                            obs_out[idx_snake, idx_object, idx_direction] = scan_counter
                            object_found = True
                    scan_counter += 1
        return obs_out.flatten()

    def _observation_ansi(self):
        """ Returns a string of the game.  """
        obs = self.env.board.obs(attribute=self._mode)
        return "\n".join(map(str, ["".join(row.tolist()) for row in obs]))

    def _observation_rgb(self):
        """ Returns a numpy array with rgb values of shape (board.width, board.height, 3).  """
        obs = self.env.board.obs()
        for x in range(obs.shape[0]):
            for y in range(obs.shape[1]):
                self.env.image[x, y] = obs[x, y]
        return np.transpose(self.env.image, axes=(1, 0, 2))

    def _observation_rgb_scaled(self, observation):
        """ Returns a scaled version of the _observation_rgb.  """
        width = observation.shape[0]
        height = observation.shape[1]
        for x in range(0, self._scale):
            for y in range(0, self._scale):
                self._image[y:width * self._scale:self._scale,
                x:height * self._scale:self._scale] = observation
        return self._image

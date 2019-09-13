


import unittest

from utils.suppress import suppress_stdout
from snake.games.snake_v0 import Snake


class TestSnakeGen(unittest.TestCase):

    def setUp(self) -> None:
        self.env = Snake()

    def test_gen_run(self):
        for _ in range(10):
            self._run_game(self.env, render=False)

    def test_gen_run_render(self):
        for _ in range(2):
            self._run_game(self.env, render=True)

    def test_gen_obs_dimension(self):
        obs = self.env.reset()
        self.assertEqual(31+32*42, len(obs), "Observation dimension is not as expected")
        self.assertEqual(True, type(obs) == str, "Observation type is not as expected")

    def _run_game(self, env, render=False):
        env.reset()
        done = False
        while not done:
            obs, reward, done, info = env.step(env.action_space.sample())
            if render:
                # Prevent console output during render tests
                with suppress_stdout():
                    env.render()
        env.close()



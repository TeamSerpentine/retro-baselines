
import unittest
import numpy as np

from tools.suppress import suppress_stdout
from snake.env import SnakeEnv


class TestModes(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = {
            'SnakeGen-v0': dict(
                kwargs=dict(game=id, mode='gen', obs_type='gen', width=32, height=42, scale=5),
                shape=(24,),
                dtype=np.int
            ),

            'SnakeGen-v1': dict(
                kwargs=dict(game=id, mode='gen', obs_type='gen', width=16, height=21, scale=10),
                shape=(24,),
                dtype=np.int
            ),

            'Snake-v0': dict(
                kwargs=dict(game=id, mode='human', width=32, height=42, scale=5),
                shape=(42, 32, 3),
                dtype=np.uint8,
            ),

            'Snake-v1': dict(
                kwargs=dict(game=id, mode='ansi', obs_type='text', width=32, height=42, scale=5),
                type=str,
                shape=(32, 42),
            ),

            'Snake-v2': dict(
                kwargs=dict(game=id, mode='ansi_fancy', obs_type='text', width=32, height=42, scale=5),
                type=str,
                shape=(32, 42),
            ),

        }

    def test_gen_run(self):
        for key, value in self.settings.items():
            env = SnakeEnv(**value['kwargs'])
            for _ in range(10):
                self._run_game(env, render=False)

    def test_gen_run_render(self):
        for key, value in self.settings.items():
            env = SnakeEnv(**value['kwargs'])
            for _ in range(2):
                self._run_game(env, render=True)

    def test_gen_obs_dimension(self):
        for key, value in self.settings.items():
            env = SnakeEnv(**value['kwargs'])
            obs = env.reset()

            if hasattr(obs, "shape"):
                self.assertEqual(value['shape'], obs.shape, f"Observation dimensions {key} is not as expected")
                self.assertEqual(value['dtype'], obs.dtype, f"Observation type {key} is not as expected")
            else:
                self.assertEqual(True, isinstance(obs, value['type']), f"Observation dimensions {key} is not as expected")
                # Convert the strings to a numpy grid
                obs = np.array([[*each] for each in obs.split("\n")])
                self.assertEqual(value['shape'], obs.shape, f"Observation dimensions {key} is not as expected")

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

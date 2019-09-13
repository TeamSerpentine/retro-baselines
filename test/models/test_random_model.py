"""
Test script for random_model.py.
"""

import gym
import unittest
import tempfile
from models.random_model import RandomModel


class TestRandomModel(unittest.TestCase):
    """
        Test class for the RandomModel class.
    """

    def setUp(self):
        self.in_space = [10, 10]
        with tempfile.TemporaryDirectory() as tmpdirname:
            name = "Pong-v0"
            self.env = gym.make(name)
            self.model = RandomModel(name, self.in_space, self.env.action_space, tmpdirname)

    def test_init(self):
        """
            Test RandomModel initialization.
        """
        self.assertEqual(self.env.action_space, self.model.action_space)
        self.assertEqual(self.in_space, self.model.input_shape)

    def test_action(self):
        """
            Test if calling action return variables between correct boundaries.
        """
        for call in range(100):
            action = self.model.action(call)
            self.assertGreater(self.env.action_space.n, action)
            self.assertLessEqual(0, action)

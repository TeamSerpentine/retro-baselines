"""
Test script for insertcoin.py
"""
import gym
import unittest
from insertcoin import InsertCoin
from models.random_model import RandomModel
from utils.suppress import suppress_stdout


class TestInsertCoin(unittest.TestCase):
    """
    Testing class for the InsertCoin class.
    """
    def setUp(self):
        """
        Set-up for data fixtures per test .
        """
        with suppress_stdout():
            self.runner = InsertCoin(run_main=False)
            self.game_name, self.game_mode, self.render, \
                self.step_limit, self.game_limit, self.clip, self.log = self.runner._args()

    def test_arg_parser_minimal(self):
        """
        Test if default inits are initialized in reasonable bounds
        """
        self.assertIsNotNone(self.game_name)
        self.assertIsNotNone(self.game_mode)
        self.assertIsNotNone(self.render)
        self.assertIsNotNone(self.clip)
        self.assertIsNotNone(self.log)
        self.assertLess(0, self.step_limit)
        self.assertLess(0, self.game_limit)

    def test_arg_parser_types(self):
        """
        Test for correct types in default argparser values.
        """
        self.assertIsInstance(self.game_name, str)
        self.assertIsInstance(self.game_mode, str)
        self.assertIsInstance(self.render, bool)
        self.assertIsInstance(self.clip, bool)
        self.assertIsInstance(self.log, bool)
        self.assertIsInstance(self.step_limit, int)
        self.assertIsInstance(self.game_limit, int)

    def test_model(self):
        """
        Test if model function returns correct model types.
        """
        env = gym.make("Pong-v0")
        self.assertIsInstance(self.runner._model("random_model", "Pong-v0", env.reset().size, env.action_space),
                              RandomModel)

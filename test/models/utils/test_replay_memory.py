"""
Test script for the ReplayMemory
"""

import unittest
from models.utils.replay_memory import ReplayMemory
import numpy as np


class DummyTupleGenerator:

    def __init__(self, input_shape, action_space):
        self.state_number = 0
        self.last_action = 0
        self.input_shape = input_shape
        self.action_space = action_space

    def get_next_tuple(self):
        next_tuple = (self._get_state(self.state_number),
                      self._get_action(),
                      self._get_reward(self.state_number),
                      self._get_state(self.state_number + 1),
                      self._get_done(self.state_number))

        self.state_number += 1
        return next_tuple

    def _get_action(self):
        if self.last_action + 1 > self.action_space:
            self.last_action = 0
        else:
            self.last_action += 1
        return self.last_action

    def _get_state(self, state_nr):
        return state_nr * np.ones(self.input_shape)

    @staticmethod
    def _get_reward(state_nr):
        return state_nr

    @staticmethod
    def _get_done(state_nr):
        return state_nr % 100 == 0


class TestReplayMemory(unittest.TestCase):
    """
    Testing class for the InsertCoin class.
    """

    def setUp(self):
        """
        Set-up for data fixtures per test .
        """
        memory_length = 500
        input_shape = (20, 20, 1)
        action_space = 4
        self.dummy_agent = DummyTupleGenerator(input_shape, action_space)
        self.memory = ReplayMemory(memory_length, input_shape, action_space)

    def test_remember(self):
        """"
        Test if the remember function works correctly.
        """
        self.memory.remember(*self.dummy_agent.get_next_tuple())
        self.memory.remember(*self.dummy_agent.get_next_tuple())
        self.memory.remember(*self.dummy_agent.get_next_tuple())

    def test_get(self):
        """"
        Test if the correct items are returned.
        """
        first_tuple = self.dummy_agent.get_next_tuple()
        self.memory.remember(*first_tuple)

        # Store a tuple inside the memory to check later.
        second_tuple = self.dummy_agent.get_next_tuple()
        self.memory.remember(*second_tuple)

        # Add another tuple
        last_tuple = self.dummy_agent.get_next_tuple()
        self.memory.remember(*last_tuple)

        self.assertEqual(self.memory[0], first_tuple)
        self.assertEqual(self.memory[1], second_tuple)
        self.assertEqual(self.memory[2], last_tuple)
        self.assertEqual(self.memory[-1], last_tuple)

    def test_set(self):
        """"
        Test if the correct items are set.
        """
        self.memory.remember(*self.dummy_agent.get_next_tuple())
        self.memory.remember(*self.dummy_agent.get_next_tuple())
        self.memory.remember(*self.dummy_agent.get_next_tuple())

        self.memory[1] = (0, 1, 2, 3, 4)

        self.assertEqual(self.memory[1], (0, 1, 2, 3, 4))

    def test_length(self):
        """"
        Test if the correct length is shown.
        """
        self.memory.remember(*self.dummy_agent.get_next_tuple())
        self.memory.remember(*self.dummy_agent.get_next_tuple())
        self.memory.remember(*self.dummy_agent.get_next_tuple())
        self.assertEqual(len(self.memory), 3)

    def test_fifo(self):
        """"
        Test if the first in first out principle holds for the memory.
        """
        for _ in range(505):
            self.memory.remember(*self.dummy_agent.get_next_tuple())

        self.assertEqual(self.memory[0][2], 5)
        self.assertEqual(self.memory[499][2], 504)

    def test_next_prev(self):
        """"
        Test if the next state item in tuple x corresponds to state in tuple x+1
        """
        for _ in range(500):
            self.memory.remember(*self.dummy_agent.get_next_tuple())

        for idx in range(490):
            self.assertTrue(np.all(self.memory[idx][3] == self.memory[idx + 1][0]))

    def test_random_sample(self):
        """"
        Test if the random sample function returns the correct number of tuples, and whether these tuples exists.
        """
        pass

    def test_load(self):
        """"
        Test the load function for the ReplayMemory.
        """
        pass

    def test_save(self):
        """"
        Test the save function for the ReplayMemory.
        """
        pass

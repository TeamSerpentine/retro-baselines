"""
Test script for decay_policies.py.
"""

import unittest
from models.tools.decay_policies import *


class TestDecayPolicies(unittest.TestCase):
    """
    Test class for the BaseModel class.
    """

    def test_linear_decay(self):
        """
        Test the properties of the linear decay policies.
        """
        start = 0
        end = 1000
        max_value = 1
        min_value = 0.1
        policy = LinearDecayCutOff(start, end, max_value, min_value)

        self.assertEqual(max_value, policy.get(-1))

        # Testing bounds
        self.assertAlmostEqual(max_value, policy.get(start), 5)
        self.assertAlmostEqual(min_value, policy.get(end), 5)

        # Outside bounds
        self.assertAlmostEqual(max_value, policy.get(start - 10), 5)
        self.assertAlmostEqual(min_value, policy.get(end + 10), 5)

        # In between
        self.assertAlmostEqual(0.325, policy.get(start + (end - start) * 0.25), 5)
        self.assertAlmostEqual(0.550, policy.get(start + (end - start) * 0.50), 5)
        self.assertAlmostEqual(0.775, policy.get(start + (end - start) * 0.75), 5)

    def test_exponential_decay(self):
        """
        Test the properties of the exponential decay policies.
        """
        decay = 0.95
        max_value = 1
        min_value = 0.1
        policy = ExponentialDecay(decay, max_value, min_value)

        # Testing bounds
        self.assertAlmostEqual(max_value, policy.get(0), 5)
        self.assertAlmostEqual(min_value, policy.get(44.89056748), 5)

        # Outside bounds
        self.assertAlmostEqual(min_value, policy.get(60), 5)

        # In between
        self.assertAlmostEqual(0.25, policy.get(27.026814668), 5)
        self.assertAlmostEqual(0.50, policy.get(13.513407334), 5)
        self.assertAlmostEqual(0.75, policy.get(5.6085707866), 5)

    def test_linear_decay_simple(self):
        min_value = 0
        max_value = 100
        steps = 10
        policy = LinearDecay(min_value, max_value, steps)

        # Testing bounds
        self.assertEqual(max_value, policy.get(0), "Incorrect value at step is 0")
        self.assertEqual(min_value, policy.get(11), "Incorrect value at step is 11")

        # Outside bounds
        self.assertEqual(min_value, policy.get(60), "Not set to min value")

        # In between
        self.assertEqual(70, policy.get(3), "Not set to min value")
        self.assertEqual(50, policy.get(5), "Not set to min value")
        self.assertEqual(30, policy.get(7), "Not set to min value")

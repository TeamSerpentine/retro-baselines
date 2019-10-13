"""
Test script for weight_set.py.
"""
import unittest
import numpy as np
np.random.seed(1234)
from copy import deepcopy
from models.tools.weight_set import WeightSet

initializations = ['random', 'glorot_normal',
                   'glorot_uniform',
                   'he_normal', 'he_uniform',
                   'lecun_normal', 'lecun_uniform']


class TestWeightSet(unittest.TestCase):
    """
        Test class for the WeightSet class.
    """
    def setUp(self):
        """
            Setup WeightSet for every test
        """
        # Initialize random layers and sizes
        model_depth = np.random.randint(3, 10)
        self.layer_sizes = [int(np.random.randint(2, 50)) for _ in range(model_depth)]
        # Output size must be smaller than last hidden layer
        self.output_size = np.random.randint(1, self.layer_sizes[-1])
        self.weightset = WeightSet(layer_sizes=self.layer_sizes + [self.output_size])

        # Save input size for testing
        self.input_size = self.layer_sizes[0]

    def reset(self):
        """
            Initialize arbitrary WeightSet
        """
        # Initialize random layers and sizes
        model_depth = np.random.randint(3, 10)
        self.layer_sizes = [np.random.randint(2, 50) for _ in range(model_depth)]
        # Output size must be smaller than last hidden layer
        self.output_size = np.random.randint(1, self.layer_sizes[-1])
        self.weightset = WeightSet(layer_sizes=self.layer_sizes + [self.output_size])

        # Save input size for testing
        self.input_size = self.layer_sizes[0]

    def test_clone(self):
        """
            Test cloning (deepcopy)
        """
        clone = self.weightset.clone()
        # Test if they are not the same instance
        self.assertNotEqual(self.weightset, clone)

        # Test if arguments are the same
        self.assertEqual(self.weightset.layer_sizes, clone.layer_sizes)
        self.assertEqual(self.weightset.activation, clone.activation)
        self.assertEqual(self.weightset.initialization_name, clone.initialization_name)

        # Test if deepcopy argument change does not change original
        clone.activation = 'foo'
        clone.layer_sizes = [-999, -999]
        clone.initialization_name = 'foo'
        self.assertNotEqual(self.weightset.activation, clone.activation)
        self.assertNotEqual(self.weightset.activation, clone.activation)
        self.assertNotEqual(self.weightset.initialization_name, clone.initialization_name)

    def test_randn_init(self):
        """
            Test random initialization of weights
        """
        for _ in range(1000):
            self.reset()
            self.assertIsInstance(self.weightset.weights, np.ndarray)

    def test_feedforward(self):
        """
            Test the feedforward method
        """
        for _ in range(100):
            # Get random set of weights
            self.reset()
            # The feedforward pass must work on all activation functions
            for act_func in self.weightset.activation_dir.values():
                self.weightset.activation = act_func

                # Make feedforward pass
                model_input = np.random.uniform(-999, 999, self.input_size)
                output = self.weightset.feedforward(model_input)

                # Output must be an integer
                self.assertIsInstance(output, np.int64)

    def test_mutate(self):
        """
            Test if mutate changes the weights in-place
        """
        for _ in range(1000):
            mutation_probability = np.random.uniform(0.00001, 1)
            weights_before = deepcopy(self.weightset.weights)
            self.weightset.mutate(mutation_probability)
            weights_after = self.weightset.weights
            # Weights cannot be the same after mutating if mutation_probability > 0
            self.assertNotEqual(weights_before, weights_after)

    def test_crossbreed(self):
        """
            Test if crossbreeding works properly and results in a entirely new WeightSet
        """
        # Get two arbitrary arrays
        for _ in range(1000):
            # Get arbitrary array for crossbreeding
            ws2 = WeightSet(layer_sizes=self.layer_sizes)

            crossbreeded_ws = WeightSet.crossbreed(self.weightset, ws2)

            # Crossbreeded WeightSet cannot be the same as the input instances
            self.assertNotEqual(crossbreeded_ws, self.weightset)
            self.assertNotEqual(crossbreeded_ws, ws2)

            # Crossbreeded weights cannot be the same as either of the initial weights
            self.assertNotEqual(crossbreeded_ws.weights, self.weightset.weights)
            self.assertNotEqual(crossbreeded_ws.weights, ws2.weights)

            # Crossbreeded weightset must be a WeightSet instance
            self.assertIsInstance(crossbreeded_ws, WeightSet)
            self.assertIsInstance(crossbreeded_ws.weights, np.ndarray)

            # Activation function must be the same as the first weightset
            self.assertEqual(self.weightset.activation_name, crossbreeded_ws.activation_name)

    def test_get_init_std(self):
        """
            Test if all initialization schemes are working properly
        """
        # Create arbitrary values for rows and columns
        for _ in range(1000):
            rows = np.random.randint(1, 1000)
            columns = np.random.randint(1, 1000)
            for init in initializations:
                self.weightset.initialization_name = init
                std = self.weightset.get_init_std(rows, columns)
                self.assertIsInstance(std, np.float64)
                self.assertGreater(std, 0)

    def test_activations(self):
        """
            Test all activations that are included in the activation directory
        """
        for _ in range(100):
            # Initialize random weights and get arbitrary layer
            self.weightset.weights = self.weightset.randn_init()
            weight_array = self.weightset.weights[0][0]
            bias_array = self.weightset.weights[0][0]
            for act_func in self.weightset.activation_dir.values():
                result1 = act_func(weight_array)
                result2 = act_func(bias_array)
                self.assertIsInstance(result1, np.ndarray)
                self.assertIsInstance(result2, np.ndarray)

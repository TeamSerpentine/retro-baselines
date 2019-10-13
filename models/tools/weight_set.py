import pickle
from random import random

import numpy as np
from copy import deepcopy


class WeightSet:
    """
        A WeightSet is a set of weights and biases of a model with accompanying operations

        :param layer_sizes: Array of integers
            Indicating the sizes of the (dense) layers, starting at the input layer
            and ending with the output layer

        :param weights: NDArray
            That contains for every layer a list of NDArrays (weight matrix and bias matrix)
            For example, with 2 layers the weights array should have the following structure:
            array([array(weight_matrix1), array(bias_matrix1)],
                  [array(weight_matrix2), array(bias_matrix2)])
            If weights are not specified, WeightSet will randomly initialize weights
            based on layer sizes

        :param activation: str
            The activation function that is used to activate every layer (except the output layer)
            The following activations can be used:
            ['relu', 'leakyrelu', 'elu', 'gelu', 'softplus'].

        :param initialization: str
            The initialization scheme that is used to initialize every layer
            The following initialization schemes can be used:
            ['random', 'glorot_normal', 'glorot_uniform', 'he_normal',
             'he_uniform', 'lecun_normal', 'lecun_uniform']
    """

    def __init__(self, layer_sizes=None, weights=None, activation='relu', initialization='random'):
        """
        Initialize the model based on layer sizes or given weights
        """
        self.layer_sizes = layer_sizes

        # Initialize activation function
        self.activation_name = activation
        self.activation_dir = dict(relu=self.relu,
                                   leakyrelu=self.leakyrelu,
                                   elu=self.elu,
                                   gelu=self.gelu,
                                   softplus=self.softplus)
        self.activation = self.activation_dir[self.activation_name]

        # Save initialization scheme
        self.initialization_name = initialization

        # Use specified weights
        if weights is not None:
            assert isinstance(weights, np.ndarray), 'weights argument needs to be an ndarray'
            self.weights = weights
        else:
            assert self.layer_sizes is not None, 'If no weights are provided, specify layer sizes'
            self.weights = self.randn_init()

    def feedforward(self, observation):
        """
            Use the model to compute which output is taken for a given observation

            :param observation: Array of numbers,
                Namely as many numbers as the initialized input_size
            :return: int
                The number of the action to take. From 0 to the initialized output_size
        """
        x = observation
        # Perform matrix multiplication, bias adding and activation on all layers except the last
        for layer in self.weights[:-1]:
            x = self.activation(np.dot(layer[0], x) + layer[1])
        # Argmax over the last layer to get predicted action
        x = np.argmax(np.dot(self.weights[-1][0], x) + self.weights[-1][1])
        return x

    def clone(self):
        """
            Clone this WeightSet into an identical WeightSet

            :return: A WeightSet with identical weights and biases as this WeightSet
        """
        return deepcopy(self)

    def mutate(self, mutation_probability):
        """
            Mutate this WeightSet's weights and biases
            This mutation is in-place, meaning that it alters its own weights and biases and does not return anything

            :param: mutation_probability: float
                The probability [0,1] for each value to mutate to a random value
        """
        for i, layer in enumerate(self.weights):
            for j, arr in enumerate(layer):
                init_std = self.get_init_std(*arr.shape)
                mutation_values = np.random.normal(loc=0, scale=init_std, size=arr.shape)
                mask = np.random.binomial(1, mutation_probability, arr.shape)
                mutated_arr = np.where(mask, mutation_values, arr)
                # Set the added and clipped weights
                self.weights[i][j] = np.clip(arr + mutated_arr, a_min=-1.0, a_max=1.0)
        return

    @staticmethod
    def crossbreed(first, second):
        """
            Cross-breed two WeightSets to create and return a new one.
            Crossbreeding happens by taking weights from the first WeightSet with 50% probability and
            the remaining weights from the second WeightSet.

            :param first: The first WeightSet to cross-breed
            :param second: The second WeightSet to cross-breed
            :return: A WeightSet resulting from cross-breeding
        """
        new_weight_set = []
        for layer_first, layer_second in zip(first.weights, second.weights):
            # Each layer is a list containing a weight matrix and a bias vector
            new_layer_array = []
            for arr_first, arr_second in zip(layer_first, layer_second):
                assert arr_first.shape == arr_second.shape, 'Both weight matrices need to have the same shape'
                # Do breeding based on mask
                total_size = int(np.prod(arr_first.shape))
                break_point = int(random() * total_size)
                ones = np.ones(break_point)
                zeroes = np.zeros(total_size - break_point)
                mask = np.concatenate((ones, zeroes))
                mask = mask.reshape(arr_first.shape)

                arr_breeded = np.where(mask, arr_first, arr_second)
                new_layer_array.append(arr_breeded)
            new_weight_set.append(new_layer_array)
        breeded_weight_set = np.array(new_weight_set)
        return WeightSet(weights=breeded_weight_set, activation=first.activation_name)

    def randn_init(self):
        """
            Initializes weights and biases from a standard random normal distribution.

            Each element of the initialized array is a list
            with the weight matrix and bias matrix for every layer

            For example, with 2 layers the output will be:
            array([array(weight_matrix1), array(bias_matrix1)],
                  [array(weight_matrix2), array(bias_matrix2)])

            :return: ndarray with weights and biases for every layer
        """
        n_layers = len(self.layer_sizes) - 1
        weight_set = []

        for i in range(n_layers):
            # Get standard deviation that is used to generate random weights
            init_std = self.get_init_std(self.layer_sizes[i + 1], self.layer_sizes[i])
            # Generate arrays
            weight_array = np.random.normal(loc=0, scale=init_std, size=(self.layer_sizes[i + 1], self.layer_sizes[i]))
            bias_array = np.random.normal(loc=0, scale=init_std, size=(self.layer_sizes[i + 1], 1)).ravel()
            layer_array = [np.clip(weight_array, a_min=-1.0, a_max=1.0), np.clip(bias_array, a_min=-1.0, a_max=1.0)]
            weight_set.append(layer_array)
        return np.array(weight_set)

    def get_init_std(self, n_rows, n_columns=1):
        """
            :param n_rows: int
                The number of rows in the tensor
            :param n_columns: int
                The number of columns in the tensor.
                If a vector is passed, columns will be 1.
            :return: The standard deviation for initialization according to the chosen scheme
        """
        # Save initialization scheme
        init_dir = dict(random=np.float64(1.0) / 3,
                        glorot_normal=np.sqrt(2 / (n_rows + n_columns)),
                        glorot_uniform=np.sqrt(6 / (n_rows + n_columns)),
                        he_normal=np.sqrt(2 / n_columns),
                        he_uniform=np.sqrt(6 / n_columns),
                        lecun_normal=np.sqrt(1 / n_columns),
                        lecun_uniform=np.sqrt(3 / n_columns))
        return init_dir[self.initialization_name]

    @staticmethod
    def relu(arr):
        """
            Performs a ReLU (Rectified Linear Unit) activation over an array

            Based on:
            https://arxiv.org/pdf/1803.08375.pdf

            :param arr: An NDArray object
            :return: NDArray
        """
        return np.maximum(0, arr)

    @staticmethod
    def leakyrelu(arr, alpha=0.3):
        """
            Performs a LeakyReLU (Leaky Rectified Linear Unit) activation over an array

            Based on:
            https://arxiv.org/pdf/1803.08375.pdf

            :param arr: An NDArray object
            :param alpha:
            :return: NDArray
        """
        return np.where(arr > 0, arr, arr * alpha)

    @staticmethod
    def elu(arr, alpha=1):
        """
            Performs an elu (Exponential Linear Unit) activation over an array

            Based on:
            https://arxiv.+/1511.07289.pdf

            :param arr: An NDArray object
            :param alpha: float >= 0. Negative slope coefficient.
            :return: NDArray
        """
        return np.where(arr >= 0.0, arr, np.multiply(np.expm1(arr), alpha))

    @staticmethod
    def gelu(x):
        """
            Performs a GELU (Gaussian Error Linear Unit) activation over an array

            Based on:
            https://arxiv.org/pdf/1606.08415.pdf

            :param x: An NDArray object
            :return: NDArray
        """
        cdf = 0.5 * (1.0 + np.tanh((np.sqrt(2 / np.pi) * (x + 0.044715 * np.power(x, 3)))))
        return x * cdf

    @staticmethod
    def softplus(x):
        """
            Performs a Softplus activation over an array.

            Based on:
            https://ieeexplore.ieee.org/document/7280459

            :param x: An NDArray object
            :return: NDArray
        """
        return np.logaddexp(0, x)

    def save(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self.weights, file)

    def load(self, path):
        with open(path, 'rb') as file:
            self.weights = pickle.load(file)

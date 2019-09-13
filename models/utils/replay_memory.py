"""
Replay memory class

This class is used to keep track of the past states, rewards, actions and other information relevant to the game.
Models can retrieve this information on demand.

"""

from collections import deque
import random
import pickle


class ReplayMemory:
    """
    This class is used to keep track of the past states, rewards, actions and other information relevant to the game.
    Models can retrieve this information on demand.

    :param memory_length: The maximum amount of frame tuples in the memory.
    :param input_shape: Shape of the input array.
    :param action_space: Set of actions that are available in the game.
    """

    def __init__(self, memory_length, input_shape, action_space):
        self.memory = deque(maxlen=memory_length)
        self.action_space = action_space
        self.input_shape = input_shape

    def remember(self, state, action, reward, next_state, done):
        """
        Store game step information in internal memory.

        :param state: State of the game.
        :param action: Action taken this frame.
        :param reward: Reward gained this frame.
        :param next_state: State after action has been executed.
        :param done: Game flag. True if game run is over and has to be reset.
        """
        self.memory.append((state, action, reward, next_state, done))

    def get_random_sample(self, sample_size=32):
        """
        Get a random tuple sample from the past array.

        :param sample_size: Total amount of steps taken.
        :return sample: A Numpy array containing sample_size tuples from the ReplayMemory.
        """
        return random.sample(self.memory, sample_size)

    def save(self, path):
        """
        Save the memory for later usage. Useful for restoring checkpoints.

        :param path: Stores the memory for later restoration.
        """
        with open(path, 'wb') as output:
            pickle.dump(self.memory, output, pickle.HIGHEST_PROTOCOL)

    def load(self, path):
        """
        Load the memory to restore your checkpoint.

        :param path: Stores the memory for later restoration.
        """
        with open(path, 'wb') as output:
            self.memory = pickle.load(output, pickle.HIGHEST_PROTOCOL)

    def __getitem__(self, item):
        """"
        Returns a given tuple from the ReplayMemory.

        :param item: Index of the tuple that should be retrieved.
        :return tuple: Tuple containing info about the state, reward, action, next_state and done.
        """
        return self.memory[item]

    def __setitem__(self, key, value):
        """
        Sets the tuple at an index to the given tuple.

        :param key: Index where the tuple should be stored.
        :param value: Tuple that should be stored in the ReplayMemory.
        """
        self.memory[key] = value

    def __len__(self):
        """"
        Returns the number of tuples in the memory

        :return length: The number of stored tuples.
        """
        return len(self.memory)

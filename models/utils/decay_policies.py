"""
Decay policy classes

These classes contain formulas that represent various forms of decay.
They can be used to determine decaying scalars such as epsilon greedy policies or decaying learning rates.

"""

from abc import ABC, abstractmethod


class DecayPolicies(ABC):
    """ The DecayPolicy abstract base class that provides template for creating a mathematical decay formula. """

    @abstractmethod
    def get(self, x):
        """
        Gets the current property value for a given x

        :param x: The input for which the current value should be returned.
        :returns y: The value corresponding to the current input.
        """
        pass


class LinearDecay(DecayPolicies):
    """
        The most basic decay scale, linear interpolation between 2 points.
        Capped on the maximum and minimum values provided in the constructor.

        :param min_value: The input at which the value stops decaying.
        :param max_value: starting value of the decay.
        :param stary_y: The number of steps until it is decayed to the min_value.
    """

    def __init__(self, min_value, max_value, steps):
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.steps = steps
        self.decay_factor = (max_value-min_value) / steps

    def get(self, x):
        """
        Gets the current property value for a given x

        :param x: The input for which the current value should be returned.
        :returns y: The value corresponding to the current input.
        """
        return max(self.max_value - x * self.decay_factor, self.min_value)


class LinearDecayCutOff(DecayPolicies):
    """
        The most basic decay scale, linear interpolation between 2 points.
        Capped on the maximum and minimum values provided in the constructor.

        :param start_x: The input at which the value starts decaying.
        :param end_x: The input at which the value stops decaying (reaches minimum).
        :param start_y: The starting value.
        :param end_y: The value after decaying.
    """

    def __init__(self, start_x, end_x, start_y, end_y):
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

    def get(self, x):
        """
        Gets the current property value for a given x

        :param x: The input for which the current value should be returned.
        :returns y: The value corresponding to the current input.
        """
        if x <= self.start_x:
            return self.start_y
        elif x >= self.end_x:
            return self.end_y
        else:
            return self.start_y + (self.start_y - self.end_y) * (self.end_x - x) / (self.start_x - self.end_x)


class ExponentialDecay(DecayPolicies):
    """
        An exponential decay scale, exponential decay according to N = b * g**t.
        Capped on the minimum value provided in the constructor.

        :param decay: The decay factor g.
        :param start_y: The starting value.
        :param end_y: The minimum value cap, by default -inf.
    """

    def __init__(self, decay, start_y, end_y=-float('inf')):
        self.decay = decay
        self.start_y = start_y
        self.end_y = end_y

    def get(self, x):
        """
        Gets the current property value for a given x

        :param x: The input for which the current value should be returned.
        :returns y: The value corresponding to the current input.
        """
        return max(self.start_y * self.decay ** x, self.end_y)

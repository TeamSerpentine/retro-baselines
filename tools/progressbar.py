import time
import sys
import math

from collections import namedtuple


class Progress:
    """ Print a progress bar with time indication.  """
    __slots__ = ("current", "max", "update_step", "start", "init")

    def __init__(self, *, start=0, maximum=100, update_step=1):
        init = namedtuple("init", ["start", "maximum", "update_step"])
        self.init = init(start=start, maximum=maximum, update_step=update_step)
        self.reset_counter()
        self.__str__()

    def __str__(self):
        if self.max == 0:
            percentage_info = 'In progress 100.0%'
            ratio_info = f"{'%10d' % self.current} steps"
        else:
            percentage = '%6.02f' % round(self.current / self.max * 100, 2)
            percentage_info = f"In progress {percentage}%"
            ratio = f'%{int(math.log10(self.max)) + 1}d'
            ratio_info = f"{ratio % self.current}/{self.max}"

        time_info = f"running {'%6.02f' % round(time.time() - self.start, 2)} seconds"
        sys.stdout.write(f"\r{percentage_info} {time_info} {ratio_info}  ")
        sys.stdout.flush()

    def change_init(self, *, start=0, maximum=100, update_step=1):
        init = namedtuple("init", ["start", "maximum", "update_step"])
        self.init = init(start=start, maximum=maximum, update_step=update_step)
        self.reset_counter()

    def reset_counter(self):
        self.current = self.init.start
        self.max = self.init.maximum
        self.update_step = self.init.update_step
        self.start = time.time()

    def increase(self, increase):
        """ Increase the counter and display all information.  """
        self.current += increase
        if (self.current % self.update_step) == 0:
            self.__str__()
        if self.current == self.max:
            self.done()

    def done(self, value=None):
        self.current = value if value is not None else self.current
        self.__str__()
        print("DONE")

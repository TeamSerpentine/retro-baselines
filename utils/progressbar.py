import time
import sys

from collections import namedtuple


class Progress:
    """ Print a progress bar with time indication.  """
    __slots__ = ("current", "max", "update_step", "start", "init")
    def __init__(self,*, start=0, maximum=100, update_step=1):
        init =  namedtuple("init", ["start", "maximum", "update_step"])
        self.init = init(start=start, maximum=maximum, update_step=update_step)
        self.reset_counter()
        self.__str__()

    def __str__(self):
        percentage = round(self.current/self.max*100, 2)
        sys.stdout.write(f"\rIn progress {str(percentage).rjust(5)}% "
                         f"running {str(round(time.time()-self.start, 2))} seconds"
                         f" {self.current}/{self.max}")
        sys.stdout.flush()

    def change_init(self,*, start=0, maximum=100, update_step=1):
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
            print(" DONE".rjust(10))

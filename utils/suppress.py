
from contextlib import contextmanager
import os
import sys
import codecs

@contextmanager
def suppress_stdout():
    with open(os.devnull, "wb") as devnull:
        old_stdout, sys.stdout = sys.stdout, devnull
        # Fancy characters, require special handling, so we make sure everything is written to utf-8
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
        try:
            yield
        finally:
            sys.stdout = old_stdout

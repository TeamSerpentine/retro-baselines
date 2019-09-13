"""
Base class for game wrappers.

Game wrappers provide a standard interface in order to run games using insertcoin.py.
Wrappers take care of pre-processing steps without having to alter the underlying games.
"""

from base_environment import BaseEnvironment


class BaseGameWrapper:
    """
    Base class for game wrappers.

    Game wrappers provide a standard interface in order to run games using insertcoin.py.
    Wrappers take care of pre-processing steps without having to alter the underlying games.
    """

    def wrap(self, env) -> BaseEnvironment:
        """
        Wrap game and return the wrapped environment for use.

        :param env: Environment to wrap.
        :return: Wrapped environment.
        """
        return env

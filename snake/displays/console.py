

from snake.displays.base_display import BaseDisplay


class Console(BaseDisplay):
    """
        Returns a console output of the snake where the objects are simple
        characters from the keyboard.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def render(self, obs):
        print("".join(obs))

    def close(self):
        pass

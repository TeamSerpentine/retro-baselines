import numpy as np
from tools.suppress import suppress_stdout

# This suppresses the welcome message from pygame
# Hello from the pygame community. https://www.pygame.org/contribute.html
with suppress_stdout():
    import pygame


class Image:
    """
        Shows an image output with pygame and can scale it with a certain factor.

        :param caption: str
            The name of the window that will be opened on rendering
        :param scale_factor: int
            The number of times the image has to be enlarged
    """

    def __init__(self, caption, scale_factor=1):
        self.scale = scale_factor
        self.caption = caption
        self._setup = False

    def _init_pygame(self, width, height, channels, scale, caption):
        """ Helper function to restart pygame if env is closed and you want to reset it.  """
        pygame.init()
        pygame.display.set_caption(caption)

        self._image = np.zeros((width*scale, height*scale, channels), dtype=np.uint8)
        self._display_surface = pygame.display.set_mode((width*scale, height*scale))

    def render(self, obs):
        """
            Shows the observation in pygame.

            :return boolean
                It is True when the pygame window is closed.
        """
        obs = obs.transpose(1, 0, 2)

        # Lazy setup, only when called at rendering.
        if not self._setup:
            self._setup = not self._setup
            width, height, channels = obs.shape
            self._init_pygame(width, height, channels, self.scale, self.caption)

        # Only scale the image if the scaling is more than 1
        if self.scale > 1:
            obs = self._scale_obs(self._image, obs, self.scale)


        pygame.surfarray.blit_array(self._display_surface, obs)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return True
        return False

    @staticmethod
    def _scale_obs(obs, old_obs, scale_factor):
        """
            Scales up the old observation with a predetermined factor in the
            x and y direction. So a (10, 10, 3) with scale_factor 5, will become
            (50, 50, 3).

            :param obs: np.array
                This array will hold the scaled up version of the old_obs array
                This method will crash if the observation can't hold the scaled
                up version.
            :param old_obs: np.array
                The array that has to be scaled up
            :param scale_factor: int
                The factor with which the array is being scaled
        """
        for row, x in enumerate(old_obs):
            for col, y in enumerate(x):
                obs[row*scale_factor:(row+1)*scale_factor,
                    col*scale_factor:(col+1)*scale_factor] = y
        return obs

    def close(self):
        """ Closes pygame and reset the setup value, so it can be restarted on a reset.  """
        pygame.quit()
        self._setup = not self._setup

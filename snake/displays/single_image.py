

import numpy as np

from snake.displays.base_display import BaseDisplay
from utils.suppress import suppress_stdout


with suppress_stdout():
    import pygame


class SingleImage(BaseDisplay):
    """ Returns an image output of the snake. """

    def __init__(self, width, height, scale_factor=1):
        super().__init__(self)
        self.scale_factor = scale_factor
        self.width = width
        self.height = height
        self._setup = False

    def _init_pygame(self, width, height, scale_factor):
        """ Helper function to restart pygame if env is closed and you want to reset it.  """
        pygame.init()
        pygame.display.set_caption('Snakes')

        self._image = np.zeros((width*scale_factor, height*scale_factor, 3),
                               dtype=np.uint8)
        self._display_surface = pygame.display.set_mode((width * scale_factor,
                                                         height * scale_factor))

    def render(self, obs):

        # Lazy starting of rendering
        if not self._setup:
            self._setup = not self._setup
            self._init_pygame(self.width, self.height, self.scale_factor)

        obs = self.scale_obs(self._image, obs, self.scale_factor)
        pygame.surfarray.blit_array(self._display_surface, obs)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

    @staticmethod
    def scale_obs(obs, old_obs, scale_factor):
        """
            Scales up the old observation with a predetermined factor in the
            x and y direction. So a (10, 10) with scale_factor 5, will become
            (50, 50).

            :param obs: np.array
                This array will hold the scaled up version of the old_obs array
                This method will crash if the observation can't hold the scaled
                up version.
            :param old_obs: np.array
                The array that has to be scaled up
            :param scale_factor: int
                The factor with which the array is being scaled
        """
        width = old_obs.shape[0]
        height = old_obs.shape[1]
        for x in range(0, scale_factor):
            for y in range(0, scale_factor):
                obs[y:width*scale_factor:scale_factor,
                    x:height*scale_factor:scale_factor] = old_obs
        return obs

    def close(self):
        pygame.quit()
        self._setup = not self._setup

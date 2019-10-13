import threading
import time

import gym
import numpy as np
from models.tools.display import Image
from models.tools.weight_set import WeightSet


class PlayWeightSet(threading.Thread):
    """
        Thread that renders newly (live) played games with a given WeightSet.
        Supports updating of the WeightSet that the games are being played with.
    """

    def __init__(self, game_name, weight_set: WeightSet, fps=5, scale_factor=5):
        """
        :param game_name: Name of the Gym game to run games of
        :param weight_set: First WeightSet to run games with
        :param fps: Steps/frames per second
        """
        threading.Thread.__init__(self)
        self.game_name = game_name
        self.weight_set = weight_set
        self.weight_set_updated = False
        self.fps = fps
        self.scale_factor = scale_factor

    def update_weightset(self, weight_set):
        """
            Choose a new WeightSet to play games with.
            The current game is ended and a new games is started with the new WeightSet

            :param weight_set: The new WeightSet to play games with
        """
        self.weight_set = weight_set
        self.weight_set_updated = True

    def run(self):
        """
            Main Thread loop.
            Runs games with the current WeightSet indefinitely.
            Cuts of games and starts a new one whenever a new WeightSet is provided.
        """

        env = gym.make(self.game_name)
        prev_time = time.time()
        env.reset()
        display = Image(caption=self.game_name, scale_factor=self.scale_factor)
        closed = False

        while not closed:
            self.weight_set_updated = False
            obs = env.reset()
            done = False
            while not done and not self.weight_set_updated and not closed:
                min_time = prev_time + 1.0 / self.fps
                cur_time = time.time()
                if cur_time < min_time:
                    time.sleep(min_time - cur_time)
                prev_time = cur_time
                closed = display.render(env.render(mode='rgb_array'))
                flattened_obs = np.ravel(obs)
                obs, _, done, _ = env.step(self.weight_set.feedforward(flattened_obs))

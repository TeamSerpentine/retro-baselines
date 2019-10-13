"""
Main file for retro_baselines.

The main file and command line interface for retro_baselines.
"""
import gym
import argparse
import numpy as np

import importlib

import snake  # Required for registering games into gym
from tools.progressbar import Progress
from tools.finder import model_finder


class InsertCoin:
    """
    Class containing retro_baselines command line interface and initial run parameters.
    Use the command line interface to run games using different models.
    Examples can be machine learning based models or perhaps scripted ones.
    """

    def __init__(self, run_main=True):
        game_name, game_mode, render, step_limit, game_limit, clip, log = self._args()
        if game_name not in self._get_all_gym_environments_names():
            valid = '\n  '.join(self._get_all_gym_environments_names())
            raise ValueError(f"Game '{game_name}' not inside gym valid options:\n  {valid}")

        env = gym.make(game_name)
        if run_main:
            self._main_loop(self._model(game_mode, game_name, self._input_shape(env), env.action_space),
                            step_limit, game_limit, env, render, clip, log)

    @staticmethod
    def _main_loop(model, step_limit, game_limit, env, render, clip, log):
        """
            Run main snake loop using the settings from the command line interface or the default settings.

            The main snake loop runs the snake step by step. It is stopped when either the maximum number of games
            or maximum number of steps is reached. During each run of the main loop a model is invoked to perform
            actions in the snake environment. A model is the interface to various kinds of autonomous decision
            making algorithms.

            :param model: Handle for model to run this snake
            :param step_limit: Maximum amount of frames per run.
            :param game_limit: Maximum amount of games per run.
            :param env: Environment handle for the snake.
            :param render: Render flag.
            :param clip: Clip flag. If True, rewards are clipped between -1 and 1.
        """
        progress = Progress(start=0, maximum=step_limit, update_step=1000)
        total_step = 0
        games = 0
        # Looping over multiple games
        while True:
            # Check step and snake limit
            if 0 < game_limit <= games:
                progress.done(value=total_step)
                print("Maximum number of games reached: " + str(game_limit))
                exit(0)

            # Update games counter
            games += 1

            current_state = env.reset()
            step = 0
            score = 0
            while True:
                if step_limit == 0 or total_step <= step_limit:
                    total_step += 1
                    step += 1

                    if render:
                        env.render()

                    action = model.action(current_state)
                    next_state, reward, terminal, info = env.step(action)
                    if clip:
                        np.sign(reward)
                    score += reward

                    model.remember(current_state, action, reward, next_state, terminal)
                    model.step_update(total_step)
                    if terminal:
                        if log:
                            model.save_game(score, step, games)
                        model.finalize_game(score, step, games)
                        break

                    current_state = next_state
                    if (total_step % 1000) == 0:
                        progress.increase(1000)
                else:
                    progress.done(value=step_limit)
                    print("Reached total step limit of: " + str(step_limit))
                    exit(0)

    @staticmethod
    def _input_shape(env):
        if hasattr(env.reset(), "size"):
            return env.reset().shape
        if isinstance(env.reset(), str):
            return 1,
        else:
            raise ValueError("No support for this game")

    def _args(self):
        """
        Command line argument parser.
        """
        parser = argparse.ArgumentParser()
        available_games = self._get_all_environment_names()
        parser.add_argument("-g", "--game",
                            help="Choose from available games: " + str(available_games) + ". Default is 'Snake-v0'.",
                            default="Snake-v0")
        parser.add_argument("-m", "--model", help="Choose from available models: random_model."
                                                  " Default is 'random_model'.", default="random_model")
        parser.add_argument("-tsl", "--total_step_limit", help="Choose how many total steps (frames) "
                                                               "should be performed. "
                                                               "Default is '0 (no limit)'.", default=0, type=int)
        parser.add_argument("-tgl", "--total_game_limit", help="Choose after how many games we should stop. Default is "
                                                               "0 (no limit).", default=0, type=int)
        parser.add_argument("-r", "--render", help="Include if you want to render game.",
                            action="store_true")
        parser.add_argument("-c", "--clip",
                            help="Choose whether we should clip rewards to (0, 1) range. Default is 'True'",
                            action="store_false")
        parser.add_argument("-l", "--log",
                            help="Choose whether we should save game results per game. Default is 'False'",
                            action="store_true")
        args = parser.parse_args()

        print("Selected game: " + str(args.game))
        print("Selected model: " + str(args.model))
        print("Should render: " + str(args.render))
        print("Should clip: " + str(args.clip))
        print("Should log: " + str(args.log))
        print("Total step limit: " + str(args.total_step_limit))
        print("Total game limit: " + str(args.total_game_limit))

        return args.game, args.model, args.render, args.total_step_limit, args.total_game_limit, args.clip, args.log

    def _get_all_environment_names(self):
        """ Returns a list of all the possible games you can make.  """
        all_game_names = self._get_all_gym_environments_names()
        all_game_names.append(self._get_all_custom_environments_names())
        return all_game_names

    @staticmethod
    def _model(game_mode, *args, **kwargs):
        """ Returns an initialized model.

            :param game_mode: str
                Should be either the name of the modules located in the
                models folder or the name of the class inside one of the modules
                located in models.

                In case there are multiple classes inside a module, the first
                one will be selected.
        """
        return model_finder(game_mode)(*args, **kwargs)

    @staticmethod
    def _get_all_gym_environments_names():
        """ Returns a list of all the possible gym games you can make.  """
        all_environments = gym.envs.registry.all()
        all_game_names = [env_spec.id for env_spec in all_environments]
        return all_game_names

    @staticmethod
    def _get_all_custom_environments_names():
        """ Returns a list of all the possible custom games you can make. """
        all_game_names = ["snake"]
        return all_game_names


if __name__ == "__main__":
    InsertCoin()

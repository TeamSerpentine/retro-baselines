"""
    Genetic model.

    Simplified, the Genetic Model runs a (couple of) game(s) for many agents and then combines the best ones to run
    again so the population improves.

    More elaborately, the Genetic Model is a genetic algorithm that uses a population of many agents over multiple
    generations, improving them using elites, cross breeding and mutation in the generation of the next population.
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
from models.base_model import BaseModel
from models.tools.play_weightset import PlayWeightSet
from models.tools.weight_set import WeightSet


class GeneticModel(BaseModel):
    """
        Genetic Model that learns to play games based on a genetic algorithm.

        :param game_name: Name of the current snake.
        :param input_shape: Shape of the input array.
        :param action_space: Set of actions that are available in the snake.
        :param logger_path: Path to the log files.
    """

    POPULATION_SIZE = 500  # Number of different WeightSets to try in each generation
    ELITE_FRACTION = 0.05  # The top percentage of the population to carry over to the next generation
    CROSSOVER_FRACTION = 0.7  # The fraction of new WeightSet (so non-elite) that will be created using crossover.
    # Otherwise it will be a mutation
    MUTATION_PROBABILITY = 0.01  # Probability that a value in a mutated WeightSet will mutate with a random value
    CROSSOVER_MUTATION_PROBABILITY = 0.001  # Probability that a value in a WeightSet resulting from crossbreeding will
    # mutate with a random value
    HIDDEN_LAYERS = [18, 18, 16]  # The sizes of the hidden layers
    GAMES_PER_WEIGHTSET = 4  # Number of games each WeightSet plays in each generation
    PLOT_STATS = True  # Whether to plot stats of each generation
    SAVE_BEST_WEIGHTSETS = True  # Whether to save the best WeightSets of each generation
    SAVE_GEN_SCORES = True  # Whether to save logs of the generation scores of each generation
    RENDER_BEST_WEIGHTSETS = True  # Whether to render (new) games with the best WeightSet of the last finished
    # generation.

    # Directories of logging information (used only if above flags are enabled)
    dir_current = os.path.dirname(os.path.abspath(__file__))
    dir_logs = os.path.join(dir_current, "..", "logs")
    dir_scores = os.path.join(dir_logs, 'scores')
    dir_weightsets = os.path.join(dir_logs, 'weightsets')

    def __init__(self, game_name, input_shape, action_space, logger_path="output/genetic_model"):
        """
            Initialize the population
        """
        # Initialize variables
        self.population = list()  # Set of WeightSets containing the weights of all agents in the current population
        self.scores = list()  # The scores that the WeightSets of the population achieved when running a game
        self.current_weight_set_id = 0  # The index of the WeightSet that is currently playing
        self.generation_id = 0  # The generation number we are currently in
        self.generation_outcomes = list()  # Stores results for each generation
        self.weight_set_score = list()  # The scores of the GAMES_PER_GENERATION games played with one WeightSet

        # Calculate sizes of all layers of the neural net
        input_size = int(np.prod(input_shape))
        output_size = action_space.n
        layer_sizes = [input_size, *self.HIDDEN_LAYERS, output_size]

        # Populate with POPULATION_SIZE nets / WeightSets
        for i in range(self.POPULATION_SIZE):
            self.population.append(WeightSet(layer_sizes))

        # If enabled, create a replayer that plays games with the best WeightSets of the previous generation
        if self.RENDER_BEST_WEIGHTSETS:
            self.replayer = PlayWeightSet(game_name, self.population[0])
            self.replayer.start()

        # Prevent any plots from making the terminal hang
        if self.PLOT_STATS:
            plt.ion()

        # If saving certain logs, make sure the folders for it exists
        if self.SAVE_BEST_WEIGHTSETS or self.SAVE_GEN_SCORES:
            # Make sure the LOGS folder exists
            if not os.path.exists(self.dir_logs):
                os.makedirs(self.dir_logs)
            if self.SAVE_GEN_SCORES:
                # Make sure the SCORES folder exists
                if not os.path.exists(self.dir_scores):
                    os.makedirs(self.dir_scores)
            if self.SAVE_GEN_SCORES:
                # Make sure the WEIGHTSETS folder exists
                if not os.path.exists(self.dir_weightsets):
                    os.makedirs(self.dir_weightsets)

        super().__init__(game_name, input_shape, action_space, logger_path)

    def action(self, state):
        """
            Find the action to take using the currently active WeightSet with the state as input for the WeightSet.

            :param state: State of the game
            :return: Integer corresponding to action to take
        """
        # The WeightSet that is currently playing
        current_weight_set: WeightSet = self.population[self.current_weight_set_id]

        # Flatten the state to 1-dimension in case it was multi dimensional to feed to the network's weights
        input = np.ravel(state)

        # Find the output/action the network with the current WeightSet gives for the current state as input
        action = current_weight_set.feedforward(input)

        return action

    def step_update(self, *kwargs):
        """
            Update model with total amount of steps taken.
            Unused for the genetic model as there is nothing to save after each step.
        """
        pass

    def remember(self, *kwargs):
        """
            Store a game step's information in internal memory.
            Currently unused by the genetic algorithm. May be used later for logging
        """
        pass

    def save_game(self, *kwargs):
        """
            Called at the end of a single game.
            Save this game's information.
            Currently unused by the genetic algorithm. May be used later for logging
        """
        pass

    def finalize_game(self, score, step, run):
        """
            Handle the finishing of a game run by selecting the WeightSet that will run next game.

            First, check whether there are more games to run for the WeightSet that just played a game. If not, then
            another WeightSet is to be selected for the next game.

            If all WeightSets of a generation have been run, compute a new generation and select the first WeightSet.
            Otherwise, activate the next WeightSet.

            :param score: Score of this game run.
            :param step: Amount of steps this run took.
            :param run: Current run number.
        """
        # Save the score the currently running WeightSet scored in the last game
        self.weight_set_score.append(score)

        # Check whether the currently running WeightSet has played enough games for a good average
        if len(self.weight_set_score) >= self.GAMES_PER_WEIGHTSET:
            # Save the average score this WeightSet achieved in its games
            self.scores.append(np.average(self.weight_set_score))

            # Reset the list of scores of games for the currently running WeightSet so the next WeightSet will fill it
            self.weight_set_score = list()

            # Select next WeightSet to be playing now
            self.current_weight_set_id += 1

            # If all WeightSets have played, generate a new generation of WeightSets and start from the first one again
            if self.current_weight_set_id >= self.POPULATION_SIZE:
                self.finalize_generation()
                self.generation_id += 1
                self.current_weight_set_id = 0

    def finalize_generation(self):
        """
            Finalize a generation by generating the population for the next generation and optionally
            saving stats on the generation, updating the graph with those stats and/or updating the
            best WeightSet of last generation to be visualized.
        """
        # Gather and store statistics about this generation
        stats = [
            np.min(self.scores),
            np.quantile(self.scores, 0.25),
            np.average(self.scores),
            np.quantile(self.scores, 0.75),
            np.max(self.scores)
        ]
        stats_formatted = ['%7.02f' % stat for stat in stats]
        print(" " * 4, f"Finalized generation {self.generation_id}",
              f"with scores [MIN, 25%Q, AVG, 75%Q, MAX] = [{', '.join(stats_formatted)}]")
        self.generation_outcomes.append(stats)

        # If enabled, save the stats
        if self.SAVE_GEN_SCORES:
            self.save_stats(stats)

        # Find best WeightSet of this generation
        best_index = np.argmax(self.scores)
        best_weightset = self.population[best_index]

        # If enabled, save the best WeightSet
        if self.SAVE_BEST_WEIGHTSETS:
            best_weightset.save(
                os.path.join('logs', 'weightsets', f'weightset_gen_{self.generation_id}.pickle'))

        # If enabled, update that a new WeightSet of last generation will now be live-played
        if self.RENDER_BEST_WEIGHTSETS:
            self.replayer.update_weightset(best_weightset.clone())

        # If enabled, plot the stats over all generations if wanted
        if self.PLOT_STATS:
            self.plot_stats()

        # Generate the next generation's population
        self.generate_next_generation()

    def generate_next_generation(self):
        """
            With the current generation and the achieved scores of each WeightSet, construct a new set of WeightSets
            to use for the next generation.
        """
        # Create a list for the new population we are creating
        new_population = list()

        # Sort the population based on the achieved scores
        sorted_population = [weight_set for _, weight_set in sorted(zip(self.scores, self.population),
                                                                    key=lambda pair: pair[0], reverse=True)]

        # Calculate how many of elites, crossovers and mutations we will have in the new population
        num_elites = int(self.POPULATION_SIZE * self.ELITE_FRACTION)
        num_crossovers = int((self.POPULATION_SIZE - num_elites) * self.CROSSOVER_FRACTION)
        num_mutations = self.POPULATION_SIZE - num_elites - num_crossovers

        # Let the best elite percentage directly carry over
        new_population.extend(sorted_population[:num_elites])

        # Scale the scores so that together they sum to 1 (used to then sample randomly from it)
        if np.sum(self.scores) <= 0:
            # Prevent division by 0 if no WeightSet achieved any points
            scaled_scores = np.full(self.POPULATION_SIZE, 1.0 / self.POPULATION_SIZE)
        else:
            scaled_scores = np.array(self.scores) / np.sum(self.scores)

        # Cross-overs from 2 parents sampled with probability linked to their score
        for parent1, parent2 in np.random.choice(self.population, p=scaled_scores, size=(num_crossovers, 2)):
            # New child from crossover
            child = WeightSet.crossbreed(parent1, parent2)

            # Also mutate a little bit if wanted
            if self.CROSSOVER_MUTATION_PROBABILITY > 0:
                child.mutate(self.CROSSOVER_MUTATION_PROBABILITY)

            new_population.append(child)

        # Mutate the remainder from current WeightSets sampled with probability linked to their score
        for parent in np.random.choice(self.population, p=scaled_scores, size=num_mutations):
            mutant: WeightSet = parent.clone()
            mutant.mutate(self.MUTATION_PROBABILITY)
            new_population.append(mutant)

        # Replace the old generation's population with the new population (which now does not have a tested score yet)
        self.population = new_population
        self.scores = list()

    def plot_stats(self):
        """
            Plot the statistics over all generations
        """
        # Plot a line for each statistic
        x = range(len(self.generation_outcomes))
        for i in range(len(self.generation_outcomes[0])):
            y = [entry[i] for entry in self.generation_outcomes]
            plt.plot(x, y)

        # Draw and pause so the graph can be interacted with each update
        plt.draw()
        plt.pause(0.0001)

    def save_stats(self, stats):
        """
            Save stats of the current generation to a file in json format
        """
        # Convert stats from np.int64 to normal integers
        stats_ints = [int(stat) for stat in stats]

        # Find the correct file
        file_path = os.path.join(self.dir_scores, f'scores_gen_{self.generation_id}.json')

        # Output the stats to the file
        with open(file_path, 'w') as file:
            file.write(json.dumps(stats_ints))

"""
Test script for genetic_model.py.
"""

import unittest

from mock import patch

from models.genetic_model import GeneticModel
from models.tools.weight_set import WeightSet
import gym
import snake  # Required for registering snake in the gym games list


class TestGeneticModel(unittest.TestCase):

    def setUp(self):
        # Create a environment to test with action space
        self.environment = gym.make("Pong-v0")

        # Turn off logging and auto-rendering as these are not tested currently
        GeneticModel.SAVE_BEST_WEIGHTSETS = False
        GeneticModel.SAVE_GEN_SCORES = False
        GeneticModel.PLOT_STATS = False
        GeneticModel.RENDER_BEST_WEIGHTSETS = False

    def test_init(self):
        """
        Initializing the genetic model should generate the population by creating POPULATION_SIZE
        different WeightSets
        """
        # Generates exactly enough instances in the population
        for population_size in {1, 2, 10, 253, 7102}:
            GeneticModel.POPULATION_SIZE = population_size
            genetic_model = GeneticModel(game_name="SnakeGen-v1", input_shape=(68,),
                                         action_space=self.environment.action_space)
            self.assertEqual(len(genetic_model.population), population_size)

        # Each instance is a WeightSet
        GeneticModel.POPULATION_SIZE = 10
        genetic_model = GeneticModel(game_name="SnakeGen-v1", input_shape=(21,),
                                     action_space=self.environment.action_space)
        for instance in genetic_model.population:
            self.assertIs(type(instance), WeightSet)

        # Each instance is a unique instance
        for i in range(genetic_model.POPULATION_SIZE):
            for j in range(i + 1, genetic_model.POPULATION_SIZE):
                self.assertIsNot(genetic_model.population[i], genetic_model.population[j])

        # Initializes variables correctly
        self.assertEqual(genetic_model.scores, list())
        self.assertEqual(genetic_model.current_weight_set_id, 0)
        self.assertEqual(genetic_model.generation_outcomes, list())
        self.assertEqual(genetic_model.generation_id, 0)

    def test_action(self):
        """
        Make sure the action is gotten from the (correct) active WeightSet by feed-forwarding the input
        """
        GeneticModel.POPULATION_SIZE = 50
        genetic_model = GeneticModel(game_name="SnakeGen-v1", input_shape=(2,),
                                     action_space=self.environment.action_space)
        for i in {0, 4, 10, 24, 49}:
            weight_set = WeightSet(layer_sizes=[2, 4, 5])  # Create a new WeightSet
            genetic_model.current_weight_set_id = i  # Select the i'th WeightSet
            genetic_model.population[i] = weight_set  # Insert our WeightSet in spot i in the population
            inputs = [(i * 17) % 21, (i * 11) % 7]  # Slightly random input

            # Make sure the action gotten from the genetic model is actually the action you get when
            # you feedforward our input in our WeightSet that we injected
            self.assertEqual(genetic_model.action(inputs), weight_set.feedforward(inputs))

    @patch('models.genetic_model.GeneticModel.finalize_generation')
    def test_finalize_game(self, mock_finalize_generation):
        """
        Test whether finalizing a game increases the selected WeightSet to the next one and
        if a generation has finished, that it generates a new generation and increases the generation id
        """
        GeneticModel.POPULATION_SIZE = 50
        genetic_model = GeneticModel(game_name="SnakeGen-v1", input_shape=(2,),
                                     action_space=self.environment.action_space)

        # Make sure weight_set_id increases appropriately including wrapping to the next generation
        for weight_set_id in {0, 4, 10, 24, 49}:
            genetic_model.current_weight_set_id = weight_set_id
            for _ in range(GeneticModel.GAMES_PER_WEIGHTSET):
                genetic_model.finalize_game(5, 6, 7)  # Arbitrary input
            self.assertEqual(genetic_model.current_weight_set_id, (weight_set_id + 1) % GeneticModel.POPULATION_SIZE,
                             "weight_set_id did not increase appropriately")

        # Make sure generation_id increases appropriately when last game of the generation has finished
        for generation_id in {0, 1, 3, 15, 102}:
            genetic_model.generation_id = generation_id
            genetic_model.current_weight_set_id = genetic_model.POPULATION_SIZE - 1
            for _ in range(GeneticModel.GAMES_PER_WEIGHTSET):
                genetic_model.finalize_game(5, 6, 7)  # Arbitrary input
            self.assertEqual(genetic_model.generation_id, generation_id + 1, "Faulty generation id")

        # Make sure finalize_generation is called when a generation is done
        for generation_id in {0, 1, 3, 15, 102}:
            genetic_model.generation_id = generation_id
            genetic_model.current_weight_set_id = genetic_model.POPULATION_SIZE - 1
            call_count = mock_finalize_generation.call_count
            for _ in range(GeneticModel.GAMES_PER_WEIGHTSET):
                genetic_model.finalize_game(5, 6, 7)  # Arbitrary input
            self.assertEqual(mock_finalize_generation.call_count, call_count + 1)

        # Make sure finalize_generation is NOT called when a generation is NOT done
        for weight_set_id in {0, 4, 10, 24, 44}:
            genetic_model.current_weight_set_id = weight_set_id
            call_count = mock_finalize_generation.call_count
            for _ in range(GeneticModel.GAMES_PER_WEIGHTSET):
                genetic_model.finalize_game(5, 6, 7)  # Arbitrary input
            self.assertEqual(mock_finalize_generation.call_count, call_count)

    @patch('models.genetic_model.GeneticModel.generate_next_generation')
    def test_finalize_generation(self, mock_gen_next_gen):
        """
        Test that finalize_generation saves the scores appropriately and calls generate_next_generation
        """
        GeneticModel.POPULATION_SIZE = 50
        genetic_model = GeneticModel(game_name="SnakeGen-v1", input_shape=(2,),
                                     action_space=self.environment.action_space)
        genetic_model.scores = [1, 5, 7]

        # Make sure generate_next_generation is not called before
        mock_gen_next_gen.assert_not_called()

        stats_len = len(genetic_model.generation_outcomes)
        genetic_model.finalize_generation()

        # Make sure generate_next_generation is called
        mock_gen_next_gen.assert_called()

        # Make sure stats are being saved
        self.assertEqual(len(genetic_model.generation_outcomes), stats_len + 1)
        genetic_model.finalize_generation()
        self.assertEqual(len(genetic_model.generation_outcomes), stats_len + 2)

    def finalize_generate_next_generation(self):
        pass

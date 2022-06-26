import copy
import numpy as np

from player import Player


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        # TODO (Additional: Implement roulette wheel here)
        # TODO (Additional: Implement SUS here)

        # TODO (Additional: Learning curve)
        return players[: num_players]

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            # TODO ( Parent selection and child generation )
            new_players = prev_players  # DELETE THIS AFTER YOUR IMPLEMENTATION
            return new_players

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player

    def top_k(self, players, num_players):
        """
        This function select top k players according to their fitness.
        :param players: list of players in the previous generation (NOTE that each player has a fitness attribute)
        :param num_players: number of players that we return
        :return: best k players that have maximum fitness
        """
        k = num_players
        # below method give us sorted players according to their fitness and reverse is rue for descending order
        best_k_palyers = sorted(players, key=lambda x: x.fitness, reverse=True)[: k]
        return best_k_palyers

    def roulette_wheel(self, players, num_players):
        """
        We know that for roulette wheel :
        1- find each player probability
        2- create a ruler that we associate an area for each player proportionate to its probability
        3- create a uniform random number in[0,1] num_players times
        4- according to number that produced last step we should choose a player from ruler
        instead of implementing 2,3,4 step manually we use np.random.choice() function
        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        :return: num_players players according to RW are returned as a
        """
        # step 1
        probabilities = self.fitness_proportionate(players)
        # step 2,3,4
        for i in range(num_players):
            yield np.random.choice(players, num_players, p=probabilities)

    def fitness_proportionate(self, players):
        """
        This function return list of probabilities of players proportionate to their fitness
        :param players: list of players in the previous generation
        :return: list of players probabilities
        """
        # 1- find sum of players' fitness in our population
        total_fitness = 0
        for player in players:
            total_fitness += player.fitness

        # 2- find each player probability proportionate to its fitness
        probabilities = []
        for player in players:
            probabilities.append(player.fitness / total_fitness)

        return probabilities
    
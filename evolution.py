import copy
import numpy as np
from config import *
from player import Player
from operator import attrgetter

class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"
        self.parent_selection_mode = parent_selection_mode
        self.selection_mode = selection_mode
        self.crossover_method = crossover_method

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
            # for player in prev_players:
            #   new_parents.append(self.clone_player(player))
            new_players = []
            # 1- select parents
            chosen_parents = []
            # 1-1  one state is all of previous players are chosen as parents
            if self.parent_selection_mode == 'all':
                chosen_parents = prev_players
            # 1-2 another state is selecting according to methods that implemented
            else:
                chosen_parents = self.select_players(prev_players, num_players, parent_selection_mode, Q=Q, replace=replace)

            # 2- choose children
            # 2-1 clone player for creating new objects
            new_parents = [self.clone_player(parent) for parent in chosen_parents]
            for i in range(0, num_players, 2):
                # 2-2 choose two parent
                parent1 = new_parents[i]
                parent2 = new_parents[i+1]
                # 2-3 generate children with crossover
                child1, child2 = self.crossover(parent1, parent2, P_c=0.8, crossover_method=self.crossover_method)
                # 2-4 mutation on each child
                self.mutate(child1, 0.1)
                self.mutate(child2, 0.1)
                new_players.append(child1)
                new_players.append(child2)
            return new_players

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player

    def select_players(self, players, num_players, selection_mode, Q = 14, replace = False):
        """

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        :param selection_mode: the method that we use for selection. its type is string
        :param Q: this parameter is only for Q tournament. its type is integer
        :param replace: this parameter is only for Q tournament. its type is boolean
        :return: selected players according to selection_mode that user use
        """
        if selection_mode == "top_k":
            return self.top_k(players, num_players)
        elif selection_mode == "roulette_wheel":
            return self.roulette_wheel(players, num_players)
        elif selection_mode == "SUS":
            return self.SUS(players, num_players)
        elif selection_mode == "Q tournament":
            return self.Q_tournament(players, num_players, Q, replace)
        else:
            raise ValueError("Invalid selection method")

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
        :return: selected players according to RW are returned
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

    def SUS(self, players, num_players):
        """
        We know that for SUS :
        1- find each player probability
        2- create a ruler that we associate an area for each player proportionate to its probability
        3- create another ruler with size of 1-(1/num_players)
        4- create a uniform random number in[0,1/num_players]
        5- shift second ruler as long as uniform random number that produced in step 4
        6- compare ruler2 and ruler1 and select players
        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        :return: selected players according to SUS are returned
        """
        # define list of selected players for output
        selected_players = []
        # step 1
        probabilities = self.fitness_proportionate(players)
        # step 2
        ruler1 = [0]
        for i in range(num_players):
            ruler1.append(probabilities[i]+ruler1[i])
        # step 3
        ruler2 = [i for i in np.arange(0, 1-1/num_players, 1/num_players)]
        # step 4
        uni_rand_num = np.random.uniform(0, 1/num_players)
        # step 5
        shifted_ruler2 = [ i + uni_rand_num for i in ruler2]
        # step 6
        for i in shifted_ruler2:
            for j in range(len(ruler1)-1):
                if  ruler1[j] <= i <= ruler1[j+1]:
                    selected_players.append(players[j])
        return selected_players

    def  Q_tournament(self, players, num_players, Q, replace):
        """
        In this algorithme we choose uniform random Q players from players
        and then choose the player with best fitness among Q players. this
        procedure occurrs num_players times. Q tournament has two form. one
        is replace is true and another replace is false.
        if replace is false the selected player cant be chosen any more.
        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        :param Q: Q value for Q_tournament algorithme
        :param replace: boolean value and if false the selected player cant be chosen any more
        :return: selected players according to Q_tournament are returned
        """
        selected_players = []
        for i in range(num_players):
            random_selected_players = np.random.choice(players, Q, replace=replace)
            best_from_QSelected = max(random_selected_players, key=attrgetter('fitness'))
            selected_players.append(best_from_QSelected)
        return selected_players

    def crossover(self, player1, player2, P_c=0.8, crossover_method="multi-points"):
        # 1- generate uniform random number in [0,1]
        uniform_rand_num = np.random.uniform(0, 1, 1)
        # 2- check with crossover probability
        if uniform_rand_num > P_c:
            return player1, player2
        # 3- choose crossover method according to input parameter
        if crossover_method == "uniform":
            return self.uniform_crossover(player1, player2)
        elif crossover_method =="multi_points":
            return self.multi_points_crossover(player1, player2, n=n)
        else:
            raise ValueError("invalid crossover method")

    def uniform_crossover(self, player1, player2):
        # first we create copy from parents for swapping perceptrons easily
        player1_copy = self.clone_player(player1)
        player2_copy = self.clone_player(player2)
        for i in range(len(player1.nn.weights)):
            # we should save shape and size of weights and biases. shape is necessary for
            # creating matrix to its first form after crossover, with reshape function
            # also we need total size because we flatten weights and biases and then we should know
            # which part of weights must be changed with the help of size
            #  -- weights
            weights_shape = player1.nn.weights[i].shape
            weights_size = player1.nn.weights[i].size
            #  -- biases
            biases_shape = player1.nn.biases[i].shape
            biases_size = player1.nn.biases[i].size

            # in this step first we flatten matrices and then we should produce uniform random number between 0 and 1
            # for each weights[j] then if the uniform_rand_num > 0.5 we change that parents weights[j]
            #  -- weights
            for j in range(weights_size):
                uniform_rand_num = np.random.uniform(0, 1)
                if uniform_rand_num>0.5:
                    player1.nn.weights[i].flatten()[j] = player2_copy.nn.weights[i].flatten()[j]
                    player2.nn.weights[i].flatten()[j] = player1_copy.nn.weights[i].flatten()[j]
            #  -- biases
            for j in range(biases_size):
                uniform_rand_num = np.random.uniform(0, 1)
                if uniform_rand_num > 0.5:
                    player1.nn.biases[i].flatten()[j] = player2_copy.nn.biases[i].flatten()[j]
                    player2.nn.biases[i].flatten()[j] = player1_copy.nn.biases[i].flatten()[j]

            # now we reshape weights and biases matrices to their first shape
            #  -- weights
            player1.nn.weights[i].reshape(weights_shape)
            player2.nn.weights[i].reshape(weights_shape)
            #  -- biases
            player1.nn.biases[i].reshape(biases_shape)
            player2.nn.biases[i].reshape(biases_shape)

        return player1, player2

    def multi_points_crossover(self, player1, player2, n):
        # number of parts
        parts_num = n+1
        # first we create copy from parents for swapping perceptrons easily
        player1_copy = self.clone_player(player1)
        player2_copy = self.clone_player(player2)
        for i in range(len(player1.nn.weights)):
            # we should save shape and size of weights and biases. shape is necessary for
            # creating matrix to its first form after crossover, with reshape function
            # also we need total size because we flatten weights and biases and then we should know
            # which part of weights must be changed with the help of size
            #  -- weights
            weights_shape = player1.nn.weights[i].shape
            weights_size = player1.nn.weights[i].size
            #  -- biases
            biases_shape = player1.nn.biases[i].shape
            biases_size = player1.nn.biases[i].size

            # in this step first we flatten matrices and then we break them in parts_num parts.
            # then the odd part(for example if n=2 : between 1/3 and 2/3) of parents must be changed with each other.
            for j in range(1, parts_num, 2):
                # -- weights
                player1.nn.weights[i].flatten()[j*weights_size // parts_num:(j+1) * weights_size // parts_num] = player2_copy.nn.weights[i].flatten()[
                                                                                     weights_size // parts_num:(j+1) * weights_size // parts_num]
                player2.nn.weights[i].flatten()[weights_size // parts_num:(j+1) * weights_size // parts_num] = player1_copy.nn.weights[i].flatten()[
                                                                        weights_size // parts_num:(j+1) * weights_size // parts_num]
                #  -- biases
                player1.nn.biases[i].flatten()[biases_size // parts_num:(j+1) * biases_size // parts_num] = player2_copy.nn.biases[
                                                                                               i].flatten()[
                                                                                           biases_size // parts_num:(j+1) * biases_size // parts_num]
                player2.nn.biases[i].flatten()[biases_size // parts_num:(j+1) * biases_size // parts_num] = player1_copy.nn.biases[
                                                                                            i].flatten()[
                                                                                        biases_size // parts_num:(j+1) * biases_size // parts_num]
            # now we reshape weights and biases matrices to their first shape
            #  -- weights
            player1.nn.weights[i].reshape(weights_shape)
            player2.nn.weights[i].reshape(weights_shape)
            #  -- biases
            player1.nn.biases[i].reshape(biases_shape)
            player2.nn.biases[i].reshape(biases_shape)

        return player1, player2

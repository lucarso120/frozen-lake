"""
This file contains the implementation of the general genetic algorithm.
It holds the abstarct and general functions to all other implementatios
"""

import numpy as np
import pygame
import random
import logging
from frozen_lake import FrozenLake
import abc

from objects import Gene, AlgorithmStats

class GeneticAlgorithm:
    def __init__(self, frozen_lake: FrozenLake,
        population_size: int, gene_length: int):
        self.population_size: int = population_size
        self.gene_length: int = gene_length
        self.frozen_lake: FrozenLake = frozen_lake
        self.population = []
        self.new_population = []
        self.best_gene = []
        self.last_best_gene = []
        self.buffer = 0
        self.elite_size = 0.2
        self.generation = 0
        self.stats = AlgorithmStats([], 0)

    def avoid_repetitive_gene(self, gene):
        """ 
        This function is used to avoid repetitive genes in the best_gene list.
        After 50 repetitive genes, the last element of the best_gene list is deleted.
        This should prevent the persistence of genes stuck in local minimums.
        """
        if np.array_equal(self.last_best_gene, np.array([])):
            self.last_best_gene = gene
        else:
            if np.array_equal(gene, self.last_best_gene):
                self.buffer += 1
            else:
                self.last_best_gene = gene
                self.buffer = 0
            if self.buffer == 50:
                self.buffer = 0
                # delete the last element of the best_gene
                self.last_best_gene = np.array([])
                self.best_gene = self.best_gene[:-1]
                logging.info("deleted the last element of the best_gene due to repetitive genes policy")

    @abc.abstractmethod
    def calculate_fitness(self, gene, gene_length_penalty: int = 0.1, opposite_actions_penalty: int = 0.8):
        """
        This function calculates the fitness of a gene.
        Our fitness function is the total reward divided by the distance to the goal.
        We also penalize the gene length and opposite actions.
        """

        if not self.frozen_lake.game_over:
            distance_to_goal = abs(self.frozen_lake.player_pos[0] - self.frozen_lake.goal_pos[0]) + abs(self.frozen_lake.player_pos[1] - self.frozen_lake.goal_pos[1])
            self.frozen_lake.fitness = self.frozen_lake.total_reward / (distance_to_goal + 1) 
            opposite_actions = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}
            for i in range(len(gene)-1):
                if gene[i+1] == opposite_actions[gene[i]]:
                    self.frozen_lake.fitness -= opposite_actions_penalty

    def calculate_gene_fitness(self, gene: list[str]) -> int:
        """ 
        This methods calls the calculate_fitness method and returns the fitness of the gene.
        We use this function due to the issue of having to process the player moves
        """
        for movement in gene:
            self.frozen_lake.take_action(movement)
            if self.frozen_lake.game_over:
                return 0
        self.calculate_fitness(gene)
        return self.frozen_lake.fitness
        
    def initialize_population(self):
        """
        Initialize the population with random genes.
        Makes it possible to adapt the probability of each action.
        """
        down_right_prob = [0.25, 0.25, 0.25, 0.25]  # Probabilities for [down, right, up, left]
        population = []
        for i in range(self.population_size):
            gene = np.random.choice(self.frozen_lake.action_space, size=self.gene_length, p=down_right_prob)
            population.append(gene)
        return population

    @abc.abstractmethod
    def solve(self):
        """
        Solve the problem using the genetic algorithm.
        """
        pass
    
    @abc.abstractmethod
    def evaluate_gene(self, gene):
        """
        Evaluate the gene by playing the game with it, and calculating the fitness.
        This is our implementation of elitism, where we keep the best gene from the population.
        """
        pass

    def get_step_gene(self, best_gene):
        """
        This is a helper function to handle the duiality of dealing with
        np arrays and lsists
        """
        try:
            return best_gene.copy().tolist()
        except AttributeError:
            return best_gene.copy()

    def mutate(self, gene):
        """
        Mutate the gene by changing one of the existing actions
        This should be called for the best gene, in order to create mutations on
        about 20% of the population
        """
        if random.random() < 0.1:
            try:
                gene[random.randint(0, self.gene_length - 1)] = random.choice(self.frozen_lake.action_space)
            except IndexError:
                pass
        return gene

    def crossover(self, parent1, parent2):
        """
        Perform crossover between two parents to create a child gene.
        """
        try:
            crossover_point = np.random.randint(1, self.gene_length - 1)
        except ValueError:
            crossover_point = 1
        child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        return child

    @abc.abstractmethod
    def generate_new_population(self, step_gene):
        """
        Generate a new population based on the best gene.
        We ad a random factor to the gene length, in order to create diversity
        """
        pass

    def get_algorithm_stats(self):
        """
        Return the algorithm stats
        """
        self.stats = AlgorithmStats(self.best_gene, self.generation)
        

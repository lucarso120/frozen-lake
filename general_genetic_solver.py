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
        self.new_population = []
        self.best_gene = []
        self.last_best_gene = []
        self.buffer = 0
        self.elite_size = 0.2
        self.stats = AlgorithmStats([], 0)

    def avoid_repetitive_gene(self, gene):
        if np.array_equal(self.last_best_gene, np.array([])):
            self.last_best_gene = gene
        else:
            if np.array_equal(gene, self.last_best_gene):
                self.buffer += 1
            if self.buffer == 50:
                self.buffer = 0
                # delete the last element of the best_gene
                self.last_best_gene = np.array([])
                self.best_gene = self.best_gene[:-1]
                print("deleted the last element of the best_gene due to repetitive genes policy")

    def calculate_fitness(self, gene, gene_length_penalty: int = 0.5, opposite_actions_penalty: int = 0.6):
        if not self.frozen_lake.game_over:
            distance_to_goal = abs(self.frozen_lake.player_pos[0] - self.frozen_lake.goal_pos[0]) + abs(self.frozen_lake.player_pos[1] - self.frozen_lake.goal_pos[1])
            self.frozen_lake.fitness = 1 / (distance_to_goal + gene_length_penalty * len(gene))
            opposite_actions = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}
            for i in range(len(gene)-1):
                if gene[i+1] == opposite_actions[gene[i]]:
                    self.frozen_lake.fitness -= opposite_actions_penalty
            self.frozen_lake.fitness = round(self.frozen_lake.fitness, 2) + self.frozen_lake.total_reward


    def calculate_gene_fitness(self, gene: list[str]) -> int:
        for movement in gene:
            self.frozen_lake.take_action(movement)
            if self.frozen_lake.game_over:
                return 0
        self.calculate_fitness(gene)
        return self.frozen_lake.fitness
        
    def initialize_population(self):
        population = []
        for i in range(self.population_size):
            gene = np.random.choice(self.frozen_lake.action_space, size=self.gene_length)
            population.append(gene)
        return population

    @abc.abstractmethod
    def solve(self):
        pass
    
    @abc.abstractmethod
    def evaluate_gene(self, gene):
        """
        Evaluate the gene by playing the game with it, and calculating the fitness.
        This is our implementation of elitism, where we keep the best gene from the population.
        """
        pass

    def get_step_gene(self, best_gene):
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
        crossover_point = np.random.randint(1, self.gene_length - 1)
        child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        return child

    @abc.abstractmethod
    def generate_new_population(self, step_gene):
        """
        Generate a new population based on the best gene.
        We ad a random factor to the gene length, in order to create diversity
        """
        pass

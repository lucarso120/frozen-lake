"""
This module initializes the GA version in which we use FPS selection method.
"""
import numpy as np
import pygame
import random
from frozen_lake import FrozenLake
from general_genetic_algorithm import GeneticAlgorithm
from objects import Gene, AlgorithmStats
import sys

class GeneticAlgorithmSolverFPS(GeneticAlgorithm):
    """
    In this implementation, we use FPS selection method to select the parents.
    """
    def __init__(self, frozen_lake, population_size, gene_length, mutation_method):
        super().__init__(frozen_lake, population_size, gene_length, mutation_method)
        self.mutation_method = mutation_method

    def calculate_fitness(self, gene, gene_length_penalty: int = 0.5, opposite_actions_penalty: int = 0.6):
        self.frozen_lake.fitness = self.frozen_lake.total_reward
        opposite_actions = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}
        for i in range(len(gene)-1):
            if gene[i+1] == opposite_actions[gene[i]]:
                self.frozen_lake.fitness -= opposite_actions_penalty

    def fps_selection(self, fitness_list):
        # in fitness_list, if fitness is negative, we make it zero
        fitness_list = [fitness if fitness > 0 else 0 for fitness in fitness_list]
        total_fitness = sum(fitness_list)
        if total_fitness == 0:
            probabilities = [1 / len(fitness_list) for fitness in fitness_list]
        else:
            probabilities = [fitness / total_fitness for fitness in fitness_list]
        indices = np.random.choice(range(len(self.population)), size=round(self.population_size/2), p=probabilities)
        return indices

    def generate_new_population(self):
        """
        Generate a new population based on the best gene.
        We add a random factor to the gene length, in order to create diversity
        """
        down_right_prob = [0.4, 0.4, 0.1, 0.1]  # Probabilities for [down, right, up, left]
        fitness_list = [self.calculate_gene_fitness(gene) for gene in self.population]
        selected_indices = self.fps_selection(fitness_list)

        new_population = []
        for _ in range(self.population_size):
            parent1_index, parent2_index = np.random.choice(selected_indices, size=2, replace=False)
            parent1, parent2 = self.population[parent1_index], self.population[parent2_index]
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child.tolist())
        self.population = new_population
    

    def solve_illustrate(self):
        self.population = self.initialize_population()
        while not self.frozen_lake.won:
            self.generation += 1
            for gene in self.population:
                print(Gene(self.frozen_lake.fitness, gene))
                for movement in gene:
                    self.frozen_lake.render()
                    pygame.display.update()
                    self.frozen_lake.take_action(movement)
                    pygame.time.wait(10)
                    if self.frozen_lake.won:
                        breakpoint()
                        print("Stats")
                        self.best_gene = gene
                        self.get_algorithm_stats()
                        print(self.stats)
                        pygame.quit()
                        sys.exit()
                self.frozen_lake.restart()
            self.generate_new_population()

    def solve(self):
        self.population = self.initialize_population()
        while not self.frozen_lake.won:
            self.generation += 1
            if self.generation > 100:
                self.get_algorithm_stats()
                return
            for gene in self.population:
                for movement in gene:
                    self.frozen_lake.take_action(movement)
                    if self.frozen_lake.won:
                        self.best_gene = gene
                        self.get_algorithm_stats()
                        return
                self.frozen_lake.restart()
            self.generate_new_population()

#fl = FrozenLake(slippery=False) 
#solver = GeneticAlgorithmSolverFPS(fl, population_size=10, gene_length=10) 
#solver.solve_illustrate()
"""
This module initializes the GA version in which we use FPS selection method.
"""
import numpy as np
import pygame
import random
from frozen_lake import FrozenLake
from general_genetic_solver import GeneticAlgorithm
from objects import Gene, AlgorithmStats


class GeneticAlgorithmSolverFPS(GeneticAlgorithm):
    """
    In this implementation, we use FPS selection method to select the parents.
    """

    def fps_selection(self, fitness_list):
        total_fitness = sum(fitness_list)
        if total_fitness == 0:
            probabilities = [1 / len(fitness_list) for fitness in fitness_list]
        else:
            probabilities = [fitness / total_fitness for fitness in fitness_list]
        
        indices = np.random.choice(range(len(self.population)), size=round(self.population_size/2), p=probabilities)
        return indices


    def generate_new_population(self, step_gene):
            
        fitness_list = [self.calculate_gene_fitness(gene) for gene in self.population]
        selected_indices = self.fps_selection(fitness_list)

        new_population = []
        for i in range(self.population_size):
            parent1_index, parent2_index = np.random.choice(selected_indices, size=2, replace=False)
            parent1, parent2 = self.population[parent1_index], self.population[parent2_index]
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)

        self.population = new_population


    def solve(self):
        self.population = self.initialize_population()
        while not self.frozen_lake.won:
            for gene in self.population:
                self.calculate_gene_fitness(gene)
                self.generate_new_population(gene)
                print(Gene(self.frozen_lake.fitness, gene))
                for movement in gene:
                    self.frozen_lake.render()
                    self.frozen_lake.take_action(movement)
                    pygame.display.update()
                    pygame.time.wait(100)
                self.generate_new_population(gene)

fl = FrozenLake(slippery=False) 
solver = GeneticAlgorithmSolverFPS(fl, population_size=5, gene_length=10) 
solver.solve()
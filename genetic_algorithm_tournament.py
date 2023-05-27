
import numpy as np
import pygame
import random
from frozen_lake import FrozenLake
from general_genetic_algorithm import GeneticAlgorithm
from objects import Gene, AlgorithmStats

class GeneticAlgorithmSolverTournament(GeneticAlgorithm):
    """
    In this implementation, we use Tournament selection method to select the parents.
    """

    def tournament_selection(self, fitness_list):
        selected_indices = []
        for i in range(self.population_size):
            tournament_indices = np.random.choice(range(len(self.population)), size=2, replace=False)
            tournament_fitness = [fitness_list[i] for i in tournament_indices]
            selected_indices.append(tournament_indices[np.argmax(tournament_fitness)])
        return selected_indices

    def generate_new_population(self, step_gene):
        fitness_list = [self.calculate_gene_fitness(gene) for gene in self.population]
        elite_size = int(self.elite_size * self.population_size)
        elite_indices = np.argsort(fitness_list)[::-1][:elite_size]
        new_population = [self.population[i] for i in elite_indices]

        selected_indices = self.tournament_selection(fitness_list)

        for i in range(self.population_size - elite_size):
            parent1_index, parent2_index = np.random.choice(selected_indices, size=2, replace=True)
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

    def evaluate_gene(self, gene):
        self.frozen_lake.reset()
        for movement in gene:
            self.frozen_lake.take_action(movement)


fl = FrozenLake(slippery=False) 
solver = GeneticAlgorithmSolverTournament(fl, population_size=10, gene_length=10) 
solver.solve()
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

    def __init__(self, frozen_lake, population_size, gene_length):
        super().__init__(frozen_lake, population_size, gene_length)
        self.frozen_lake.rewards = {'goal': 100, 'hole': -10, 'move': 1, "out-of-bounds": -0.2}

    def calculate_fitness(self, gene, gene_length_penalty: int = 0.5, opposite_actions_penalty: int = 0.6):
        self.frozen_lake.fitness = self.frozen_lake.total_reward
        opposite_actions = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}
        for i in range(len(gene)-1):
            if gene[i+1] == opposite_actions[gene[i]]:
                self.frozen_lake.fitness -= opposite_actions_penalty

    def tournament_selection(self, fitness_list):
        selected_indices = []
        for i in range(self.population_size):
            tournament_indices = np.random.choice(range(len(self.population)), size=2, replace=False)
            tournament_fitness = [fitness_list[i] for i in tournament_indices]
            selected_indices.append(tournament_indices[np.argmax(tournament_fitness)])
        return selected_indices

    def generate_new_population(self):
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
                print(Gene(self.frozen_lake.fitness, gene))
                self.frozen_lake.play_auto_agent(gene)
                for movement in gene:
                    if self.frozen_lake.game_over:
                        continue
                    if self.frozen_lake.won:
                        break
                        print("Won")
                self.frozen_lake.restart()
            self.generate_new_population()

fl = FrozenLake(slippery=False) 
solver = GeneticAlgorithmSolverTournament(fl, population_size=10, gene_length=10) 
solver.solve()
import numpy as np
import pygame
import random
import sys
from frozen_lake import FrozenLake
from general_genetic_algorithm import GeneticAlgorithm
from objects import Gene, AlgorithmStats


class GeneticAlgorithmSolverTournament(GeneticAlgorithm):
    """
    In this implementation, we use Tournament selection method to select the parents.
    """

    def __init__(self, frozen_lake, population_size, gene_length):
        super().__init__(frozen_lake, population_size, gene_length)
        self.frozen_lake.rewards = {'goal': 100, 'hole': -5, 'move': 1, "out-of-bounds": -1}

    def calculate_fitness(self, gene, gene_length_penalty: int = 0.5, opposite_actions_penalty: int = 0.6):
        self.frozen_lake.fitness = self.frozen_lake.total_reward
        opposite_actions = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}
        for i in range(len(gene)-1):
            if gene[i+1] == opposite_actions[gene[i]]:
                self.frozen_lake.fitness -= opposite_actions_penalty

    def mutate(self, gene):
        """
        Mutate the gene by changing one of the existing actions
        This should be called for the best gene, in order to create mutations on
        about 20% of the population
        """
        if random.random() < 0.5:
            try:
                gene[random.randint(0, self.gene_length - 1)] = random.choice(self.frozen_lake.action_space)
            except IndexError:
                pass
        return gene

    def calculate_gene_fitness(self, gene: list[str]) -> int:
        for movement in gene:
            self.frozen_lake.take_action(movement)
        self.calculate_fitness(gene)
        return self.frozen_lake.fitness

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

    def solve_illustrate(self):
        self.population = self.initialize_population()
        while not self.frozen_lake.won:
            self.generation += 1
            for gene in self.population:
                print(Gene(self.frozen_lake.fitness, gene))
                for movement in gene:
                    self.frozen_lake.render()
                    pygame.display.update()
                    reward = self.frozen_lake.take_action(movement)
                    pygame.time.wait(10)
                    if self.frozen_lake.won:
                        print("Won")
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
            for gene in self.population:
                for movement in gene:
                    reward = self.frozen_lake.take_action(movement)
                    if self.frozen_lake.won:
                        self.best_gene = gene
                        self.get_algorithm_stats()
                        return
                self.frozen_lake.restart()
            self.generate_new_population()

#fl = FrozenLake(slippery=False) 
#solver = GeneticAlgorithmSolverTournament(fl, population_size=10, gene_length=10) 
#solver.solve_illustrate()
import numpy as np
import pygame
import random
from frozen_lake import FrozenLake

class GeneticAlgorithmSolver:
    def __init__(self, frozen_lake: FrozenLake,
        population_size: int, gene_length: int):
        self.population_size: int = population_size
        self.gene_length: int = gene_length
        self.frozen_lake: FrozenLake = frozen_lake
        self.new_population = []
        self.best_gene = []

    def initialize_population(self):
        population = []
        for i in range(self.population_size):
            gene = np.random.choice(self.frozen_lake.action_space, size=self.gene_length)
            population.append(gene)
        return population

    def solve(self):
        self.frozen_lake.population = self.initialize_population()
        while not self.frozen_lake.won:
            for gene in self.frozen_lake.population:
                self.evaluate_gene(gene)
            
            step_gene = self.get_step_gene(self.best_gene)
            self.generate_new_population(step_gene)

            self.frozen_lake.population = self.new_population
            self.frozen_lake.play_auto_agent(self.best_gene)

    def evaluate_gene(self, gene):
        self.frozen_lake.restart()
        print(f"gene sequence: {gene}")
        for movement in gene:
            self.frozen_lake.render()
            self.frozen_lake.take_action(movement)
            self.frozen_lake.calculate_fitness()
            pygame.display.update()
            pygame.time.wait(100)

            if self.frozen_lake.game_over:
                print("game over for this gene")
                self.frozen_lake.restart()
                continue
        if self.frozen_lake.fitness > self.frozen_lake.best_fitness:
            self.frozen_lake.best_fitness = self.frozen_lake.fitness
            self.best_gene = gene
        print(f"best gene is {self.best_gene}")

    def get_step_gene(self, best_gene):
        try:
            return best_gene.copy().tolist()
        except AttributeError:
            return best_gene.copy()

    def generate_new_population(self, step_gene):
        for _ in range(self.population_size):
            new_gene = step_gene.copy()
            for _ in range(self.gene_length):
                new_gene.append(random.choice(self.frozen_lake.action_space))
            self.new_population.append(new_gene)

fl = FrozenLake() 
solver = GeneticAlgorithmSolver(fl, population_size=5, gene_length=2) 
solver.solve()
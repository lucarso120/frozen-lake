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
    
    def initialize_population(self):
        population = []
        for i in range(self.population_size):
            gene = np.random.choice(self.frozen_lake.action_space, size=self.gene_length)
            population.append(gene)
        return population

    def solve(self):
        self.frozen_lake.population = self.initialize_population()
        best_fitness = 0
        best_gene = []

        while not self.frozen_lake.won:
            new_population = []
            for gene in self.frozen_lake.population:
                self.evaluate_gene(gene, best_gene, best_fitness)
            
            step_gene = self.get_step_gene(best_gene)
            self.generate_new_population(step_gene, new_population)

            self.frozen_lake.population = new_population
            self.frozen_lake.play_auto_agent(best_gene)

    def evaluate_gene(self, gene, best_gene, best_fitness):
        self.frozen_lake.restart()
        print(f"gene sequence: {gene}")
        for movement in gene:
            self.frozen_lake.render()
            self.frozen_lake.take_action(movement)
            pygame.display.update()
            pygame.time.wait(100)

            if self.frozen_lake.game_over:
                print("game over for this gene")
                self.frozen_lake.restart()
                continue

        if self.frozen_lake.fitness >= best_fitness:
            best_fitness = self.frozen_lake.fitness
            best_gene.extend(gene)
        print(f"best gene is {best_gene}")

    def get_step_gene(self, best_gene):
        try:
            return best_gene.copy().tolist()
        except AttributeError:
            return best_gene.copy()

    def generate_new_population(self, step_gene, new_population):
        for _ in range(self.population_size):
            new_gene = step_gene.copy()
            for _ in range(self.gene_length):
                new_gene.append(random.choice(self.frozen_lake.action_space))
            new_population.append(new_gene)


fl = FrozenLake()
solver = GeneticAlgorithmSolver(fl, population_size=5, gene_length=2)
solver.solve()   
    

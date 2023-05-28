import numpy as np
import pygame
import random
import sys
from frozen_lake import FrozenLake
from general_genetic_algorithm import GeneticAlgorithm
from objects import Gene, AlgorithmStats


class GeneticAlgorithmSolver(GeneticAlgorithm):
    """
    For this implementation, we base our approach on elitism, where we keep the best gene from the population.
    However, instead of using a full lenght gene, we increase its size at each generation.
    This approach, which we can refer to as complexity increase, allows us to find the best gene faster.
    Additionally, we add a random factor to the gene length, in order to create diversity.

    """
    def __init__(self, frozen_lake, population_size, gene_length, mutation_method):
        super().__init__(frozen_lake, population_size, gene_length, mutation_method)
        self.mutation_method = mutation_method

    def solve_illustrate(self):
        self.population = self.initialize_population()
        while not self.frozen_lake.won:
            self.generation += 1
            for gene in self.population:
                print(Gene(self.frozen_lake.fitness, gene))
                self.evaluate_gene_illustrate(gene)
                self.frozen_lake.restart()
            step_gene = self.get_step_gene(self.best_gene)
            self.generate_new_population(step_gene)

    def solve(self):
        self.population = self.initialize_population()
        while not self.frozen_lake.won:
            self.generation += 1
            if self.generation > 100:
                self.get_algorithm_stats()
                return
            for gene in self.population:
                self.evaluate_gene(gene)
                if not self.frozen_lake.won:
                    self.frozen_lake.restart()
                else:
                    self.best_gene = gene
                    self.get_algorithm_stats()
                    return
            step_gene = self.get_step_gene(self.best_gene)
            self.generate_new_population(step_gene)


    def generate_new_population(self, step_gene):
        """
        Generate a new population based on the best gene.
        We add a random factor to the gene length, in order to create diversity
        """
        self.new_population = []
        down_right_prob = [0.4, 0.4, 0.1, 0.1]  # Probabilities for [down, right, up, left]
        for _ in range(self.population_size):
            new_gene = self.get_step_gene(self.mutate(step_gene.copy()))
            for _ in range(self.gene_length):
                if len(new_gene) < self.gene_length:
                    new_move = np.random.choice(self.frozen_lake.action_space, p=down_right_prob)
                    new_gene.append(new_move)
            if random.random() < 0.5:
                new_gene.append(random.choice(self.frozen_lake.action_space))
            if random.random() < 0.2:
                new_gene.append(random.choice(self.frozen_lake.action_space))
            self.new_population.append(new_gene)
        self.population = self.new_population
            
    def evaluate_gene_illustrate(self, gene):
        """
        Evaluate the gene by playing the game with it, and calculating the fitness.
        This is our implementation of elitism, where we keep the best gene from the population.
        """
        print(f"gene sequence: {gene}")

        for movement in gene:
            self.frozen_lake.render()
            if not self.frozen_lake.game_over:
                self.frozen_lake.take_action(movement)
                pygame.display.update()
                pygame.time.wait(100)
            if self.frozen_lake.won:
                self.best_gene = gene
                self.get_algorithm_stats()
                print(self.stats)
                pygame.quit()
                sys.exit()
        self.calculate_fitness(gene)
        print(f"Evaluated Gene: {gene}, with fitness: {str(self.frozen_lake.fitness)}. The current best gene is: {self.best_gene} with fitness: {str(self.frozen_lake.best_fitness)}")  
    
        if self.frozen_lake.fitness >= self.frozen_lake.best_fitness:
            self.frozen_lake.best_fitness = self.frozen_lake.fitness
            self.best_gene = gene
            self.avoid_repetitive_gene(self.best_gene)
            print(f"New best gene updated to: {self.best_gene} with fitness: {self.frozen_lake.best_fitness}")
        else:
            self.avoid_repetitive_gene(self.best_gene)
        
    def evaluate_gene(self, gene):
        """
        Evaluate the gene by playing the game with it, and calculating the fitness.
        This is our implementation of elitism, where we keep the best gene from the population.
        """
        for movement in gene:
            self.frozen_lake.take_action(movement)
            if self.frozen_lake.won:
                self.best_gene = gene
                self.get_algorithm_stats()
                return
        self.calculate_fitness(gene)
        if self.frozen_lake.fitness >= self.frozen_lake.best_fitness:
            self.frozen_lake.best_fitness = self.frozen_lake.fitness
            self.best_gene = gene
            self.avoid_repetitive_gene(self.best_gene)
        else:
            self.avoid_repetitive_gene(self.best_gene)


#fl = FrozenLake(slippery=False) 
#solver = GeneticAlgorithmSolver(fl, population_size=10, gene_length=4) 
#solver.solve_illustrate()
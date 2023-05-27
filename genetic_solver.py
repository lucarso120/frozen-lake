import numpy as np
import pygame
import random
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

    def solve(self):
        self.frozen_lake.population = self.initialize_population()
        while not self.frozen_lake.won:
            self.stats.generation += 1
            for gene in self.frozen_lake.population:
                self.evaluate_gene(gene)
                self.stats.total_number_of_genes += 1
            
            step_gene = self.get_step_gene(self.best_gene)
            self.generate_new_population(step_gene)

            self.frozen_lake.population = self.new_population
            self.frozen_lake.play_auto_agent(self.best_gene)


    def generate_new_population(self, step_gene):
        """
        Generate a new population based on the best gene.
        We add a random factor to the gene length, in order to create diversity
        """
        down_right_prob = [0.4, 0.4, 0.1, 0.1]  # Probabilities for [down, right, up, left]
        for _ in range(self.population_size):
            new_gene = self.mutate(step_gene.copy())
            for _ in range(self.gene_length - 1):
                if len(new_gene) < self.gene_length:
                    new_move = np.random.choice(self.frozen_lake.action_space, p=down_right_prob)
                    new_gene.append(new_move)
            if random.random() < 0.5:
                new_gene.append(random.choice(self.frozen_lake.action_space))
            if random.random() < 0.2:
                new_gene.append(random.choice(self.frozen_lake.action_space))
            self.new_population.append(new_gene)
            
    def evaluate_gene(self, gene):
        """
        Evaluate the gene by playing the game with it, and calculating the fitness.
        This is our implementation of elitism, where we keep the best gene from the population.
        """
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
                return
            if self.frozen_lake.won:
                self.best_gene = gene
                self.stats.best_gene = gene
                self.stats.best_fitness = self.frozen_lake.fitness
                print(self.stats.__str__)
                continue
        self.calculate_fitness(gene)
        print(f"Evaluated Gene: {gene}, with fitness: {str(self.frozen_lake.fitness)}. The current best gene is: {self.best_gene} with fitness: {str(self.frozen_lake.best_fitness)}")  
    
        if self.frozen_lake.fitness > self.frozen_lake.best_fitness:
            self.frozen_lake.best_fitness = self.frozen_lake.fitness
            self.best_gene = gene
            print(f"New best gene updated to: {self.best_gene} with fitness: {self.frozen_lake.best_fitness}")
        else:
            self.avoid_repetitive_gene(self.best_gene)


fl = FrozenLake(slippery=False) 
solver = GeneticAlgorithmSolver(fl, population_size=5, gene_length=3) 
solver.solve()
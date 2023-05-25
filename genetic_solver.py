import numpy as np
import pygame
import random
import logging
from frozen_lake import FrozenLake

class GeneticAlgorithmSolver:
    def __init__(self, frozen_lake: FrozenLake,
        population_size: int, gene_length: int):
        self.population_size: int = population_size
        self.gene_length: int = gene_length
        self.frozen_lake: FrozenLake = frozen_lake
        self.new_population = []
        self.best_gene = []
        self.last_best_gene = []
        self.buffer = 0

    def avoid_repetitive_gene(self, gene):
        if np.array_equal(self.last_best_gene, np.array([])):
            self.last_best_gene = gene
        else:
            if np.array_equal(gene, self.last_best_gene):
                self.buffer += 1
            if self.buffer == 10:
                self.buffer = 0
                # delete the last element of the best_gene
                self.last_best_gene = np.array([])
                self.best_gene = self.best_gene[:-1]

    def calculate_fitness(self, gene, gene_length_penalty: int = 0.5, opposite_actions_penalty: int = 1):
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
            self.take_action(movement)
            if self.game_over:
                return 0
        fitness = self.calculate_fitness(gene)
        return fitness
        
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
            pygame.display.update()
            pygame.time.wait(100)

            if self.frozen_lake.game_over:
                print("game over for this gene")
                self.frozen_lake.restart()
                continue
            if self.frozen_lake.won:
                self.best_gene = gene
        fitness = self.calculate_fitness(gene)
        print(f"Evaluated Gene: {gene}, with fitness: {str(fitness)}. The current best gene is: {self.best_gene} with fitness: {str(self.frozen_lake.best_fitness)}")  
    
        if self.frozen_lake.fitness > self.frozen_lake.best_fitness:
            self.frozen_lake.best_fitness = self.frozen_lake.fitness
            self.best_gene = gene
            self.avoid_repetitive_gene(self.best_gene)
            print(f"New best gene updated to: {self.best_gene} with fitness: {self.frozen_lake.best_fitness}")

    def get_step_gene(self, best_gene):
        try:
            return best_gene.copy().tolist()
        except AttributeError:
            return best_gene.copy()

    def generate_new_population(self, step_gene):
        for _ in range(self.population_size):
            if random.random() < 0.2 :
                # change one of the action spaces in the step_gene
                try:
                    step_gene[random.randint(0, self.gene_length - 1)] = random.choice(self.frozen_lake.action_space)
                except IndexError:
                    continue
            new_gene = step_gene.copy()
            for _ in range(self.gene_length - 1):
                new_gene.append(random.choice(self.frozen_lake.action_space))
            if random.random() < 0.3: # will add an extra gene 0.3 of the time
                new_gene.append(random.choice(self.frozen_lake.action_space))
            if random.random() < 0.2: # will add an extra gene 0.3 x 0.2 of the time
                new_gene.append(random.choice(self.frozen_lake.action_space))
            self.new_population.append(new_gene)

fl = FrozenLake() 
solver = GeneticAlgorithmSolver(fl, population_size=5, gene_length=2) 
solver.solve()
import numpy as np
class GeneticAlgorithm:
    
    def __init__(self, population_size, gene_length, action_space):
        self.population_size = population_size
        self.gene_length = gene_length
        self.action_space = action_space
        self.population = self.initialize_population()
    
    def initialize_population(self):
        population = []
        for i in range(self.population_size):
            gene = np.random.choice(self.action_space, size=self.gene_length)
            population.append(gene)
        return population


    
    

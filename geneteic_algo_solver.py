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
    
    def select_parents(self, fitness_scores):
        parent1 = self.population[np.random.choice(range(self.population_size), p=fitness_scores)]
        parent2 = self.population[np.random.choice(range(self.population_size), p=fitness_scores)]
        return parent1, parent2
    
    def generate_offspring(self, parent1, parent2):
        crossover_point = np.random.randint(1, self.gene_length-1)
        offspring1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
        offspring2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
        return offspring1, offspring2
    
    def evolve_population(self, fitness_function, mutation_rate=0.1):
        fitness_scores = np.array([fitness_function(individual) for individual in self.population])
        fitness_scores = fitness_scores / np.sum(fitness_scores)
        
        new_population = []
        for i in range(self.population_size):
            parent1, parent2 = self.select_parents(fitness_scores)
            offspring1, offspring2 = self.generate_offspring(parent1, parent2)
            new_population.append(offspring1)
            new_population.append(offspring2)
        
        for i in range(self.population_size):
            if np.random.rand() < mutation_rate:
                gene_index = np.random.randint(self.gene_length)
                new_population[i][gene_index] = np.random.choice(self.action_space)
        
        self.population = new_population
        return np.max(fitness_scores)

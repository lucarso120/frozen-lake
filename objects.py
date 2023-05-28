class AlgorithmStats:
    def __init__(self, best_gene: list, generation: int):
        self.best_gene = best_gene
        self.generation = generation

    def __str__(self):
        return f"best gene: {self.best_gene}, generation: {self.generation}"


class Gene:
    def __init__(self, gene_fitness: int, gene: list):
        self.gene_fitness: int = gene_fitness
        self.gene: list = gene
    
    def __str__(self):
        return f"gene: {self.gene}, fitness: {self.gene_fitness}"



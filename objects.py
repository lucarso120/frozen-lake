class AlgorithmStats:
    def __init__(self, best_gene: list, best_fitness: int):
        self.best_gene = best_gene
        self.best_fitness = best_fitness
        self.total_number_of_genes = 0
        self.generation = 0

    def __str__(self):
        return f"best gene: {self.best_gene}, best fitness: {self.best_fitness}, generation: {self.generation}"


class Gene:
    def __init__(self, gene_fitness: int, gene: list):
        self.gene_fitness: int = gene_fitness
        self.gene: list = gene
    
    def __str__(self):
        return f"gene: {self.gene}, fitness: {self.gene_fitness}"



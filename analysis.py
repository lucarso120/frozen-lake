"""
In this module we run all the GAs to measure its performance.
The implementation here doe snot apply the slippery mode.
"""

from frozen_lake_raw import FrozenLakeRaw
from genetic_solver import GeneticAlgorithmSolver
from objects import AlgorithmStats
from genetic_algorithm_fps import GeneticAlgorithmSolverFPS
from genetic_algorithm_tournament import GeneticAlgorithmSolverTournament
from tqdm import tqdm

def main(num_runs):
    solver_generations = []
    fps_generations = []
    tournament_generations = []

    for i in tqdm(range(num_runs)):
        # create a new game for every trial
        frozen_lake_game = FrozenLakeRaw()
        genetic_algorithm_solver = GeneticAlgorithmSolver(frozen_lake_game, population_size=10, gene_length=3, mutation_method=None)
        genetic_algorithm_fps = GeneticAlgorithmSolverFPS(frozen_lake_game, population_size=10, gene_length=8, mutation_method=None)
        genetic_algorithm_tournament = GeneticAlgorithmSolverTournament(frozen_lake_game, population_size=10, gene_length=8, mutation_method=None)

        genetic_algorithm_solver.solve()
        solver_generations.append(genetic_algorithm_solver.stats.generation)

        genetic_algorithm_fps.solve()
        fps_generations.append(genetic_algorithm_fps.stats.generation)

        genetic_algorithm_tournament.solve()
        tournament_generations.append(genetic_algorithm_tournament.stats.generation)

    avg_solver_generations = sum(solver_generations) / num_runs
    avg_fps_generations = sum(fps_generations) / num_runs
    avg_tournament_generations = sum(tournament_generations) / num_runs

    print(f"Average generations for GeneticAlgorithmSolver: {avg_solver_generations}")
    print(f"Average generations for GeneticAlgorithmSolverFPS: {avg_fps_generations}")
    print(f"Average generations for GeneticAlgorithmSolverTournament: {avg_tournament_generations}")

main(1000)
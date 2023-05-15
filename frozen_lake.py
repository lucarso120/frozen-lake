import numpy as np
import random
import pygame
import sys 

from geneteic_algo_solver import GeneticAlgorithm

class FrozenLake:
    
    def __init__(self, size=4, population=[]):
        self.size = size
        self.population = population
        self.board = np.zeros((size, size))
        self.player_pos = (0, 0)
        self.goal_pos = (size-1, size-1)
        self.hole_positions = [(1,1), (3,3), (2,0)]
        self.action_space = ['u', 'd', 'l', 'r']
        self.rewards = {'goal': 10, 'hole': -10, 'move': -1}
        self.game_over = False
        self.won = False
        self.fitness = 0
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.font = pygame.font.SysFont('Arial', 20)
        self.colors = {'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)}

    def render(self):
        block_size = 100
        for i in range(self.size):
            for j in range(self.size):
                rect = pygame.Rect(j * block_size, i * block_size, block_size, block_size)
                if self.player_pos == (i, j):
                    pygame.draw.rect(self.screen, self.colors['green'], rect)
                    label = self.font.render('P', True, self.colors['white'])
                    self.screen.blit(label, (j * block_size + 40, i * block_size + 40))

                elif self.goal_pos == (i, j):
                    pygame.draw.rect(self.screen, self.colors['blue'], rect)
                    label = self.font.render('G', True, self.colors['white'])
                    self.screen.blit(label, (j * block_size + 40, i * block_size + 40))
                elif (i, j) in self.hole_positions:
                    pygame.draw.rect(self.screen, self.colors['red'], rect)
                    label = self.font.render('H', True, self.colors['white'])
                    self.screen.blit(label, (j * block_size + 40, i * block_size + 40))
                else:
                    pygame.draw.rect(self.screen, self.colors['white'], rect)
        pygame.display.flip()

    def evaluate_fitness(self):
        return self.player_pos[0] + self.player_pos[1]

    def take_action(self, action):
        if self.game_over:
            self.player_pos = (0,0)
        if action == 'u':
            new_pos = (self.player_pos[0]-1, self.player_pos[1])
        elif action == 'd':
            new_pos = (self.player_pos[0]+1, self.player_pos[1])
        elif action == 'l':
            new_pos = (self.player_pos[0], self.player_pos[1]-1)
        elif action == 'r':
            new_pos = (self.player_pos[0], self.player_pos[1]+1)

        if new_pos[0] < 0 or new_pos[0] >= self.size or new_pos[1] < 0 or new_pos[1] >= self.size:
            reward = self.rewards['move']
            self.fitness = self.evaluate_fitness()
        elif new_pos == self.goal_pos:
            reward = self.rewards['goal']
            self.game_over = True
            self.won = True
            print('you won')
        elif new_pos in self.hole_positions:
            reward = self.rewards['hole']
            self.game_over = True
            print('Game Over')
        else:
            reward = self.rewards['move']
            self.player_pos = new_pos

        return reward

    def play_auto_agent(self, movements):

        for mov in movements:
            self.render()
            pygame.display.update()
            reward = self.take_action(mov)
            pygame.time.wait(500)

            if self.won:
                print('Yay')
                pygame.time.wait(500)
                pygame.quit()
                sys.exit()

    def restart(self):
        self.game_over = False
        self.won = False
        self.player_pos = (0, 0)

    def solve_genetic_algorithm(self, population_size, gene_length):
        ga = GeneticAlgorithm(population_size, gene_length, self.action_space)
        self.population = ga.initialize_population()
        best_fitness = 0
        best_gene = []

        while not self.won:
            new_population = []
            # Evaluate fitness for each gene in the population
            for gene in self.population:
                self.restart()
                print(f"gene sequence: {gene}")
                for movement in gene:
                    self.render()
                    self.take_action(movement)
                    pygame.display.update()
                    pygame.time.wait(500)
                    
                    if self.game_over:
                        print("game over for this gene")
                        self.restart()
                        continue

                    if self.fitness >= best_fitness:
                        best_fitness = self.fitness
                        best_gene = gene
                    print(f"best gene is {best_gene}")              
            try:
                step_gene = best_gene.copy().tolist()
            except AttributeError:
                step_gene = best_gene.copy()

            for _ in range(population_size):
                new_gene = step_gene.copy()
                for _ in range(gene_length):
                    new_gene.append(random.choice(self.action_space))
                new_population.append(new_gene)
            self.population = new_population

            # Update game state using the best gene
            self.play_auto_agent(best_gene)
        
        print(f"Best gene: {best_gene}")


    def play(self, auto_agent=False):
        clock = pygame.time.Clock()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.render()
            pygame.display.update()

            # handle user input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                action = 'u'
            elif keys[pygame.K_DOWN]:
                action = 'd'
            elif keys[pygame.K_LEFT]:
                action = 'l'
            elif keys[pygame.K_RIGHT]:
                action = 'r'
            else:
                action = None

            # take action and update game state
            if action is not None:
                reward = self.take_action(action)
                if self.game_over:
                    print('Game over')
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

            # wait for a short time to slow down the game
            clock.tick(10)

ga = GeneticAlgorithm(10, 6, ["r", "u", "l", "d"])
fl = FrozenLake( population=ga.initialize_population())
fl.solve_genetic_algorithm(5, 2)
#fl.play()

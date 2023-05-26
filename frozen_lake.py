import numpy as np
import random
import pygame
import sys 
from images.load_images import load_image

player_image = load_image(f"images/student.png", size=(100, 100))
goal_image = load_image(f"images/nova.png", size=(100, 100))
hole_image = load_image(f"images/cat.png", size=(100, 100))


class FrozenLake:
    def __init__(self, size: int = 5, population: list =[], slippery: bool= False):
        self.size: int = size
        self.population: int = population
        self.board = np.zeros((size, size))
        self.player_pos = (0, 0)
        self.goal_pos = (self.size-1, self.size-1)
        self.hole_positions = self.generate_hole_positions()
        self.action_space = ['u', 'd', 'l', 'r']
        self.rewards = {'goal': 10, 'hole': -10, 'move': 0, "out-of-bounds": -0.2}
        self.total_reward = 0.0
        self.game_over = False
        self.won = False
        self.fitness = 0
        self.best_fitness = 0
        self.slippery = slippery
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.font = pygame.font.SysFont('Arial', 20)
        self.colors = {'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)}
        self.ACTIONS = {
                    'u': (-1, 0),
                    'd': (1, 0),
                    'l': (0, -1),
                    'r': (0, 1),
                }
    def generate_hole_positions(self):

        artificial_path = [(0,0), self.goal_pos]
        current_pos = (0,0)
        while current_pos != self.goal_pos:
            if current_pos[0] == self.goal_pos[0]:
                current_pos = (current_pos[0], current_pos[1]+1)
            elif current_pos[1] == self.goal_pos[1]:
                current_pos = (current_pos[0]+1, current_pos[1])
            else:
                if random.random() > 0.5:
                    current_pos = (current_pos[0], current_pos[1]+1)
                else:
                    current_pos = (current_pos[0]+1, current_pos[1])
            artificial_path.append(current_pos)
        hole_positions = []
        for i in range(self.size):
            for j in range(self.size):
                if (i,j) not in artificial_path and (i,j) not in artificial_path:
                    if random.random() < 0.4:
                        hole_positions.append((i,j))
        return hole_positions

    def render(self):
        block_size = 100
        for i in range(self.size):
            for j in range(self.size):
                rect = pygame.Rect(j * block_size, i * block_size, block_size, block_size)
                if self.player_pos == (i, j):
                    self.screen.blit(player_image, (j * block_size, i * block_size))
                    label = self.font.render('P', True, self.colors['white'])

                elif self.goal_pos == (i, j):
                    self.screen.blit(goal_image, (j * block_size, i * block_size))
                    label = self.font.render('G', True, self.colors['white'])

                elif (i, j) in self.hole_positions:
                    self.screen.blit(hole_image, (j * block_size, i * block_size))
                    label = self.font.render('H', True, self.colors['white'])

                else:
                    pygame.draw.rect(self.screen, self.colors['white'], rect)
        pygame.display.flip()


    def take_action(self, action):
        if self.game_over:
            self.player_pos = (0, 0)
        new_pos = (self.player_pos[0] + self.ACTIONS[action][0], self.player_pos[1] + self.ACTIONS[action][1])

        if self.slippery and random.random() < 0.3:
            action = random.choice([a for a in self.action_space if a != action])
            new_pos = (self.player_pos[0] + self.ACTIONS[action][0], self.player_pos[1] + self.ACTIONS[action][1])

        if new_pos[0] < 0 or new_pos[0] >= self.size or new_pos[1] < 0 or new_pos[1] >= self.size:
            self.total_reward = self.rewards['out-of-bounds']  # assign negative reward for out of board move
        elif new_pos == self.goal_pos:
            self.total_reward = self.rewards['goal']
            self.game_over = True
            self.won = True
            print('you won')
        elif new_pos in self.hole_positions:
            self.total_reward = self.rewards['hole']
            self.game_over = True
            self.fitness = 0
            print('Game Over')
        else:
            self.total_reward = self.rewards['move']
            self.player_pos = new_pos


    def play_auto_agent(self, movements):

        for mov in movements:
            self.render()
            pygame.display.update()
            reward = self.take_action(mov)
            pygame.time.wait(100)

            if self.won:
                print('Yay')
                pygame.time.wait(500)
                pygame.quit()
                sys.exit()

    def restart(self):
        self.game_over = False
        self.won = False
        self.player_pos = (0, 0)


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
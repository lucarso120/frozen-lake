import numpy as np
import random
import pygame

class FrozenLake:
    
    def __init__(self, size=4):
        self.size = size
        self.board = np.zeros((size, size))
        self.player_pos = (0, 0)
        self.goal_pos = (size-1, size-1)
        self.hole_positions = [(1,1), (3,3), (2,0)]
        self.action_space = ['Up', 'Down', 'Left', 'Right']
        self.rewards = {'goal': 10, 'hole': -10, 'move': -1}
        self.game_over = False
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

    def take_action(self, action):
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
        elif new_pos == self.goal_pos:
            reward = self.rewards['goal']
            self.game_over = True
            print('you won')
        elif new_pos in self.hole_positions:
            reward = self.rewards['hole']
            self.game_over = True
            print('Game Over')
        else:
            reward = self.rewards['move']
            self.player_pos = new_pos

        return reward

    def play(self):
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



fl = FrozenLake()
fl.play()
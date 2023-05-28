"""
This module has the exact same functionality as frozen_lake.py, but it does not use pygame.
We did this to avoid the overhead of pygame and to make the algorithm run faster.
"""

import numpy as np
import random

class FrozenLakeRaw:
    def __init__(self, size: int = 4, population: list =[], slippery: bool= False):
        self.size: int = size
        self.population: int = population
        self.board = np.zeros((size, size))
        self.player_pos = (0, 0)
        self.goal_pos = (self.size-1, self.size-1)
        self.hole_positions = self.generate_hole_positions()
        self.action_space = ['d', 'r', 'u', 'l']
        self.rewards = {'goal': 100, 'hole': -10, 'move': 1, "out-of-bounds": -0.2}
        self.total_reward = 0.0
        self.game_over = False
        self.won = False
        self.fitness = 0
        self.best_fitness = 0
        self.slippery = slippery
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
                    if random.random() < 0.3:
                        hole_positions.append((i,j))
        return hole_positions

    def take_action(self, action):
        if self.game_over:
            self.player_pos = (0, 0)
        new_pos = (self.player_pos[0] + self.ACTIONS[action][0], self.player_pos[1] + self.ACTIONS[action][1])

        if self.slippery and random.random() < 0.3:
            action = random.choice([a for a in self.action_space if a != action])
            new_pos = (self.player_pos[0] + self.ACTIONS[action][0], self.player_pos[1] + self.ACTIONS[action][1])
        if new_pos[0] < 0 or new_pos[0] >= self.size or new_pos[1] < 0 or new_pos[1] >= self.size:
            self.total_reward += self.rewards['out-of-bounds']  # assign negative reward for out of board move
        elif new_pos == self.goal_pos and not self.game_over:
            self.total_reward += self.rewards['goal']
            self.game_over = True
            self.won = True
        elif new_pos in self.hole_positions:
            self.total_reward += self.rewards['hole']
            self.game_over = True
            self.fitness = 0
        else:
            self.total_reward += self.rewards['move']
            self.player_pos = new_pos

    def play_auto_agent(self, movements):
        for mov in movements:
            reward = self.take_action(mov)
            if self.won:
                print('Yay')
                break

    def restart(self):
        self.game_over = False
        self.won = False
        self.player_pos = (0, 0)
        self.total_reward = 0.0

    def play(self, auto_agent=False):
        while not self.game_over:
            # handle user input
            if not auto_agent:
                action = input("Enter action (u/d/l/r): ")
            else:
                action = auto_agent.pop(0)

            # take action and update game state
            if action in self.action_space:
                reward = self.take_action(action)
                if self.game_over:
                    print('Game over')
                    break
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 12:00:00 2021

@author: harry
Heavily based off https://www.youtube.com/watch?v=iKdlKYG78j4&t=729s
"""
import random
from utils import Directions
import config
import numpy as np


class QAgent():

    def __init__(self, dungeon):

        # Make a copy of the world an attribute, so that Robot can
        # query the state of the world
        self.gameWorld = dungeon
        self.u_map = [] # to see
        self.rewards = [] # to hold values (int)
        self.q_values = np.zeros((config.worldLength, config.worldBreadth, 4))
        self.robot_loc = self.gameWorld.getRobotLocation()
        # Moves
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        self.moves_made = []
        
        
    def util_map(self): # builds minimap for print to console then duplicates to statemap for computation
        strawb = 1
        pits = -1
        human = -1
        #Arrays for locations
        strawb_loc = []
        human_loc = []
        pit_loc = []
        #Get Strawberry locations
        for i in range(len(self.gameWorld.getStrawberryLocation())):
            location = (self.gameWorld.getStrawberryLocation()[i].x, self.gameWorld.getStrawberryLocation()[i].y)
            strawb_loc.append(location)
            #print(gold_loc)
        
        #Get human locations
        for i in range(len(self.gameWorld.getHumanLocation())):
            location = (self.gameWorld.getHumanLocation()[i].x, self.gameWorld.getHumanLocation()[i].y)
            human_loc.append(location)
        
        #Get pit locaitons
        for i in range(len(self.gameWorld.getPitsLocation())):
            location = (self.gameWorld.getPitsLocation()[i].x, self.gameWorld.getPitsLocation()[i].y)
            pit_loc.append(location)
        
        #Create empty map of 0's same size as map
        self.u_map = np.zeros((config.worldBreadth, config.worldLength))
        self.rewards = np.zeros((config.worldBreadth, config.worldLength))
        
        #Go over all coordinates
        for x in range(config.worldBreadth):
            for y in range(config.worldLength):
                #Put in values for strawb locaiton
                self.rewards[x][y] = -0.5
                if (x,y) in strawb_loc:
                    self.u_map[x][y] = strawb
                    self.rewards[x][y] = strawb
                #Put in values for pit location
                if (x,y) in pit_loc:
                    self.u_map[x][y] = pits
                    self.rewards[x][y] = pits
                #Put in values for wumpus location
                if (x,y) in human_loc:
                    self.u_map[x][y] = human
                    self.rewards[x][y] = human
        

    #define a function that determines if the specified location is a terminal state
    def is_terminal_state(self, y, x):
        if self.rewards[x, y] == -1 or self.rewards[x, y] == -0.5: 
            return False
        else:
            return True
        
    #define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
    def get_next_action(self, y, x, epsilon):
        #if a randomly chosen value between 0 and 1 is less than epsilon, 
        #then choose the most promising value from the Q-table for this state.
        if np.random.random() < epsilon:
            return np.argmax(self.q_values[y, x])
        else: #choose a random action
            return np.random.randint(4)
        
    #define a function that will get the next location based on the chosen action
    def get_next_location(self, y, x, action):
        new_x = y
        new_y = x
        if self.moves[action] == Directions.NORTH and y > 0:
            new_x -= 1
        elif self.moves[action] == Directions.EAST and x < config.worldLength-1:
            new_y += 1
        elif self.moves[action] == Directions.SOUTH and y < config.worldBreadth-1:
            new_x += 1
        elif self.moves[action] == Directions.WEST and x > 0:
            new_y -= 1
        return new_x, new_y
    
    #Define a function that will get the shortest path
    def get_shortest_path(self, y_start, x_start):
        current_y, current_x = y_start, x_start
        shortest_path = []
        shortest_path.append([current_y, current_x])
        #continue moving along the path until we reach the goal
        while not self.is_terminal_state(current_y, current_x):
            #get the best action to take
            action = self.get_next_action(current_y, current_x, config.directionProbability)
            # add all actions to global array
            self.moves_made.append(action)
            current_y, current_x = self.get_next_location(current_y, current_x, action)
            shortest_path.append([current_y, current_x])
        
        return shortest_path
        
    def makeMove(self):
        self.util_map()
        
        epsilon = 0.2 
        discount_factor = 0.6
        learning_rate = 0.7 

        for _ in range(1000):
            y, x = self.robot_loc.x, self.robot_loc.y 

            # Loop till end state
            while not self.is_terminal_state(y, x):
                action = self.get_next_action(y, x, epsilon)

                pre_y, pre_x = y, x 
                y, x = self.get_next_location(y, x, action)
                
               
                reward = self.rewards[y, x]
                old_q_value = self.q_values[pre_y, pre_x, action]
                
                diff = reward + (discount_factor * np.max(self.q_values[y, x])) - old_q_value

                #update the Q-value for the previous state and action pair
                new_q_value = old_q_value + (learning_rate * diff)
                self.q_values[pre_y, pre_x, action] = new_q_value
                #print(self.q_values)
        
        route = self.get_shortest_path(self.robot_loc.x, self.robot_loc.y)
        for i in self.moves_made: # delete as will compute new ones each turn
            if i == 3:
                self.moves_made = []
                
                print('Now going ', Directions.SOUTH)
                return Directions.SOUTH 
            elif i == 2:
                self.moves_made = []
                print('Now going ', Directions.NORTH)
                return Directions.NORTH 
            elif i == 1:
                self.moves_made = []
                print('Now going ', Directions.EAST)
                return Directions.EAST
            elif i == 0:
                self.moves_made = []
                
                print('Now going ', Directions.WEST)
                return Directions.WEST
            

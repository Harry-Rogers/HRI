#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 16:53:00 2021

@author: harry
"""

# link.py
#
# The code that defines the behaviour of Link. You should be able to
# do all you need in here, using access methods from world.py, and
# using makeMove() to generate the next move.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20
import config
import numpy as np
from utils import Directions



class IRL():

    def __init__(self, dungeon):
        # Make a copy of the world an attribute, so that Link can
        # query the state of the world
        self.gameWorld = dungeon

        # What moves are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        self.exp_rate = 0.7
        self.states = []
        self.state_values = []
        self.map = []
        self.previous_moves = []
        

    def makeMove(self):
        self.map = self.util_map()
     
        robot_loc = (self.gameWorld.getRobotLocation().x, self.gameWorld.getRobotLocation().y)
                #Arrays for locations
        strawb_loc = []
        human_loc = []
        pit_loc = []
                
                              
        #Get Strawberry locations
        for i in range(len(self.gameWorld.getStrawberryLocation())):
            location = (self.gameWorld.getStrawberryLocation()[i].x, self.gameWorld.getStrawberryLocation()[i].y)
            strawb_loc.append(location)
                    
                
        #Get human locations
        for i in range(len(self.gameWorld.getHumanLocation())):
            location = (self.gameWorld.getHumanLocation()[i].x, self.gameWorld.getHumanLocation()[i].y)
            human_loc.append(location)
                
        #Get pit locaitons
        for i in range(len(self.gameWorld.getPitsLocation())):
            location = (self.gameWorld.getPitsLocation()[i].x, self.gameWorld.getPitsLocation()[i].y)
            pit_loc.append(location)
        #Get action
        action = self.max_action_util(self.map, robot_loc[1], robot_loc[0])
        self.previous_moves.append(action)
        print("Action chosen: ", action)
        feedback = input("Good or bad? (g/b): ")
        u_feedback = 0
        if feedback == "g":
            action = action
        elif feedback == "b":
            newAction = 0
            newAction = self.max_action_util(self.map , robot_loc[0], robot_loc[1], True)
            action = newAction
        else:
            action = action
                
        self.states.append(self.possible(self.map , robot_loc[0], robot_loc[1], action))
                
                
                
        current_state = robot_loc
        print("Action was: ", action)
        feedback = input("\n Was the action good or bad? (g/b): ")
        if feedback == "g":
            u_feedback = 1.0
        elif feedback == "b":
            u_feedback = -1.0
        else:
            u_feedback = 0.1
                
        reward = self.map[current_state] + self.exp_rate *(u_feedback - self.map[current_state])
        self.map[current_state] = round(reward, 3)
        if self.states[len(self.states)-1] == strawb_loc:
            end = True
        if self.states[len(self.states)-1] == pit_loc:
            end = True
        if self.states[len(self.states)-1] == human_loc:
            end = True
            
        self.previous_moves.append(action)
        print(self.previous_moves)
                
        return action
    
    
    def util_map(self):
        strawb = 1
        pits = -1
        human = -1
        
        #Arrays for locations
        strawb_loc = []
        human_loc = []
        pit_loc = []
        
        robot_loc = (self.gameWorld.getRobotLocation().x, self.gameWorld.getRobotLocation().y)
        
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
        u_map = np.zeros((config.worldBreadth, config.worldLength))
        #print(strawb_loc)
        
        #Go over all coordinates
        for x in range(config.worldBreadth):
            for y in range(config.worldLength):
                #Put in values for strawb locaiton
                if (x,y) in strawb_loc:
                    u_map[y][x] = strawb
                #Put in values for pit location
                if (x,y) in pit_loc:
                    u_map[y][x] = pits
                #Put in values for wumpus location
                if (x,y) in human_loc:
                    u_map[y][x] = human

        return u_map
        
    def max_action_util(self, u_map, x, y, rand=False): 
        mx_nxt_reward = 0
        
        if rand == True:    
            flag = True
            while (flag):
                action = np.random.choice(self.moves)
                action = self.repeater(action)
                return action
        
        
        
        if np.random.uniform(0,1) <= self.exp_rate:
            action = np.random.choice(self.moves)
        else:
            for a in self.moves:
                 nxt_reward_loc = self.possible(u_map, x, y, a)
                 nxt_reward_val = u_map[nxt_reward_loc[0], nxt_reward_loc[1]]
                 if nxt_reward_val >= mx_nxt_reward:
                     action = a
                     mx_nxt_reward = nxt_reward_val
        
        return action
    
    def possible(self, u_map, x, y, a):
        going_west = -1
        going_east = 1
        going_north = 1
        going_south = -1
        
        #print(x)
        #print(y)
        
        #If on edges cant move certain directions 
        if x==0:
            going_west = 0
        if x == (config.worldBreadth -1):
            going_east = 0
        if y == 0:
            going_south = 0
        if y ==(config.worldLength -1):
            going_north = 0
        
        #This is the worst way to do it but I can't think atm
        if a == Directions.WEST:
            
            if going_west == 0:
                a = self.check(a)
        if a == Directions.EAST:
            
            if going_east == 0:
                a = self.check(a)
        
        if a == Directions.SOUTH:
            if going_south == 0:
                a = self.check(a)
        
        if a == Directions.NORTH:
            if going_north == 0:
                a = self.check(a)
        
        #Gives value not location
        if a == Directions.NORTH:
            nxt = (y + going_north, x)
        elif a == Directions.SOUTH:
            nxt = (y + going_south,x)
        elif a == Directions.EAST:
            nxt = (y, x + going_east)
        else:
            nxt = (y, x + going_west)
        
        return nxt
    
    def repeater(self, action):
        holder = self.moves
        #Make sure new move can't be one we just said no to
        if action == self.previous_moves[len(self.previous_moves)-1]:
            new = np.random.choice(self.moves)
            if action == new:
                new = np.random.choice(self.moves)
            action = new
            return action
            
        return action
    

    def check(self, action):
        #create holder array
        holder = self.moves
        #find index of action in array
        index = holder.index(action)
        #delete action
        del holder[index]
        #get new action from list
        action = np.random.choice(holder)
        del holder
        return action
        
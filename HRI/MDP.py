# link.py
#
# The code that defines the behaviour of Link. You should be able to
# do all you need in here, using access methods from world.py, and
# using makeMove() to generate the next move.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20
import world
import random
import utils
import config
import time
import numpy as np
from utils import Directions


class MDP():

    def __init__(self, dungeon):
        # Make a copy of the world an attribute, so that Link can
        # query the state of the world
        self.gameWorld = dungeon

        # What moves are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        
    def makeMove(self):
        u_map = self.util_map_greed()
        robot_loc = (self.gameWorld.getRobotLocation().x, self.gameWorld.getRobotLocation().y)
        
        
        greed = self.max_action_util(u_map, robot_loc[0], robot_loc[1])
        print("Policy says to go ")
        print(self.moves[greed[1]])
        return self.moves[greed[1]]
    
    def util_map_greed(self):
        #values for formula
        gamma = 0.9
        empty = -0.01
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
        u_map = np.zeros((config.worldBreadth, config.worldLength))
        
        #Convert to list
        u_map_orig = list(u_map)
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
                #Apply utility map to original
                action = self.max_action_util(u_map_orig, x, y)
                #Assign to map
                u_map[y][x] = empty + gamma * (action[0])

                #if value is gold
                #Not sure why but does not complete all cells, explained in pdf
                if u_map[y][x] > 0.7:
                    #go to west and south and update as these are areas that are not updated
                    action, flag = self.correction_x(u_map, x,y)
                    if flag == True:
                        u_map[y][x-1] = empty + gamma * action[0]
                    if flag == False:
                        u_map[y][x+1] = empty + gamma * action[0]
            
                    action, flag = self.correction_y(u_map, x, y)
                    if flag == True:
                        u_map[y-1][x] = empty + gamma * action[0]
                    if flag == False:
                        u_map[y+1][x] = empty + gamma * action[0]
                    action = self.correction_xy(u_map, x, y)
                    u_map[y-1][x-1] = empty + gamma * (action[0])
                    #Send to try to correct all values
                    self.correction_all(u_map, x, y, empty, gamma)
        #time.sleep(0.5)
        return u_map

    #Correct the value next to gold to leave trail x coord
    def correction_x(self, u_map, x, y): 
        flag = False
        if x == 0:
            action = self.max_action_util(u_map, x +1, y)
            #print("x=0 err")
            return action, flag
        else:
            flag = True
            action = self.max_action_util(u_map, x-1, y)
            #print("x-1 err")
            return action, flag
      

    #Correct the value next to gold to leave trail y coord
    def correction_y(self,u_map, x, y):
        flag = False
        if y== 0:
            action = self.max_action_util(u_map, x, y+ 1)
            return action, flag
        else:
            flag = True
            action = self.max_action_util(u_map,x,y-1)
            return action, flag
    
    # Correct the value near gold for trail
    def correction_xy(self, u_map, x, y):
        action = self.max_action_util(u_map, x-1, y-1)
        return action

    #Try to correct all values for trail
    def correction_all(self, u_map, x, y, empty, gamma):
        #if full length, seems to go really wrong
        for i in range(2,config.worldLength -2):
            action = self.max_action_util(u_map, x -i, y)
            u_map[y][x-i] = empty + gamma * action[0]
            action = self.max_action_util(u_map, x, y-i)
            u_map[y-i][x] = empty + gamma * action[0]
            action = self.max_action_util(u_map, x-i,y-i)
            u_map[y-i][x-i] = empty + gamma * action[0]
    

        
    def max_action_util(self, u_map, x, y): 
        #Check if value is one keep it at 1 same for other values
        if u_map[y][x] == 1:
            actions = [1,1,1,1]
            return actions
        if u_map[y][x] == -1:
            actions = [-1,-1,-1,-1]
            return actions
        
        if u_map[y][x] < -0.1:
            actions = [-1,-1,-1,-1]
            return actions
       
        # Directions
        going_west = -1
        going_east = 1
        going_north = 1
        going_south = -1
        
        #If on edges cant move certain directions 
        if x==0:
            going_west = 0
        if x == (config.worldBreadth -1):
            going_east = 0
        if y == 0:
            going_south = 0
        if y ==(config.worldLength -1):
            going_north = 0

        #Direciton probabilityS
        side_direct_prob = (1-config.directionProbability)/2

        #North = probab of going north * value at north + probab of going west * value at west + probab of going east * value at east
        North = ((u_map[y + going_north][x] * config.directionProbability) + (u_map[y][x + going_west] * side_direct_prob) + (u_map[y][x + going_east] * side_direct_prob))

        #South = probab of going south * value at south + probab of going west * value at west + probab of going east * value at east
        South = ((u_map[y + going_south][x] * config.directionProbability) + (u_map[y][x + going_west] * side_direct_prob) + (u_map[y][x + going_east] * side_direct_prob))

        #East = = probab of going east * value at east + probab of going north * value at north + probab of going south * value at south
        East = ((u_map[y][x + going_east] * config.directionProbability) + (u_map[y + going_north][x] * side_direct_prob) + (u_map[y + going_south][x] * side_direct_prob))

        #West = = probab of going west * value at west + probab of going north * value at north + probab of going south * value at south
        West = ((u_map[y][x + going_west] * config.directionProbability) + (u_map[y + going_north][x] * side_direct_prob) + (u_map[y + going_south][x] * side_direct_prob))
        
        #Actions list
        actions = [North,South,East,West]
        
        #find max value in list
        max_action = max(actions)

        #find index of max value in list
        action_index = actions.index(max_action)
        
        return (max_action, action_index, actions)
                    

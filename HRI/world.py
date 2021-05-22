# world.py
#
# A file that represents the Wumpus World, keeping track of the
# position of all the objects: pits, Wumpus, gold, and the agent, and
# moving them when necessary.
#
# Written by: Simon Parsons
# Edited by: Harry Rogers
# Last Modified: 22/05/21

import random
import config
import utils
from utils import Pose
from utils import Directions
from utils import State

class World():

    def __init__(self):

        # Import boundaries of the world. because we index from 0,
        # these are one less than the number of rows and columns.
        self.maxX = config.worldLength - 1
        self.maxY = config.worldBreadth - 1
        print(self.maxX)
        print(self.maxY)

        # Human
        self.hLoc = []
        for i in range(config.numberOfHuman):
            self.hLoc.append(utils.pickRandomPose(self.maxX, self.maxY))

        # Robot
        self.rLoc = utils.pickRandomPose(self.maxX, self.maxY)

        # Strawberry
        self.sLoc = []
        for i in range(config.numberOfStrawb):
            self.sLoc.append(utils.pickRandomPose(self.maxX, self.maxY))

        # Pits
        self.pLoc = []
        for i in range(config.numberOfPits):
            self.pLoc.append(utils.pickRandomPose(self.maxX, self.maxY))

        # Game state
        self.status = State.PLAY

        # Did Link just successfully loot some gold?
        self.looted = False
        
        
    #
    # Access Methods
    #
    # These are the functions that should be used by Link to access
    # information about the world.

    # Where is/are the Wumpus?
    def getHumanLocation(self):
        return self.hLoc

    # Where is Link?
    def getRobotLocation(self):
        return self.rLoc

    # Where is the Gold?
    def getStrawberryLocation(self):
        return self.sLoc

    # Where are the Pits?
    def getPitsLocation(self):
        return self.pLoc

    # Did we just loot some strawberries?
    def justLooted(self):
        return self.looted

    # What is the current game state?
    def getGameState(self):
        return self.status

    #
    # Methods
    #
    # These are the functions that are used to update and report on
    # world information.

    def isEnded(self):
        dead = False
        won = False
        # Has Robot met the Human?
        for i in range(len(self.hLoc)):
            if utils.sameLocation(self.rLoc, self.hLoc[i]):
                print("Oops! Met the Human")
                dead = True
                self.status = State.LOST
                
        # Did Robot fall in a Pit?
        for i in range(len(self.pLoc)):
            if utils.sameLocation(self.rLoc, self.pLoc[i]):
                print("Arghhhhh! Fell in a pit")
                dead = True
                self.status = State.LOST

        # Did Robot loot all the Strawberries?
        if len(self.sLoc) == 0:
            won = True
            self.status = State.WON
            
        if dead == True or won == True:
            print("Game Over!")
            return True
            
    # Implements the move chosen by Robot
    def updateRobot(self, direction):
        # Set the looted flag to False
        self.looted = False
        # Implement non-determinism if appropriate
        direction = self.probabilisticMotion(direction)
        if direction == Directions.NORTH:
            if self.rLoc.y < self.maxY:
                self.rLoc.y = self.rLoc.y + 1
            
        if direction == Directions.SOUTH:
            if self.rLoc.y > 0:
                self.rLoc.y = self.rLoc.y - 1
                
        if direction == Directions.EAST:
            if self.rLoc.x < self.maxX:
                self.rLoc.x = self.rLoc.x + 1
                
        if direction == Directions.WEST:
            if self.rLoc.x > 0:
                self.rLoc.x = self.rLoc.x - 1

        # Did Robot just loot some strawberries?
        match = False
        index = 0
        for i in range(len(self.sLoc)):
            if utils.sameLocation(self.rLoc, self.sLoc[i]):
                match = True
                index = i
                self.looted = True
                print("Strawberry, yeah!")

        # Assumes that strawberries have different locations. Or, that only
        # one strawberry can be picked up in a given turn.
        if match:
            self.sLoc.pop(index)

    # Implement nondeterministic motion, if appropriate.
    def probabilisticMotion(self, direction):
        if config.nonDeterministic:
            dice = random.random()
            if dice < config.directionProbability:
                return direction
            else:
                return self.sideMove(direction)
        else:
            return direction
        
    # Move at 90 degrees to the original direction.
    def sideMove(self, direction):
        # Do we head left or right of the intended direction?
        dice =  random.random()
        if dice > 0.5:
            left = True
        else:
            left = False
        if direction == Directions.NORTH:
            if left:
                return Directions.WEST
            else:
                return Directions.EAST

        if direction == Directions.SOUTH:
            if left:
                return Directions.EAST
            else:
                return Directions.WEST

        if direction == Directions.WEST:
            if left:
                return Directions.SOUTH
            else:
                return Directions.NORTH

        if direction == Directions.EAST:
            if left:
                return Directions.NORTH
            else:
                return Directions.SOUTH
            
    # Move the Wumpus if that is appropriate
    #
    # Need a decrementDifference function to tidy things up
    #
    def updateHuman(self, movement):
        if config.dynamic:
            if movement == True:
                print("Moving randomly")
                #Moving in positive direction
                direction = random.randint(1, 4)
                for i in range(len(self.hLoc)):
                    if direction == 1:
                        #1 is North (Down the dungeon)
                        self.hLoc[i].y = self.hLoc[i].y + 1
                        if self.hLoc[i].y > self.maxY:
                            #Undo the addition
                            self.hLoc[i].y = self.hLoc[i].y -1
                            print("Can't leave")
                        print("Going somewhere")
                    if direction == 2:
                        #2 is South (Up the dungeon)
                        self.hLoc[i].y = self.hLoc[i].y - 1
                        if self.hLoc[i].y < 0:
                            #Undo cant leave
                            self.hLoc[i].y = self.hLoc[i].y + 1
                            print("Can't leave")

                    if direction == 3:
                        #3 is East (Right of dungeon)
                        self.hLoc[i].x = self.hLoc[i].x + 1
                        if self.hLoc[i].x > self.maxX:
                            self.hLoc[i].x = self.hLoc[i].x - 1
                            print("Can't leave")
                    if direction == 4:
                        #4 is west (Left of dungeon)
                        self.hLoc[i].x = self.hLoc[i].x - 1
                        if self.hLoc[i].x < 0:
                            self.hLoc[i].x = self.hLoc[i].x + 1
                            print("Can't leave")
            else:  
                # Head towards Robot
                target = self.rLoc
                for i in range(len(self.hLoc)):
                    # If same x-coordinate, move in the y direction
                    if self.hLoc[i].x == target.x:
                        self.hLoc[i].y = self.reduceDifference(self.hLoc[i].y, target.y)      
                        print(self.hLoc[i].y)

                    # If same y-coordinate, move in the x direction
                    elif self.hLoc[i].y == target.y:
                        self.hLoc[i].x = self.reduceDifference(self.hLoc[i].x, target.x)      
                        print(self.hLoc[i].x)
                    # If x and y both differ, approximate a diagonal
                    # approach by randomising between moving in the x and
                    # y direction.
                    else:
                        dice = random.random()
                        if dice > 0.5:
                            self.hLoc[i].y = self.reduceDifference(self.hLoc[i].y, target.y)     
                            print(self.hLoc[i].y)
                        else:
                            self.hLoc[i].x = self.reduceDifference(self.hLoc[i].x, target.x)       
                            print(self.hLoc[i].x)

    # Move value towards target.
    def reduceDifference(self, value, target):
        if value < target:
            return value+1
        elif value > target:
            return value-1
        else:
            return value
            
        

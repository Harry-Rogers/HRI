# dungeon.py
#
# Code to display information about the game in a window.
#
# Shouldn't need modifying --- only changes what gets shown, not what
# happens in the game.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

from utils import Pose
from graphics import *
import config

class Dungeon():

    def __init__(self, dungeon):
        # Make a copy of the world an attribute, so that the graphics
        # have access.
        self.gameWorld = dungeon

        # How many pixels the grid if offset in the window
        self.offset = 10
        
        # How many pixels correspond to each coordinate.
        #
        # This works with the current images. any smaller and the
        # images will not fit in the grid.
        self.magnify = 40

        # How big to make "characters" when not using images
        self.cSize = 0.4

        # How big to make objects when not using images.
        self.oSize = 0.6

        # Setup window and draw objects
        self.pane = GraphWin("Simulation", ((2*self.offset)+((self.gameWorld.maxX+1)*self.magnify)), ((2*self.offset)+((self.gameWorld.maxY+1)*self.magnify)))
        self.pane.setBackground("white")
        self.drawBoundary()
        self.drawGrid()
        self.drawBot()
        self.drawHuman()
        self.drawPits()
        self.drawStrawb()

    #
    # Draw the world
    #
    
    # Put a box around the world
    def drawBoundary(self):
        rect = Rectangle(self.convert(0, 0), self.convert(self.gameWorld.maxX+1, self.gameWorld.maxY+1))
        rect.draw(self.pane)

    # Draw gridlines, to visualise the coordinates.
    def drawGrid(self):
        # Vertical lines
        vLines = []
        for i in range(self.gameWorld.maxX+1):
            vLines.append(Line(self.convert(i, 0), self.convert(i, self.gameWorld.maxY+1)))
        for line in vLines:
            line.draw(self.pane)
        # Horizontal lines
        hLines = []
        for i in range(self.gameWorld.maxY + 1):
            hLines.append(Line(self.convert(0, i), self.convert(self.gameWorld.maxX+1, i)))
        for line in hLines:
            line.draw(self.pane)

    #
    # Draw the characters
    #

    # We either use an image of bot, or a green circle
    def drawBot(self):
        if config.useImage:
            self.bot = Image(self.convert2(self.gameWorld.rLoc.x, self.gameWorld.rLoc.y), "images/robot.png")
        else:
            self.bot = Circle(self.convert2(self.gameWorld.rLoc.x, self.gameWorld.rLoc.y), self.cSize*self.magnify)
            self.bot.setFill('green')
        self.bot.draw(self.pane)

    # We either use an image of a scary monster face, or a red circle
    def drawHuman(self):
        self.human = []
        for i in range(len(self.gameWorld.hLoc)):
            if config.useImage:
                self.human.append(Image(self.convert2(self.gameWorld.hLoc[i].x, self.gameWorld.hLoc[i].y), "images/human.png"))
            else:
                self.human.append(Circle(self.convert2(self.gameWorld.hLoc[i].x, self.gameWorld.hLoc[i].y),  self.cSize*self.magnify))
                self.human[i].setFill('red')
        for i in range(len(self.gameWorld.hLoc)): 
            self.human[i].draw(self.pane)

    #
    # Draw the objects
    #
    
    # drawPits()
    #
    # The calculation for bot and Human gives the centre of the
    # square. For a pit we need to move the x and y to either side of
    # this by 0.5*oSize*magnify.
    def drawPits(self):
        self.pits = []
        for i in range(len(self.gameWorld.pLoc)):
            centre = self.convert2(self.gameWorld.pLoc[i].x, self.gameWorld.pLoc[i].y)
            centreX = centre.getX()
            centreY = centre.getY()
            point1 = Point(centreX - 0.5*self.oSize*self.magnify, centreY - 0.5*self.oSize*self.magnify)
            point2 = Point(centreX + 0.5*self.oSize*self.magnify, centreY + 0.5*self.oSize*self.magnify)
            self.pits.append(Rectangle(point1, point2))
            self.pits[i].setFill('black')
        for i in range(len(self.gameWorld.pLoc)): 
            self.pits[i].draw(self.pane)

    def drawStrawb(self):
        self.strawb = []
        for i in range(len(self.gameWorld.sLoc)):
            # If we use an image, do the same as for bot and the Human
            if config.useImage:
                self.strawb.append(Image(self.convert2(self.gameWorld.sLoc[i].x, self.gameWorld.sLoc[i].y), "images/Strawberry.png"))
            # Otherwise, do the same as for the pits
            else:
                centre = self.convert2(self.gameWorld.sLoc[i].x, self.gameWorld.sLoc[i].y)
                centreX = centre.getX()
                centreY = centre.getY()
                point1 = Point(centreX - 0.5*self.oSize*self.magnify, centreY - 0.5*self.oSize*self.magnify)
                point2 = Point(centreX + 0.5*self.oSize*self.magnify, centreY + 0.5*self.oSize*self.magnify)
                self.strawb.append(Rectangle(point1, point2))
                self.strawb[i].setFill('strawb')
        for i in range(len(self.gameWorld.sLoc)): 
            self.strawb[i].draw(self.pane)

    # We don't need to redraw the pits, since they never change.
    def update(self):
        for i in range(len(self.gameWorld.sLoc)): 
            self.strawb[i].undraw()
        self.drawStrawb()
        self.bot.undraw()
        self.drawBot()
        for i in range(len(self.gameWorld.hLoc)): 
            self.human[i].undraw()
        self.drawHuman()

    # Take x and y coordinates and transform them for using offset and
    # magnify.
    #
    # This conversion works for the lines. 
    def convert(self, x, y):
        newX = self.offset + (x * self.magnify)
        newY = self.offset + (y * self.magnify)
        return Point(newX, newY)

    # Take x and y coordinates and transform them for using offset and
    # magnify.
    #
    # This conversion works for objects, returning the centre of the
    # relevant grid square.
    def convert2(self, x ,y):
        newX = (self.offset + 0.5*self.magnify) + (x * self.magnify)
        newY = (self.offset + 0.5*self.magnify) + (y * self.magnify)
        return Point(newX, newY)

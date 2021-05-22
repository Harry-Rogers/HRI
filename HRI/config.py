# config.py
#
# Configuration information for the Wumpus World. These are elements
# to play with as you develop your solution.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

# Dimensions in terms of the numbers of rows and columns
worldLength = 10
worldBreadth = 10

# Features
numberOfHuman = 1
numberOfPits = 1
numberOfStrawb = 1

# Control dynamism
#
# If dynamic is True, then the Wumpus will move.
dynamic = True

# Control observability --- NOT YET IMPLEMENTED
#
# If partialVisibility is True, Link will only see part of the
# environment.
partialVisibility = False
#
# The limits of visibility when visibility is partial
sideLimit = 1
forwardLimit = 5

# Control determinism
#
# If nonDeterministic is True, Link's action model will be
# nonDeterministic.
nonDeterministic = False
#
# If Link is nondeterministic, probability that they carry out the
# intended action:
directionProbability = 0.8

# Control images
#
# If useImage is True, then we use images for Link, Wumpus and
# Gold. If it is False, then we use simple colored objects.
useImage = True


#Algorithms, change these 
MDP = True
Q_Learning = False
SPARC = False

if Q_Learning == True:
    dynamic = False
# game.py
#
# The top level loop that runs the game until Link wins or loses.
#
# run this using:
#
# python3 game.py
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

from world import World
from MDP  import MDP
from dungeon import Dungeon
from q_learning_agent import QAgent
from IRLPLUS import IRL

import utils
import time

# How we set the game up. Create a world, then connect player and
# display to it.
gameWorld = World()
player = IRL(gameWorld)
display = Dungeon(gameWorld)

#Set to true for random movements from Human
random_move = False

# Now run...
while not(gameWorld.isEnded()):
    gameWorld.updateHuman(random_move)
    gameWorld.updateRobot(player.makeMove(end = False))
    #utils.printGameState(gameWorld)
    display.update()
    time.sleep(0.1)

if gameWorld.status == utils.State.WON:
    print("You won!")
else:
    print("You lost!")

from Players.randomPlayer import RandomPlayer
from world import World
from Players.playerFunctions import selectRandomMove, shortestMoves
import numpy as np

class SnailPlayer(RandomPlayer):
    '''
        A player that move only one tiles at a time.
    '''
    def __init__(self):
        super().__init__()
    
    def placePenguin(self, world: World):
        return super().placePenguin(world)
    
    def chooseMove(self, world: World):
        playable, movesList = world.possibleMove(self.name)
        if not playable:
            return None
        return selectRandomMove(shortestMoves(movesList, self, world))
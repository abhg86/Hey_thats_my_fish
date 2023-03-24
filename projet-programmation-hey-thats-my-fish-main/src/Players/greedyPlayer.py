from Players.randomPlayer import RandomPlayer
from world import World
from Players.playerFunctions import selectRandomMove, higherScoreMoves

class GreedyPlayer(RandomPlayer):
    '''
        A player that choose the tiles with highest amount of point.
    '''
    def __init__(self):
        super().__init__()
    
    def placePenguin(self, world: World):
        return super().placePenguin(world)
    
    def chooseMove(self, world: World):
        playable, movesList = world.possibleMove(self.name)
        if not playable:
            return None
        return selectRandomMove(higherScoreMoves(movesList, self, world))
    
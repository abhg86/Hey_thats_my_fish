from Players.randomPlayer import RandomPlayer
from world import World
from Players.playerFunctions import selectRandomMove, farthestMoves

class HarePlayer(RandomPlayer):
    '''
        A player that always go the farthest.
    '''
    def __init__(self):
        super().__init__()
    
    def placePenguin(self, world: World):
        return super().placePenguin(world)
    
    def chooseMove(self, world: World):
        playable, movesList = world.possibleMove(self.name)
        if not playable:
            return None
        return selectRandomMove(farthestMoves(movesList, self, world))
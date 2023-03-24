from Players.randomPlayer import RandomPlayer
from world import World
from Players.playerFunctions import selectRandomMove, closestMoves

class ChaserPlayer(RandomPlayer):
    '''
        A player that try to go the closest to other player. Randomly move without other player.
    '''
    def __init__(self):
        super().__init__()
    
    def placePenguin(self, world: World):
        return super().placePenguin(world)
    
    def chooseMove(self, world: World):
        playable, movesList = world.possibleMove(self.name)
        if not playable:
            return None
        moves = closestMoves(movesList, self, world)
        if len(moves) == 0:
            return selectRandomMove(movesList)
        else:
            return selectRandomMove(moves)
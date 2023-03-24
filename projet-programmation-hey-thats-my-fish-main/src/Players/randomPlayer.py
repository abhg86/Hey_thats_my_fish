from playerDummy import PlayerDummy
from world import World
from Players.playerFunctions import selectRandomMove

class RandomPlayer(PlayerDummy):
    '''
        A player that randomly choose between valid move.
    '''
    def __init__(self):
        super().__init__()

    def placePenguin(self, world: World):
        return selectRandomMove(world.possiblePenguinPlacement())   # Get the possible position for a penguin


    def chooseMove(self, world : World):
        playable, movesList = world.possibleMove(self.name)         # Get the possible moves for this player
        if not playable:
            return None 
        return selectRandomMove(movesList)
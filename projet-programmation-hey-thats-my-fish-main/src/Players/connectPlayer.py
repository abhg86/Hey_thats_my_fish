from Players.randomPlayer import RandomPlayer
from world import World
from Players.playerFunctions import selectRandomMove, keepConnectedMove, higherConnectedMove

class ConnectedPlayer(RandomPlayer):
    '''
        A player that try to keep the world connected and if it doesn't, take the best part.
    '''
    def __init__(self):
        super().__init__()
    
    def placePenguin(self, world: World):
        return super().placePenguin(world)
    
    def chooseMove(self, world: World):
        playable, movesList = world.possibleMove(self.name)
        if not playable:
            return None
        
        moves = higherConnectedMove(movesList, self, world)
        if len(moves) == 0:
            return selectRandomMove(movesList)
        
        movesList = keepConnectedMove(higherConnectedMove(moves, self, world), self, world)
        if len(movesList) == 0:
            return selectRandomMove(moves)
        
        return selectRandomMove(movesList)
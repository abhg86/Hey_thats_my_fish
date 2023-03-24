from abc import ABC, abstractmethod
from world import World

class PlayerDummy(ABC):
    name = 1
    def __init__(self):
        self.name = self.name
        PlayerDummy.name += 1

    def __del__(self):
        PlayerDummy.name -= 1
        
    @abstractmethod
    def placePenguin(self, world : World):
        pass

    @abstractmethod
    def chooseMove(self, world : World):
        pass
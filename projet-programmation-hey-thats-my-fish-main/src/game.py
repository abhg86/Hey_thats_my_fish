import numpy as np
from world import World
from Players.randomPlayer import RandomPlayer
from graphicsDummy import GraphicsDummy

import gameParameters as param

class Game:

    def __init__(self, 
                 affichage = None, 
                 players = None, 
                 height = param.basicHeight, 
                 width = param.basicWidth, 
                 nbPenguinsPerPlayer = param.basicNbPenguinsPerPlayer):
        self.height = height
        self.width = width
        self.players = players if players is not None else [RandomPlayer() for _ in range(param.basicNbPlayers)]
        self.nbPlayers = len(self.players)
        self.nbPenguinsPerPlayers = nbPenguinsPerPlayer
        self.world = World(self.height, self.width, self.nbPlayers, self.nbPenguinsPerPlayers * self.nbPlayers)
        self.world.initWorld()
        self.turn = 0
        self.affichage = affichage if affichage is not None else GraphicsDummy()

    def nextTurn(self):
        self.turn += 1
        for player in self.players:
            self.affichage.showWorld(self.world)
            move = player.chooseMove(self.world)
            if move is not None: 
                idPenguin, direction, distance = move
                self.world.move(player.name, idPenguin, direction, distance)
        if self.world.isFinished():
            return False
        return True

    def play(self):
        for penguin in range(self.nbPenguinsPerPlayers):
            for player in self.players:
                self.affichage.showWorld(self.world)
                while not(self.world.addPenguin(player.name, player.placePenguin(self.world))):
                    pass
        
        while self.nextTurn():
            pass
        
        self.affichage.endDisplay()
        return self.world.points

if __name__ == "__main__":
    from Graphics.graphicsPygame import GraphicsPygame
    from playerImport import *

    #players = [ConnectedPlayer(), ChaserPlayer()]
    players=[HumanPlayer(), RandomPlayer(), HarePlayer(), ConnectedPlayer()]
    graphics = GraphicsPygame()
    #graphics = GraphicsDummy()

    game = Game(players=players, affichage=graphics)
    finalScore = game.play()
    
    winner = None
    winnerScore = None
    for player in players:
        if winner is None or winnerScore < finalScore[player.name - 1]:
            winner = player
            winnerScore = finalScore[player.name - 1]
        print(f'Player : {type(player).__name__} {player.name}\n\tScore : {finalScore[player.name - 1]}')
    print(f'The winner is player {type(winner).__name__} {winner.name} with a score of {winnerScore}')
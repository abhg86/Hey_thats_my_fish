import numpy as np
import gameParameters as param

class World(object):
    column_alignement = param.column_alignement
    if column_alignement:
        evenDirections = [[0, -1], [1, -1], [1, 0], [0, 1], [-1, 0], [-1, -1]]
        oddDirections  = [[0, -1], [1,  0], [1, 1], [0, 1], [-1, 1], [-1,  0]]
    else :
        evenDirections = [[-1, 0], [-1, -1], [0, -1], [1, 0], [0, 1], [-1, 1]]
        oddDirections  = [[-1, 0], [ 0, -1], [1, -1], [1, 0], [1, 1], [ 0, 1]]

    def __init__(self, height : int, width : int, nbPlayers : int, nbPenguins : int):
        self.height = height
        self.width = width
        
        self.grid = np.zeros((width, height), dtype = int) - 1 # Empty world
        self.coordonnate = np.array([[(i,j) for j in range(height)] for i in range(width)])

        self.pointsTiles = [height*width] # Only tiles with 0 points
        self.pointDistribution = np.zeros((width, height), dtype = int)

        self.nbPlayers = nbPlayers
        self.listPlayers = np.array([i + 1 for i in range(nbPlayers)])
        self.nbPenguins = nbPenguins  
        self.penguins = [[] for _ in range(nbPlayers)]
        self.points = np.zeros(nbPlayers, dtype = int)
    
    def changeRepresentation(self, column_alignement: bool):
        '''
            Allow to change the perception of the world.
        '''
        self.column_alignement = column_alignement
        if self.column_alignement:
            self.evenDirections = [[0, -1], [1, -1], [1, 0], [0, 1], [-1, 0], [-1, -1]]
            self.oddDirections  = [[0, -1], [1,  0], [1, 1], [0, 1], [-1, 1], [-1,  0]]
        else :
            self.evenDirections = [[-1, 0], [-1, -1], [0, -1], [1, 0], [0, 1], [-1, 1]]
            self.oddDirections  = [[-1, 0], [ 0, -1], [1, -1], [1, 0], [1, 1], [ 0, 1]]
    
    def initWorldFromFile(self, file):
        '''
            Input:
                file : txt or pickle file describing a world
            Open a file and make the world described by it.
        '''
        pass

    def initWorldFromStr(self, column_alignement: bool, world: str):
        '''
            Input:
                column_alignement : bool
                world : string describing a world such as
                if column_alignement:
                    _1   1   \n
                    _1 1 1 1 \n
                    _2 1 3 1 \n
                    _1 1 2 1 \n
                    _  2   3 \n
                else:
                    _1 1 1 1 \n
                    _ 1 1 1 1 \n
                    _2 1 3 1 \n
                    _ 1 2 2 3 \n

            Create a world from a string
        '''
        self.changeRepresentation(column_alignement)

        lines = world.split('\n')[:-1]
    
        self.height = len(lines) - 1*column_alignement
        self.width = (len(lines[0]) - 1)//2

        self.grid = np.zeros((self.width, self.height), dtype = int) - 1
        self.coordonnate = np.array([[(i,j) for j in range(self.height)] for i in range(self.width)])

        self.pointDistribution = np.zeros((self.width, self.height), dtype = int)

        for i in range(self.width):
            for j in range(self.height):
                char = lines[j + (i%2)][2*i + 1] if column_alignement else lines[j][2*i + 1 + (j%2)]
                if char != ' ':
                    self.pointDistribution[i][j] = int(char)
                    self.grid[i][j] = 0                 

    def print(self):
        '''
            Printing a world as a string.
        '''
        text = ['_' for _ in range(self.height + self.column_alignement)]
        if self.column_alignement:
            for i in range(self.width):
                text[0] += '  '*(i%2)
                for j in range(self.height):
                    if self.grid[i][j] >= 0:
                        text[j + (i%2)] += f'{self.pointDistribution[i][j]}'
                    else:
                        text[j + (i%2)] += ' '
                    text[j + (i%2)] += ' '
                text[-1] += '  '*(1-i%2)                    
        else:
            for j in range(self.height):
                text[j] += ' '*(j%2)
                for i in range(self.width):
                    if self.grid[i][j] >= 0:
                        text[j] += f'{self.pointDistribution[i][j]}'
                    else:
                        text[j] += ' '
                    text[j] += ' '
        print(f"{' World ':=^64}")
        for line in text:
            print(line)
        print('='*64)
    
    def initWorld(self):
        '''
            Initializing a world from default parameters 
        '''
        # Allowing all the tiles
        self.grid *= 0

        # Removing some tiles that are not in the real game
        if param.column_alignement:
            for i in range(self.width):
                if i % 2 == 1:
                    self.grid[i][-1] = -1
        else:
            for j in range(self.height):
                if j % 2 == 1:
                    self.grid[-1][j] = -1
        
        # Creating the points distribution
        nbTiles = int((self.grid >= 0).sum())
        self.pointsTiles = [round(proba * nbTiles) for proba in param.pointProbability]
        nbTiles = np.sum(self.pointsTiles)
        tilesOrder = np.zeros(nbTiles, dtype = int)
        index = 0
        for value, number in enumerate(self.pointsTiles):
            for _ in range(number):
                tilesOrder[index] = value
                index += 1
        # Randomly attributing a number of points to a tile.
        np.random.shuffle(tilesOrder)
        index = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] >= 0:
                    self.pointDistribution[i][j] = tilesOrder[index]
                    index += 1

    def addPenguin(self, player, penguin):
        '''
            Input:
                self
                player : int [|1; 4|], player name
                penguin : [i, j] coordonate of a penguin
            Allowing a player to place a penguin.
            Return if the penguin has been placed.
        '''
        if penguin is None:
            raise Exception

        [x, y] = penguin
        if (self.pointDistribution[x, y] > 1     # We cannot place a penguin on a plate with a score greater than 1.
         or self.grid[x][y] != 0                 # We can place a penguin only on an existing plate with no obstacle.
         or not (0 <= player - 1 < self.nbPlayers)      # Verify if it is a valide player.
         or not (len(self.penguins[player - 1]) < (self.nbPenguins // self.nbPlayers)) ): # Verify if the player has not placed all his penguins.
            return False

        self.penguins[player - 1].append(penguin)
        self.grid[x][y] = player
        return True

    def addDirection(coordonate, direction):
        '''
            Input:
                coordonate : [i, j]
                direction : int [|0; 5|]
            Return the coordonate of the tiles when you move from start in direction.
        '''
        if coordonate[1 - param.column_alignement] % 2 == 0:
            directionVector = World.evenDirections[direction]
        else:
            directionVector = World.oddDirections[direction]
        return [coordonate[0] + directionVector[0], coordonate[1] + directionVector[1]]

    def makeMove(self, player : int, move):
        '''
            Input:
                self
                player : int [|1; 4|], player name
                move : [idPenguin, direction, distance]
            Return the coordonate of of the penguin after the move, None if the move is not valid.
        '''
        [idPenguin, direction, distance] = move
        coord = self.penguins[player - 1][idPenguin]
        
        for _ in range(distance):
            coord = World.addDirection(coord, direction)
            if not(0 <= coord[0] < self.height) or not(0 <= coord[1] < self.width): # Out Of Range
                return None 
            if self.grid[coord[0]][coord[1]] != 0: # Verify if their are no obstacle.
                return None
        
        return coord

    def move(self, player : int, idPenguin : int, direction : int, distance : int):
        '''
            Input:
                self
                player : int [|1; 4|], player name
                idPenguin : int
                direction : int [|0; 5|]
                distance : int
            Do the move if the move is valid, else do nothing.
            Return if the move has been done.  
        '''
        # Return if the move is valide, and if it is, do the move.
        start = self.penguins[player - 1][idPenguin]
        if self.grid[start[0]][start[1]] != player:
            return False    # Starting coordonate 

        if not (0 <= direction <= 5):
            return False
        
        if distance < 1:
            return False    # distance not valide, must be at least 1.

        if (coord := self.makeMove(player, [idPenguin, direction, distance])) is None:
            return False

        self.penguins[player - 1][idPenguin] = (coord[0], coord[1])
        self.grid[start[0]][start[1]] = -1      # Remove the starting plate.
        self.grid[coord[0]][coord[1]] = player  # Changing the player position.
        self.points[player - 1] += self.pointDistribution[start[0]][start[1]]   # Adding the score from the starting plate.
        return True

    def possiblePenguinPlacement(self):
        '''
            Return a list of possible coordonate where a penguin can be placed
        '''
        return self.coordonnate[np.logical_and(self.grid == 0, self.pointDistribution <= 1)]

    def possibleMove(self, player):
        '''
            Input:
                self
                player : int [|1; 4|], player name
            Return a couple (if the player is still in game, list of possible move of a player).
        '''
        # possible move: [startingPoint, direction, distance]

        possibleMoves = []
        for i in range(len(self.penguins[player - 1])):
            for direction in range(6): # 6 = len(self.directions)
                coordonate = World.addDirection(self.penguins[player - 1][i], direction)
                distance = 1
                while (0 <= coordonate[0] < self.height 
                   and 0 <= coordonate[1] < self.width 
                   and self.grid[coordonate[0]][coordonate[1]] == 0):
                    possibleMoves.append([i, direction, distance])
                    distance += 1
                    coordonate = World.addDirection(coordonate, direction)

        if len(possibleMoves) == 0:
            return (False, np.array([]))  # No possible move = player out of the game.

        return (True, np.array(possibleMoves))
    
    def dataForIA(self, player):
        fgrid = np.zeros((self.height, self.width), dtype = int)
        fgrid[0 < self.grid] = -1       # All players plates are set to -1
        fgrid[self.grid == player] = 1  # player plates are set to 1
        
        pgrid = np.zeros((self.height, self.width), dtype = int)
        mask = (self.grid == 0)
        pgrid[mask] = self.pointDistribution[mask]  # Points of Plates with no player.
        pgrid[0 < self.grid] = -1                   # Plates with another player are set to -1.
        pgrid[self.grid == player] = 0              # Plates with the player are set to 0.
        
        return fgrid, pgrid
    
    def get_pingouin_coordinates(self, player : int, pingouin : int):
        ''' 
            Return the coordinate of the pingouin of the player 
        '''
        return self.penguins[player - 1][pingouin]
    
    def get_points(self, player : int):
        '''
            Return the points of the player
        '''
        return self.points[player - 1]

    def isFinished(self):
        '''
            Return if no player can play. If so, that mean that the game is finished.
        '''
        endOfGame = True
        for player in range(self.nbPlayers):
            canPlay, _ = self.possibleMove(player + 1)
            if canPlay:
                endOfGame = False
            else:
                for (x,y) in self.penguins[player]:
                    self.grid[x][y] = -1      # Remove the starting plate.
                    self.points[player] += self.pointDistribution[x,y]
                self.penguins[player] = []
        return endOfGame

if __name__ == "__main__":
    from Graphics.graphicsPygame import GraphicsPygame
    from Players.randomPlayer import RandomPlayer
    from textwrap import dedent
    graphics = GraphicsPygame()
    height = 8
    width = 8
    nbPlayers = 4
    nbPinguinsPerPlayer = 2
    world_txt = '''\
                _  1 1 1 1       1 1 
                _     1   1     1   1 
                _    1     1     1 1 
                _           1         
                _1 1 1 1   1 1 1 1 1 
                _     1               
                _      1         1   
                _       1 1 1     1   
                _  1   1     1     1 
                _   1 1       1 1   1 
                '''
    world = World(height, width, nbPlayers, nbPinguinsPerPlayer*nbPlayers)
    world.initWorldFromStr(False, dedent(world_txt))
    
    #print(world.grid)
    #print(world.pointDistribution)
    #print(world.possiblePenguinPlacement())
    #print(world.grid)
    
    #while graphics.display:
    #    graphics.showWorld(world)

    world_txt = '''\
                _                    
                _    1   1   1       
                _  1                 
                _      1 1     1 1   
                _  1       1         
                _          1     1   
                _  1     1 1     1   
                _        1           
                _      1   1 1 1     
                _                    
                _                    
                '''
    world.initWorldFromStr(True, dedent(world_txt))
    players = [RandomPlayer() for _ in range(nbPlayers)]
    
    while graphics.display:
        graphics.showWorld(world)
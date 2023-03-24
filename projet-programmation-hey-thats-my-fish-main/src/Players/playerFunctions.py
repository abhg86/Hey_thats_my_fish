from world import World
from playerDummy import PlayerDummy

from textwrap import dedent

import gameParameters as param
import numpy as np
import copy

def selectRandomMove(movesList):
    '''
        Input:
            movesList : np.array of move [penguin, direction, distance]
        Return a random move.
    '''
    if len(movesList) == 0:
        return None
    return movesList[np.random.choice(movesList.shape[0], 1, replace = False)][0]


def farthestMoves(movesList, player : PlayerDummy, world : World):
    '''
        Input:
            movesList : np.array of move [penguin, direction, distance]
            player : an instance of Player
            world : an instance of World
        Return a sublist of movesList with the higher distance.
    '''
    moves = []
    maxDist = None
    for move in movesList:
        if maxDist is None or maxDist < move[2]:
            maxDist = move[2]
            moves = []
        if move[2] == maxDist:
            moves.append(move)
    return np.array(moves)


def shortestMoves(movesList, player : PlayerDummy, world : World):
    '''
        Input:
            movesList : np.array of move [penguin, direction, distance]
            player : an instance of Player
            world : an instance of World
        Return a sublist of movesList with the shortest distance.
    '''
    moves = []
    minDist = None
    for move in movesList:
        if minDist is None or minDist > move[2]:
            minDist = move[2]
            moves = []
        if move[2] == minDist:
            moves.append(move)
    return np.array(moves)


def higherScoreMoves(movesList, player : PlayerDummy, world : World):
    '''
        Input:
            movesList : np.array of move [penguin, direction, distance]
            player : an instance of Player
            world : an instance of World
        Return a sublist of movesList with the higher score.
    '''
    moves = []
    higherScore = None
    for move in movesList:
        coord = world.makeMove(player.name, move)
        
        if higherScore is None or higherScore < world.pointDistribution[coord[0]][coord[1]]:
            moves = []
            higherScore = world.pointDistribution[coord[0]][coord[1]]
        if higherScore == world.pointDistribution[coord[0]][coord[1]]:
            moves.append(move)
    return np.array(moves)


def lowerScoreMoves(movesList, player : PlayerDummy, world : World):
    '''
        Input:
            movesList : np.array of move [penguin, direction, distance]
            player : an instance of Player
            world : an instance of World
        Return a sublist of movesList with the lower score.
    '''
    moves = []
    lowerScore = None
    for move in movesList:
        coord = world.makeMove(player.name, move)
        
        if lowerScore is None or lowerScore > world.pointDistribution[coord[0]][coord[1]]:
            moves = []
            lowerScore = world.pointDistribution[coord[0]][coord[1]]
        if lowerScore == world.pointDistribution[coord[0]][coord[1]]:
            moves.append(move)
    return np.array(moves)


def squareDist(tile1, tile2):
    '''
        Input : 
            tile1 : coordonnate of a tile [x, y]
            tile2 : coordonnate of a tile [x, y]
        Return the square of the distance between tile1 and tile2 in a world.
    '''
    x1_offset, x2_offset, y1_offset, y2_offset = 0, 0, 0, 0
    if param.column_alignement:
        y1_offset = 0 if tile1[1]%2 == 0 else (np.sqrt(3)/2)
        y2_offset = 0 if tile2[1]%2 == 0 else (np.sqrt(3)/2)
    else:
        x1_offset = 0 if tile1[0]%2 == 0 else (np.sqrt(3)/2)
        x2_offset = 0 if tile2[0]%2 == 0 else (np.sqrt(3)/2)
    factor_x_sqare = 2.25 # 1,5**2
    factor_y_sqare = 3
    return factor_x_sqare*(tile1[0] + x1_offset - tile2[0] - x2_offset)**2 + factor_y_sqare*(tile1[1] + y1_offset - tile2[1] - y2_offset)**2


def closestMoves(movesList, player : PlayerDummy, world : World):
    '''
        Input:
            movesList : np.array of move [penguin, direction, distance]
            player : an instance of Player
            world : an instance of World
        Return a sublist of movesList the closest to another players.
    '''
    moves = []
    minDistFromAnotherPlayer = None
    otherPlayerPosition = world.coordonnate[np.logical_and(world.grid > 0, world.grid != player.name)]
    if len(otherPlayerPosition) == 0:
        return np.array(moves)
    
    for move in movesList:
        coord = world.makeMove(player.name, move)
        
        minDist = None
        for pos in otherPlayerPosition:
            dist = squareDist(coord, pos)
            if minDist is None or minDist > dist:
                minDist = dist

        if minDistFromAnotherPlayer is None or minDistFromAnotherPlayer > minDist:
            moves = []
            minDistFromAnotherPlayer = minDist

        if minDistFromAnotherPlayer == minDist:
            moves.append(move)

    return np.array(moves)


def mostDistantMoves(movesList, player : PlayerDummy, world : World):
    '''
        Input:
            movesList : np.array of move [penguin, direction, distance]
            player : an instance of Player
            world : an instance of World
        Return a sublist of movesList the most distant of the other players.
    '''
    moves = []
    maxDistFromAnotherPlayer = None
    otherPlayerPosition = world.coordonnate[np.logical_and(world.grid > 0, world.grid != player.name)]
    if len(otherPlayerPosition) == 0:
        return np.array(moves)
    
    for move in movesList:
        coord = world.makeMove(player.name, move)

        minDist = None
        for pos in otherPlayerPosition:
            dist = squareDist(coord, pos)
            if minDist is None or minDist > dist:
                minDist = dist

        if maxDistFromAnotherPlayer is None or maxDistFromAnotherPlayer < minDist:
            moves = []
            maxDistFromAnotherPlayer = minDist

        if maxDistFromAnotherPlayer == minDist:
            moves.append(move)

    return np.array(moves)


def connectivity(start, grid):
    '''
        Input:
            start : coordonnate of a valid tile
            grid : a copy of the world grid
        Return a numpy array, tiles that are connected to start.
    '''
    nextCoord = [start]
    width, height = len(grid), len(grid[0])
    connectedPart = np.zeros((width, height), dtype=int)
    while len(nextCoord) > 0: 
        [i, j] = nextCoord.pop()
        if connectedPart[i][j] == 0:
            connectedPart[i][j] = 1
            for direction in range(6):
                coord = World.addDirection([i, j], direction)
                if ( 0 <= coord[0] < width 
                 and 0 <= coord[1] < height 
                 and grid[coord[0]][coord[1]] == 0 ):
                    nextCoord.append(coord)
    return connectedPart

def test_connectivity_true():
    world_txt = '''\
                _  1 1 1 1       1 1 
                _     1   1     1   1 
                _    1     1     1 1 
                _           1     1   
                _1 1 1 1 1 1 1 1 1 1 
                _     1               
                _      1         1   
                _       1 1 1     1   
                _  1   1     1   1 1 
                _   1 1       1 1   1 
                '''
    world = World(param.basicHeight, param.basicWidth, param.basicNbPlayers, param.basicNbPenguinsPerPlayer)
    world.initWorldFromStr(False, dedent(world_txt))
    gridCopy = copy.deepcopy(world.grid)
    start = [4, 0]
    connectedPart = connectivity(start, gridCopy)
    return (np.sum(world.pointDistribution - connectedPart) == 0)

def test_connectivity_false():
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
    world = World(param.basicHeight, param.basicWidth, param.basicNbPlayers, param.basicNbPenguinsPerPlayer)
    world.initWorldFromStr(False, dedent(world_txt))
    gridCopy = copy.deepcopy(world.grid)
    start = [4, 0]
    connectedPart = connectivity(start, gridCopy)
    return (np.sum(world.pointDistribution - connectedPart) != 0)

def keepConnectedMove(movesList, player : PlayerDummy, world : World):
    '''
        Input:
            movesList : np.array of move [penguin, direction, distance]
            player : an instance of Player
            world : an instance of World
        Return a sublist of movesList that keep the connectivity.
    '''
    moves = []
    gridCopy = copy.deepcopy(world.grid)
    connectedPartBefore = np.zeros((world.width, world.height), dtype=int)
    connectedPartAfter = np.zeros((world.width, world.height), dtype=int)

    for move in movesList:
        start = world.penguins[player.name - 1][move[0]]
        gridCopy[start[0]][start[1]] = -1
        connectedPartBefore = connectivity(World.addDirection(start, move[1]), gridCopy)

        coord = world.makeMove(player.name, move)
        gridCopy[coord[0]][coord[1]] = -1
        connectedPartBefore[coord[0]][coord[1]] = 0
        # If it keep the connectivity, the direction doesn't matter. It just need to be valid.
        direction = None
        for dir in range(6):
            [i, j] = World.addDirection(coord, dir)
            if ( 0 <= i < len(gridCopy) 
             and 0 <= j < len(gridCopy[0]) 
             and gridCopy[i][j] == 0 ):
                direction = dir
            if not (direction is None):
                break
        if not (direction is None):
            connectedPartAfter = connectivity(World.addDirection(coord, direction), gridCopy)
    
        if np.sum(connectedPartAfter - connectedPartBefore) == 0:
            moves.append(move)

        # Reset
        gridCopy[start[0]][start[1]] = world.grid[start[0]][start[1]]
        gridCopy[coord[0]][coord[1]] = world.grid[coord[0]][coord[1]]
        connectedPartBefore[connectedPartBefore == 1] = 0
        connectedPartAfter[connectedPartAfter == 1] = 0

    return np.array(moves)

def higherConnectedMove(movesList, player : PlayerDummy, world : World):
    '''
        Input:
            movesList : np.array of move [penguin, direction, distance]
            player : an instance of Player
            world : an instance of World
        Return a sublist of moveList to the connective part with the higher number of point.
    '''
    moves = []
    gridCopy = copy.deepcopy(world.grid)
    connectedParts = []
    possibleDir = []
    doesNotMatter = True
    # list of list of dir where the index is the idPenguin
    bestDirForPenguin = [[] for _ in range(len(world.penguins[player.name - 1]))] 
    for idPenguin, penguin in enumerate(world.penguins[player.name - 1]):
        gridCopy[penguin[0]][penguin[1]] = -1
        for dir in range(6):
            start = World.addDirection(penguin, dir)
            if ( 0 <= start[0] < len(gridCopy) 
             and 0 <= start[1] < len(gridCopy[0]) 
             and gridCopy[start[0]][start[1]] == 0 ):
                possibleDir.append(dir)
                connectedParts.append(connectivity(start, gridCopy))
                
        
        if len(possibleDir) > 0:
            # Find directions with different connected part. At least 1, At most 3.
            distinctConnectedParts = [connectedParts[0]]
            dirTodistinctParts = [[possibleDir[0]]]
            indexPart = 0
            while indexPart < len(distinctConnectedParts):
                j = indexPart + 1
                while j < len(possibleDir):
                    if np.sum(distinctConnectedParts[indexPart] - connectedParts[j]) != 0:
                        distinctConnectedParts.append(connectedParts[j])
                        dirTodistinctParts.append([possibleDir[j]])
                    else:
                        dirTodistinctParts[indexPart].append(possibleDir[j])
                    j += 1
                indexPart += 1
            
            bestIndex = 0
            if len(distinctConnectedParts) > 1: # If more than 1, find the best in score.
                doesNotMatter = False
                maxScore = None
                for index, parts in enumerate(distinctConnectedParts):
                    score = np.sum(world.pointDistribution[parts == 1])
                    if maxScore is None or score > maxScore:
                        maxScore = score
                        bestIndex = index

            for dir in dirTodistinctParts[bestIndex]:
                bestDirForPenguin[idPenguin].append(dir)

        gridCopy[penguin[0]][penguin[1]] = world.grid[penguin[0]][penguin[1]]
        connectedParts = []
        possibleDir = []

    if doesNotMatter:
        return movesList

    else:
        for move in movesList:
            for dir in bestDirForPenguin[move[0]]:
                if dir == move[1]:
                    moves.append(move)
                    break

        return np.array(moves)

if __name__ == "__main__":
    print(test_connectivity_true())
    print(test_connectivity_false())

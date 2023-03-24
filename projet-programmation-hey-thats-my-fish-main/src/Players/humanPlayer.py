from playerDummy import PlayerDummy
from world import World
from Graphics.graphicsPygame import GraphicsPygame

import pygame


class HumanPlayer(PlayerDummy):
    '''
        A player that allow a human to play to the game.
    '''
    def __init__(self):
        super().__init__()
        self.graphics = GraphicsPygame()

    def placePenguin(self, world: World):
        pos = None
        parity = 0
        possibility = world.possiblePenguinPlacement()
        while pos is None:

            for event in pygame.event.get():
                self.graphics.eventManagement(event, world)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mousePosX, mousePosY) = pygame.mouse.get_pos()
                    # Find the closest tile.
                    if world.column_alignement:
                        xCoord = round(mousePosX / (self.graphics.hexagone_size * self.graphics.x_shift) - self.graphics.x_start)
                        yCoord = round(((mousePosY / self.graphics.hexagone_size) - self.graphics.column_shift*(xCoord%2))/self.graphics.y_shift - self.graphics.y_start)
                    else :
                        yCoord = round(mousePosY / (self.graphics.hexagone_size * self.graphics.y_shift) - self.graphics.y_start)
                        xCoord = round(((mousePosX / self.graphics.hexagone_size) - self.graphics.row_shift   *(yCoord%2))/self.graphics.x_shift - self.graphics.x_start)
                    # verify if this tile is a possible position for placing a penguin.
                    if ( 0 <= xCoord < world.height 
                     and 0 <= yCoord < world.width 
                     and world.grid[xCoord][yCoord] == 0 
                     and world.pointDistribution[xCoord][yCoord] <= 1):
                        pos = (xCoord, yCoord)

            hexagrid = pygame.Surface(self.graphics.context.get_size())
            hexagrid = hexagrid.convert()

            self.graphics.drawMap(world, hexagrid)
                    
            for (i,j) in possibility: # Make the tiles where you can put a penguin flash
                x = (i + self.graphics.x_start)*self.graphics.x_shift + self.graphics.row_shift   *(j%2)
                y = (j + self.graphics.y_start)*self.graphics.y_shift + self.graphics.column_shift*(i%2)
                hexagone = [[
                            (x + self.graphics.hexagone_points[k][0])*self.graphics.hexagone_size,
                            (y + self.graphics.hexagone_points[k][1])*self.graphics.hexagone_size
                            ] for k in range(6)]
                pygame.draw.polygon(hexagrid, pygame.Color(255 - 100*parity, 0, 0, 255), hexagone)
            parity = 1 - parity

            self.graphics.context.blit(hexagrid, (0,0))

            self.graphics.writePoints(world)
            self.graphics.writePlayerScores(world) 

            pygame.display.update()
            pygame.time.delay(200)
        return pos
    
    def chooseMove(self, world: World):
        penguinPos = None
        indexPenguin = None
        play = None
        parity = 0
        playable, movesList = world.possibleMove(self.name)
        if not playable:
            return None
        while play is None:

            for event in pygame.event.get():
                self.graphics.eventManagement(event, world)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mousePosX, mousePosY) = pygame.mouse.get_pos()
                    # Find the closest tile.
                    if world.column_alignement:
                        xCoord = round(mousePosX / (self.graphics.hexagone_size * self.graphics.x_shift) - self.graphics.x_start)
                        yCoord = round(((mousePosY / self.graphics.hexagone_size) - self.graphics.column_shift*(xCoord%2))/self.graphics.y_shift - self.graphics.y_start)
                    else :
                        yCoord = round(mousePosY / (self.graphics.hexagone_size * self.graphics.y_shift) - self.graphics.y_start)
                        xCoord = round(((mousePosX / self.graphics.hexagone_size) - self.graphics.row_shift   *(yCoord%2))/self.graphics.x_shift - self.graphics.x_start)
                    # verify if this tile has a penguin of the player.
                    if ( 0 <= xCoord < world.width 
                     and 0 <= yCoord < world.height 
                     and world.grid[xCoord][yCoord] == self.name):
                        penguinPos = (xCoord, yCoord)
                        
                    else:
                        if penguinPos is not None:
                            for index, penguin in enumerate(world.penguins[self.name - 1]):
                                if penguinPos[0] == penguin[0] and penguinPos[1] == penguin[1]:
                                    indexPenguin = index
                            for direction in range(6):
                                distance = 1
                                pos = World.addDirection(penguinPos, direction)
                                while (0 <= pos[0] < world.width 
                                   and 0 <= pos[1] < world.height 
                                   and world.grid[pos[0]][pos[1]] == 0):
                                    if pos[0] == xCoord and pos[1] == yCoord:
                                        play = [indexPenguin, direction, distance]
                                    distance += 1
                                    pos = World.addDirection(pos, direction)
                                    if play is not None:
                                        break
                                if play is not None:
                                    break

            hexagrid = pygame.Surface(self.graphics.context.get_size())
            hexagrid = hexagrid.convert()
            
            self.graphics.drawMap(world, hexagrid)

            for (i,j) in world.penguins[self.name - 1]: # Make the tiles where you can put a pengouin flash
                x = (i + self.graphics.x_start)*self.graphics.x_shift + self.graphics.row_shift   *(j%2)
                y = (j + self.graphics.y_start)*self.graphics.y_shift + self.graphics.column_shift*(i%2)
                pygame.draw.circle(hexagrid, 
                                   self.graphics.colors_pinguins_player[self.name - 1] - pygame.Color(50*parity, 50*parity, 50*parity, 50*parity), 
                                   (x * self.graphics.hexagone_size, y * self.graphics.hexagone_size), 
                                   self.graphics.hexagone_size/2, 
                                   width = 5 )    

            if penguinPos is not None:
                for direction in range(6):
                    distance = 1
                    pos = World.addDirection(penguinPos, direction)
                    while (0 <= pos[0] < world.height 
                        and 0 <= pos[1] < world.width 
                        and world.grid[pos[0]][pos[1]] == 0):
                        x = (pos[0] + self.graphics.x_start)*self.graphics.x_shift + self.graphics.row_shift   *(pos[1]%2)
                        y = (pos[1] + self.graphics.y_start)*self.graphics.y_shift + self.graphics.column_shift*(pos[0]%2)
                        hexagone = [[
                                    (x + self.graphics.hexagone_points[k][0])*self.graphics.hexagone_size,
                                    (y + self.graphics.hexagone_points[k][1])*self.graphics.hexagone_size
                                    ] for k in range(6)]
                        pygame.draw.polygon(hexagrid, pygame.Color(255 - 100*parity, 0, 0, 255), hexagone)
                        distance += 1
                        pos = World.addDirection(pos, direction)

            parity = 1 - parity

            self.graphics.context.blit(hexagrid, (0,0))
            
            self.graphics.writePoints(world)
            self.graphics.writePlayerScores(world) 

            pygame.display.update()
            pygame.time.delay(200)
        return play    

from Graphics.graphicsPygame import GraphicsPygame
from world import World

import gameParameters as param
import pygame

class MapMaker:

    max_rows = param.max_rows
    max_columns = param.max_columns

    def __init__(self):
        self.graphics = GraphicsPygame()
        self.world = World(self.max_rows, self.max_columns, 1, 1)

    def make(self):
        while self.graphics.display:
            for event in pygame.event.get():
                self.graphics.eventManagement(event, self.world)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # mouse left click
                    (mousePosX, mousePosY) = pygame.mouse.get_pos()
                    # Find the closest tile.
                    if self.world.column_alignement:
                        xCoord = round(mousePosX / (self.graphics.hexagone_size * self.graphics.x_shift) - self.graphics.x_start)
                        yCoord = round(((mousePosY / self.graphics.hexagone_size) - self.graphics.column_shift*(xCoord%2))/self.graphics.y_shift - self.graphics.y_start)
                    else :
                        yCoord = round(mousePosY / (self.graphics.hexagone_size * self.graphics.y_shift) - self.graphics.y_start)
                        xCoord = round(((mousePosX / self.graphics.hexagone_size) - self.graphics.row_shift   *(yCoord%2))/self.graphics.x_shift - self.graphics.x_start)
                    # verify if this tile is a possible position for placing a tile.
                    if ( 0 <= xCoord < self.world.width 
                        and 0 <= yCoord < self.world.height ):
                        self.world.grid[xCoord][yCoord] = -1 - self.world.grid[xCoord][yCoord]
                        self.world.pointDistribution[xCoord][yCoord] = 1 + self.world.grid[xCoord][yCoord]

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # mouse right click
                    (mousePosX, mousePosY) = pygame.mouse.get_pos()
                    # Find the closest tile.
                    if self.world.column_alignement:
                        xCoord = round(mousePosX / (self.graphics.hexagone_size * self.graphics.x_shift) - self.graphics.x_start)
                        yCoord = round(((mousePosY / self.graphics.hexagone_size) - self.graphics.column_shift*(xCoord%2))/self.graphics.y_shift - self.graphics.y_start)
                    else :
                        yCoord = round(mousePosY / (self.graphics.hexagone_size * self.graphics.y_shift) - self.graphics.y_start)
                        xCoord = round(((mousePosX / self.graphics.hexagone_size) - self.graphics.row_shift   *(yCoord%2))/self.graphics.x_shift - self.graphics.x_start)
                    # verify if this tile is a possible position for placing a tile.
                    if ( 0 <= xCoord < self.world.width 
                        and 0 <= yCoord < self.world.height 
                        and self.world.grid[xCoord][yCoord] >= 0):
                        self.world.pointDistribution[xCoord][yCoord] = (self.world.pointDistribution[xCoord][yCoord] + 1) % 4 
                        if self.world.pointDistribution[xCoord][yCoord] == 0:
                            self.world.pointDistribution[xCoord][yCoord] += 1
            
            hexagrid = pygame.Surface(self.graphics.context.get_size())
            hexagrid = hexagrid.convert()

            self.graphics.drawMap(self.world, hexagrid)
            self.graphics.drawEdges(hexagrid)
            self.graphics.writePoints(self.world)
            pygame.display.update()

if __name__ == "__main__":
    map = MapMaker()
    map.make()
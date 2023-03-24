from graphicsDummy import GraphicsDummy
from world import World

import pygame
import numpy as np
import gameParameters as param

class GraphicsPygame(GraphicsDummy):
    display = True

    board_height = 500
    board_width = 600

    max_rows = param.max_rows
    max_columns = param.max_columns

    # Radius
    hexaSizeDefiner = lambda board_height, board_width, max_rows, max_columns : min(board_height/(2*max_rows + 1), board_width/(2*max_columns))
    hexagone_size = hexaSizeDefiner(board_height, board_width, max_rows, max_columns)

    epsilon_shift = 0.1 # space between tiles.
    column_alignement = World.column_alignement
    if column_alignement:
        # coordonnate of an hexagone in a circle centered at (0,0) of a radius of 1.
        hexagone_points = [[np.cos(i*np.pi/3), np.sin(i*np.pi/3)] for i in range(6)]
        x_shift = 1.5 + epsilon_shift
        row_shift = 0
        y_shift = np.sqrt(3) + epsilon_shift
        column_shift = y_shift/2
    else:
        # coordonnate of an hexagone in a circle centered at (0,0) of a radius of 1.
        hexagone_points = [[np.sin(i*np.pi/3), np.cos(i*np.pi/3)] for i in range(6)]
        x_shift = np.sqrt(3) + epsilon_shift
        row_shift = x_shift/2 
        y_shift = 1.5 + epsilon_shift
        column_shift = 0

    starting_pos = lambda screen_size, max_hexagone, hexagone_size: 1 #0.5*(screen_size/hexagone_size - max_hexagone)
    x_start = starting_pos(board_width , max_columns*x_shift + row_shift   , hexagone_size)
    y_start = starting_pos(board_height, max_rows   *y_shift + column_shift, hexagone_size)


    colors_pinguins_player = [
                                pygame.Color(250,000,000,255),  #red
                                pygame.Color(000,000,250,255),  #blue
                                pygame.Color(000,250,000,255),  #green
                                pygame.Color(250,250,000,255)   #yellow
                             ]
    ice_color = pygame.Color(0, 200, 255, 255) # cyan
    water_color = pygame.Color(0, 100, 255, 255) # dark_blue

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.board_width, self.board_height), pygame.RESIZABLE)
        pygame.display.set_caption("Hey, that's my fish!")
        self.context = pygame.display.get_surface()
        self.police = pygame.font.SysFont("monospace", 20)
        self.clock = pygame.time.Clock()

    def displayResize(self, height, width):
        GraphicsPygame.board_height = height
        GraphicsPygame.board_width = width
        GraphicsPygame.hexagone_size = self.__class__.hexaSizeDefiner(self.board_height, self.board_width, self.max_rows, self.max_columns)

        GraphicsPygame.x_start = self.__class__.starting_pos(self.board_width , (self.max_columns*self.x_shift + self.row_shift   ), self.hexagone_size)
        GraphicsPygame.y_start = self.__class__.starting_pos(self.board_height, (self.max_rows   *self.y_shift + self.column_shift), self.hexagone_size)
        
        GraphicsPygame.screen = pygame.display.set_mode((self.board_width, self.board_height), pygame.RESIZABLE)

    def updateRepresentation(self, column_alignement):
        if column_alignement != self.column_alignement:
            self.column_alignement = column_alignement
            self.hexagone_points = [[self.hexagone_points[i][1], self.hexagone_points[i][0]] for i in range(6)]
            self.x_shift, self.y_shift = self.y_shift, self.x_shift
            self.row_shift, self.column_shift = self.column_shift, self.row_shift

    def drawEdges(self, pySurface):
        self.updateRepresentation(World.column_alignement)
        for i in range(self.max_rows):
            for j in range(self.max_columns):
                x = (i + self.x_start)*self.x_shift + self.row_shift   *(j%2)
                y = (j + self.y_start)*self.y_shift + self.column_shift*(i%2)
                hexagone = [[
                                (x + self.hexagone_points[k][0])*self.hexagone_size,
                                (y + self.hexagone_points[k][1])*self.hexagone_size
                            ] for k in range(6)]
                pygame.draw.polygon(pySurface, pygame.Color(240, 240, 240, 255), hexagone, width = 6 )
        self.context.blit(pySurface, (0, 0))

    def drawMap(self, world : World, pySurface):
        self.updateRepresentation(world.column_alignement)
        pySurface.fill(self.water_color)
        for i, column in enumerate(world.grid):
            for j, tiles in enumerate(column):
                if tiles >= 0: # Draw the tiles
                    x = (i + self.x_start)*self.x_shift + self.row_shift   *(j%2)
                    y = (j + self.y_start)*self.y_shift + self.column_shift*(i%2)
                    hexagone = [[
                                 (x + self.hexagone_points[k][0])*self.hexagone_size,
                                 (y + self.hexagone_points[k][1])*self.hexagone_size
                                ] for k in range(6)]
                    pygame.draw.polygon(pySurface, self.ice_color, hexagone)

                    if tiles > 0: # Draw the penguin on the tiles.
                        pygame.draw.circle(pySurface, 
                                           self.colors_pinguins_player[tiles-1], 
                                           (x * self.hexagone_size, y * self.hexagone_size), 
                                           self.hexagone_size/2, 
                                           width = 5 )
        self.context.blit(pySurface, (0, 0))

    def writePoints(self, world : World):
        self.updateRepresentation(world.column_alignement)
        for i, column in enumerate(world.grid):
            for j, tiles in enumerate(column):
                if tiles >= 0:
                    x = ((i + self.x_start)*self.x_shift - 0.16 + self.row_shift   *(j%2))*self.hexagone_size
                    y = ((j + self.y_start)*self.y_shift - 0.28 + self.column_shift*(i%2))*self.hexagone_size
                    text = self.police.render(f"{world.pointDistribution[i,j]}", 1, (0,0,0))
                    self.context.blit(text, (x,y))

    def writePlayerScores(self, world : World):
        for player, score in enumerate(world.points):
            text = self.police.render(f"Player {player + 1}: {score}", 1, self.colors_pinguins_player[player])
            self.context.blit(text, (.65*self.board_width*(player%2), 0.95*self.board_height*(player//2)))
    
    def eventManagement(self, event, world):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
            self.quit()
        
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_p):
            world.print()

        if event.type == pygame.VIDEORESIZE:
            self.displayResize(event.h, event.w)

    def showWorld(self, world : World):
        for event in pygame.event.get():
            self.eventManagement(event, world)
        
        hexagrid = pygame.Surface(self.context.get_size())
        hexagrid = hexagrid.convert()
        self.drawMap(world, hexagrid)
        self.writePoints(world)
        self.writePlayerScores(world)
        
        pygame.display.update()
        pygame.time.delay(250)
    
    def endDisplay(self):
        self.display = False
        pygame.display.quit()
        pygame.quit()

    def quit(self):
        self.endDisplay()
        exit()
        
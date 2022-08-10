import pygame
import random
import time
import copy
import CONST
import sys

pygame.init()

figures = {
    
    "Twist": {
        "width": CONST.tile_size * 3,
        "widthTurned": CONST.tile_size * 2,
        "height": CONST.tile_size * 2,
        "heightTurned": CONST.tile_size * 3,
        "color": {
            "right": CONST.blue,
            "left": CONST.yellow
            },
},
    "Square": {
        "width": CONST.tile_size * 2,
        "color": CONST.red,
},
    "Log": {
        "width": CONST.tile_size,
        "widthTurned": CONST.tile_size * 4,
        "height": CONST.tile_size * 4,
        "heightTurned": CONST.tile_size,
        "color": CONST.purple,
}
}

turns = ["right", "down", "left", "up"]

y_top = 182

screen = pygame.display.set_mode(CONST.screen_size)

#calculations functions
#should be calculated for each object separately, taking into account width of the object

def drawCoordinatesSystem(YforY=182, XforX=100):

    #commented out are x,y values on the grid
    while YforY <= CONST.y_bottom:
        #Ycoord = CONST.basicFont.render(str(YforY), True, CONST.white)
        #YcoordRect = pygame.Rect(XforY, YforY, CONST.tile_size, CONST.tile_size)
        #screen.blit(Ycoord, YcoordRect)
        pygame.draw.line(screen, CONST.white, (XforX, YforY), (CONST.end, YforY))
        YforY += CONST.tile_size

    XforX=100
    YforY=182
        
    while XforX <= CONST.end:
        #Xcoord = CONST.basicFont.render(str(XforX), True, CONST.white)
        #XcoordRect = pygame.Rect(XforX, YforX, CONST.tile_size, CONST.tile_size)
        #screen.blit(Xcoord, XcoordRect)
        pygame.draw.line(screen, CONST.white, (XforX, YforY), (XforX, CONST.y_bottom))
        XforX += CONST.tile_size

def possible_x_ccordinates(start, end, tile_size):

    x_coordinates = []

    while start <= end:

        x_coordinates.append(start)
        start += tile_size

    return x_coordinates
    

#object related functions
def create_new_object():

    figure = random.choice(list(figures.keys()))

    if figure == "Square":
        figureWidth = figures[figure]["width"]
        x_coordinates = possible_x_ccordinates(CONST.start, CONST.end - figureWidth, CONST.tile_size)
        x_origin = random.choice(x_coordinates)
        newObject = Square(x_origin, y_top - CONST.tile_size)
        
    elif figure == "Twist":
        side = random.choice(("right", "left"))
        turnedFlag = random.choice([True, False])
        if turnedFlag:
            figureWidth = figures[figure]["widthTurned"]
            figureHeight = figures[figure]["heightTurned"]
        else:
            figureWidth = figures[figure]["width"]
            figureHeight = figures[figure]["height"]
            
        x_coordinates = possible_x_ccordinates(CONST.start, CONST.end - figureWidth, CONST.tile_size)
        x_origin = random.choice(x_coordinates)
        newObject = Twist(x_origin, y_top - figureHeight + CONST.tile_size, side, turnedFlag)
            
    elif figure == "Log":

        turn = random.choice(["right", "up"])
        if turn == "right":
            figureWidth = figures[figure]["widthTurned"]
            y_start = y_top - CONST.tile_size * 3
        else:
            figureWidth = figures[figure]["width"]
            y_start = y_top - CONST.tile_size * 3
        
        x_coordinates = possible_x_ccordinates(CONST.start, CONST.end - figureWidth, CONST.tile_size)
        x_origin = random.choice(x_coordinates)
        newObject = Log(x_origin, y_start, turn)

        
    return newObject
    
def moveObject(object):

    object.present()
    pygame.display.flip()
    object.delete()
      
    
# classes
class Matrix:

    def __init__(self):
    
        self.matrix = {}
        i = CONST.start
        j = y_top
        
        while i < CONST.end:
            while j < CONST.y_bottom:
                coord = (i,j)
                self.matrix[coord] = (False, None)
                j += CONST.tile_size
            i += CONST.tile_size
            j = y_top
                
        #start of playground (100, 182)
                
    def update_matrix(self, object):
        
        for i in object.array:
            self.matrix[i] = (True, object.color)
    
    def present(self, line=[], color=None, showInTerminal=False):
        
        for j in range(y_top, CONST.y_bottom, CONST.tile_size):
            for i in range(CONST.start, CONST.end, CONST.tile_size):
                tileTaken, tileColor = self.matrix[(i,j)]
                if tileTaken:
                    matrixRect = pygame.Rect(i, j, CONST.tile_size, CONST.tile_size)
                    pygame.draw.rect(screen, tileColor, matrixRect)
                    pygame.draw.rect(screen, CONST.white, matrixRect, 1)
                    if (i, j) in line:
                        matrixRect = pygame.Rect(i, j, CONST.tile_size, CONST.tile_size)
                        pygame.draw.rect(screen, color, matrixRect)
                        pygame.draw.rect(screen, CONST.white, matrixRect, 1)
        
        #supporting part to show matrix in terminal and check if it's ok.
        if showInTerminal:
            for j in range(y_top, CONST.y_bottom, CONST.tile_size):
                for i in range(CONST.start, CONST.end, CONST.tile_size):

                    if self.matrix[(i, j)][0]:
                        print("#", end="")
                    else:
                        print("O", end="")
                print()
                        
                    
    def gameOver(self):
    
        for i in range(CONST.start, CONST.end, CONST.tile_size):
            if self.matrix[(i, y_top)][0]:
                return True
                
        return False
        
    def checkForLinesToDelete(self):
    
        checkedLines = []
        limit = (CONST.pg_width - 2 * CONST.frame_edge) / CONST.tile_size #8
        lineUnderChecking = []
        
        #finding lines to be deleted (their coordinates)
        for j in range(y_top, CONST.y_bottom, CONST.tile_size):
            for i in range(CONST.start, CONST.end, CONST.tile_size):
                tileTaken = self.matrix[(i,j)][0]
                if tileTaken:
                    lineUnderChecking.append((i,j))
                    
            if len(lineUnderChecking) == limit:
                checkedLines.append(lineUnderChecking)
            lineUnderChecking = []
        
        return checkedLines
        
    def deleteLine(self, line):
    
            i,j = line[0]
            
            matrix_copy = copy.deepcopy(self.matrix)
                
            #1) replacing the top line with False values (emptying top layer)
            for l in range(CONST.start, CONST.end, CONST.tile_size):
                matrix_copy[(l, y_top)] = (False, None)
                
            #2) copying all lines above deleted line from matrix into matrix_copy with a shift of tile_size down
            for k in range(y_top, j, CONST.tile_size):
                for m in range(CONST.start, CONST.end, CONST.tile_size):
                    matrix_copy[(m, k + CONST.tile_size)] = self.matrix[(m, k)]
            
            #2.1) unpresent old version of matrix on the screen
            for j in range(y_top, CONST.y_bottom, CONST.tile_size):
                for i in range(CONST.start, CONST.end, CONST.tile_size):
                    if self.matrix[(i,j)]:
                        matrixRect = pygame.Rect(i, j, CONST.tile_size, CONST.tile_size)
                        pygame.draw.rect(screen, CONST.black, matrixRect)
               
            #3) store the result in initial matrix
            self.matrix = matrix_copy
                
class Square:

    def __init__(self, x_origin, y_origin):

        self.name = "Square"
        self.color = figures[self.name]["color"]
        self.width = figures[self.name]["width"]
        self.x_coordinate = x_origin
        self.y_coordinate = y_origin
        
        
    @property
    def array(self):
        return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size)]
        
    @property
    def bottomCoords(self):
        return [(self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size)]
        
    @property
    def rightCoords(self):
        return [(self.x_coordinate + CONST.tile_size, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size)]
    
    @property
    def leftCoords(self):
        return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size)]
    
    def delete(self):
        
        for x,y in self.array:
            if y >= y_top:
                rect = pygame.Rect(x, y, CONST.tile_size, CONST.tile_size)
                pygame.draw.rect(screen, CONST.black, rect)
                pygame.draw.line(screen, CONST.white, (x, y), (x + CONST.tile_size, y))
                pygame.draw.line(screen, CONST.white, (x, y), (x, y + CONST.tile_size))
                pygame.draw.line(screen, CONST.white, (x + CONST.tile_size, y), (x + CONST.tile_size, y + CONST.tile_size))
                pygame.draw.line(screen, CONST.white, (x, y + CONST.tile_size), (x + CONST.tile_size, y + CONST.tile_size))
        
    def present(self):

        for x,y in self.array:
            if y >= y_top:
                rect = pygame.Rect(x, y, CONST.tile_size, CONST.tile_size)
                pygame.draw.rect(screen, self.color, rect)
                pygame.draw.rect(screen, CONST.white, rect, 1)
            
    def reachedBottom(self, matrix):
        
        for i in self.bottomCoords:
            x,y = i
            y += CONST.tile_size
            try:
                if y == CONST.y_bottom or matrix.matrix[(x, y)][0] == True:
                    return True
            except KeyError:
                return True

        return False
        
    def crossedBottom(self, matrix):
        
        for x,y in self.bottomCoords:
            try:
                if y == CONST.y_bottom - CONST.tile_size or matrix.matrix[(x,y)][0] == True:
                    return True
            except KeyError:
                return True
        return False

    def crossedRightLimit(self, matrix):
    
        for x,y in self.rightCoords:
            try:
                if x == CONST.end or matrix.matrix[(x,y)][0] == True:
                    return True
            except KeyError:
                return True
        return False
        
    def crossedLeftLimit(self, matrix):
        
        for x,y in self.leftCoords:
            try:
                if x == CONST.start - CONST.tile_size or matrix.matrix[(x,y)][0] == True:
                    return True
            except KeyError:
                return True
        return False

        
class Twist(Square):

    def __init__(self, x_origin, y_origin, side, turnedFlag):
    
        self.name = "Twist"
        self.side = side #either left or right
        self.turned = turnedFlag
        if self.side == "right":
            self.color = figures["Twist"]["color"]["right"]
        else:
            self.color = figures["Twist"]["color"]["left"]

        self.x_coordinate = x_origin
        self.y_coordinate = y_origin
        
    @property
    def array(self):
        if self.side == "right":
        
            if not self.turned:
                #rightSide
                return [(self.x_coordinate + CONST.tile_size, self.y_coordinate), (self.x_coordinate + CONST.tile_size * 2, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size)]
            else:
                #rightSideTurned
                return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size * 2)]
        else:
            if not self.turned:
                #leftSide
                return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size * 2, self.y_coordinate + CONST.tile_size)]
            else:
                #leftSide turned
                return [(self.x_coordinate + CONST.tile_size, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size), (self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 2)]
        
    @property
    def bottomCoords(self):
    
        if self.side == "right":
            if not self.turned:
                #rightSide botttom
                return [(self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size * 2, self.y_coordinate)]
                
            else:
                #rightSide bottom turned
                return [(self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size * 2)]
        else:
            if not self.turned:
                #leftSide bottom
                return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size * 2, self.y_coordinate + CONST.tile_size)]
            else:
                #leftSide borrom turned
                return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 2), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size)]
        
    @property
    def rightCoords(self):
    
        if self.side == "right":
            if not self.turned:
                #rightSide original
                return [(self.x_coordinate + CONST.tile_size * 2, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size)]
            else:
                #rightSide turned
                return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size * 2)]
        else:
            if not self.turned:
                #leftSide original
                return [(self.x_coordinate + CONST.tile_size, self.y_coordinate), (self.x_coordinate + CONST.tile_size * 2, self.y_coordinate + CONST.tile_size)]
            else:
                #leftSide turned
                return [(self.x_coordinate + CONST.tile_size, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 2)]
    
    @property
    def leftCoords(self):
    
        if self.side == "right":
            if not self.turned:
                #rightSide original
                return [(self.x_coordinate + CONST.tile_size, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size)]
                
            else:
                #rightSide turned
                return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size * 2)]
        
        else:
            if not self.turned:
                #leftSide original
                return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size)]
                
            else:
                #leftSide turned
                return [(self.x_coordinate + CONST.tile_size, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 2)]
        
class Log(Square):

    #every time a key dwon is hit log turns clockwise
    
    def __init__(self, x_origin, y_origin, turn):
        
        self.name = "Log"
        self.turn = turn
        self.color = figures[self.name]["color"]
        self.x_coordinate = x_origin
        self.y_coordinate = y_origin
        
    @property
    def array(self):

        if self.turn == "up":
            return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 2), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 3)]
            
        elif self.turn == "right":
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate + CONST.tile_size * 2, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate + CONST.tile_size * 3, self.y_coordinate + CONST.tile_size * 3)]
            
        elif self.turn == "down":
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 4), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 5), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 6)]
        
        elif self.turn == "left":
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate - CONST.tile_size, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate - CONST.tile_size * 2, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate - CONST.tile_size * 3, self.y_coordinate + CONST.tile_size * 3)]
    
        
    @property
    def bottomCoords(self):
        if self.turn == "up":
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 3)]
            
        elif self.turn == "right":
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate + CONST.tile_size, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate + CONST.tile_size * 2, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate + CONST.tile_size * 3, self.y_coordinate + CONST.tile_size * 3)]
            
        elif self.turn == "left":
            return [(self.x_coordinate - CONST.tile_size * 3, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate - CONST.tile_size * 2, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate - CONST.tile_size, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 3)]
        
        #down
        else:
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 6)]
            
    
    @property
    def rightCoords(self):
        if self.turn == "up":
            return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 2), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 3)]
            
        elif self.turn == "right":
            return [(self.x_coordinate + CONST.tile_size * 3, self.y_coordinate + CONST.tile_size * 3)]
            
        elif self.turn == "left":
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 3)]
            
        else:
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 4), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 5), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 6)]
        
    @property
    def leftCoords(self):
        if self.turn == "up":
            return [(self.x_coordinate, self.y_coordinate), (self.x_coordinate, self.y_coordinate + CONST.tile_size), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 2), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 3)]
        elif self.turn == "down":
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 3), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 4), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 5), (self.x_coordinate, self.y_coordinate + CONST.tile_size * 6)]
        elif self.turn == "right":
            return [(self.x_coordinate, self.y_coordinate + CONST.tile_size * 3)]
        else:
            return [(self.x_coordinate - CONST.tile_size * 3, self.y_coordinate + CONST.tile_size * 3)]
        

class Button:
        
    def __init__(self, x, y, width, height):
        self.pauseFont = pygame.font.Font("OpenSans-Regular.ttf", 12)
        self.pauseTitle = self.pauseFont.render("  PAUSE", True, CONST.white)
        self.buttonRect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, CONST.white, self.buttonRect, 1)
        screen.blit(self.pauseTitle, self.buttonRect)
        self.clickCount = 0
            
    def clicked(self):
    
        if self.clickCount % 2 == 1:
            self.pauseTitle = self.pauseFont.render("RESUME", True, CONST.black)
            screen.blit(self.pauseTitle, self.buttonRect)
            self.pauseTitle = self.pauseFont.render("  PAUSE", True, CONST.white)
            screen.blit(self.pauseTitle, self.buttonRect)
            
        else:
            self.pauseTitle = self.pauseFont.render("  PAUSE", True, CONST.black) #wipe out PAUSE
            screen.blit(self.pauseTitle, self.buttonRect)
            self.pauseTitle = self.pauseFont.render("RESUME", True, CONST.white) #draw RESUME
            screen.blit(self.pauseTitle, self.buttonRect)
        self.clickCount += 1
            
    def checkForClick(self):
    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if self.buttonRect.collidepoint(mouse):
                    return True
            elif event.type == pygame.QUIT:
                sys.exit()
            
        return False


    
        




import pygame
import time
import sys
import random
import util
import CONST
from pygame import mixer

pygame.init() #also initializes font module

screen = pygame.display.set_mode(CONST.screen_size)

matrix = util.Matrix()
clock = pygame.time.Clock()
pauseButton = util.Button(320, 70, 50, 30)

newObjectCreated = False
gameOver = False
reachedBottom = False
turnedFlag = False
turnIsPossible = False

mixer.music.load('tetris_bg.mp3') #background music
mixer.music.play(-1)

#we use the while-loop because it's important to keep the screen up while game is in process
while True:

    #take event from the queue to see the screen
    #there is a queue of events even before the program starts
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
        
            #create a temp object to check its turned/shifted coords on the screen and if everything fits, store them into an actual object
            if newObject.name == "Square":
                tempObject = util.Square(newObject.x_coordinate, newObject.y_coordinate)
            elif newObject.name == "Twist":
                tempObject = util.Twist(newObject.x_coordinate, newObject.y_coordinate, newObject.side, newObject.turned)
            elif newObject.name == "Log":
                tempObject = util.Log(newObject.x_coordinate, newObject.y_coordinate, newObject.turn)
        
            if event.key == pygame.K_RIGHT:
                  
            #the task is to take a shifted (temp) object and check if it hits the right wall
               tempObject.x_coordinate += CONST.tile_size
               if not tempObject.crossedRightLimit(matrix):
                   newObject.x_coordinate = tempObject.x_coordinate
                   util.moveObject(newObject)

            elif event.key == pygame.K_LEFT:
            
                tempObject.x_coordinate -= CONST.tile_size
                if not tempObject.crossedLeftLimit(matrix):
                    newObject.x_coordinate = tempObject.x_coordinate
                    util.moveObject(newObject)
                    
            elif event.key == pygame.K_DOWN:
                
                tempObject.y_coordinate += CONST.tile_size
                if not tempObject.crossedBottom(matrix):
                    newObject.y_coordinate = tempObject.y_coordinate
                    util.moveObject(newObject)
                    
            elif event.key == pygame.K_UP:
                
                if newObject.name == "Twist":
                
                #check if current object is currently turned. If so, make it straight again. If not, turn
                    
                    if newObject.turned:
                        tempObject.turned = False
                    else:
                        tempObject.turned = True
                        
                elif newObject.name == "Log":
                    
                    currentPos = util.turns.index(newObject.turn)
                    
                    try:
                        nextPos = util.turns[currentPos + 1]
                    except IndexError:
                        nextPos = util.turns[0]
                    
                    tempObject.turn = nextPos
                    
            if not tempObject.crossedBottom(matrix) and not tempObject.crossedRightLimit(matrix) and not tempObject.crossedLeftLimit(matrix):
            
                newObject = tempObject
                util.moveObject(newObject)
                    
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if pauseButton.buttonRect.collidepoint(mouse):
                mixer.music.pause()
                pauseButton.clicked()
                util.moveObject(newObject)
                while not pauseButton.checkForClick():
                    time.sleep(0.2)
                mixer.music.unpause()
                pauseButton.clicked()
                pygame.display.flip()
                    
    #start of the actual game flow
    if not gameOver:
        
        #set up basic screen
        title = CONST.tetrisFont.render("TETRIS", True, CONST.white)
        titleRect = title.get_rect()
        titleRect.center = ((CONST.width / 2), (CONST.title_height / 2))
        screen.blit(title, titleRect)
        playgroundRect = pygame.Rect(CONST.pg_x, CONST.pg_y, CONST.pg_width, CONST.pg_height)
        pygame.draw.rect(screen, CONST.white, playgroundRect, CONST.frame_edge) #edging line is inside of the rect
        util.drawCoordinatesSystem()
        
        #create a new tetris object
        if newObjectCreated is False:
            newObject = util.create_new_object()
            newObject.present()
            newObjectCreated = True
            
        else:
        
            # when object either hits the ground or true cell in matrix:
            #1) matrix is updated
            #2) matrix is checked if any lines should be deleted
            #3) lines to be deleted are marked in green, presented and deleted
            #4) matrix is updated and presented
            #5) new object is created
        
            #object hits the ground/other objects in matrix
            count = 1
            if newObject.reachedBottom(matrix):
            
                #make a sound effect
                reachedBottomSound = mixer.Sound('fall.wav')
                reachedBottomSound.play()
                
                #update matrix
                matrix.update_matrix(newObject)
                matrix.present()
            
                while True:
                    
                    #check for lines to be deleted. If no lines, present matrix and create another object
                    linesToDelete = matrix.checkForLinesToDelete()
    
                    if not linesToDelete:
                        break
                    
                    #making a single list out of nested list for present func
                    listOfCoordinatesToDelete = []
                    for line in linesToDelete:
                        listOfCoordinatesToDelete += line
      
                    #first state - show matrix with green lines
                    matrix.present(line=listOfCoordinatesToDelete, color=CONST.green)
                    time.sleep(0.2)
                    deleteLineSound = mixer.Sound('delete_line.wav')
                    deleteLineSound.play()
                    pygame.display.flip()
                    #second state - show matrix with black lines
                    matrix.present(line=listOfCoordinatesToDelete, color=CONST.black)
                    time.sleep(0.2)
                    pygame.display.flip()
                    #third states - show matrix update
                    for line in linesToDelete:
                        matrix.deleteLine(line)
                        matrix.present()
                    count += 1
                        
                newObjectCreated = False
                    
                #check if the game is over
                gameOver = matrix.gameOver()
                if gameOver:
                    mixer.music.stop()
                    gameOverSound = mixer.Sound('game_over.wav')
                    gameOverSound.play()
            
            #tile falling down on the ground
            else:
                newObject.y_coordinate += CONST.tile_size
                newObject.present()
                
        matrix.present()
        pygame.display.flip()
        
        if reachedBottom is False:
            time.sleep(0.3)
        newObject.delete()
        
    else:
        
        screen.fill((0,0,0))
        title = CONST.tetrisFont.render("GAME OVER", True, CONST.white)
        titleRect = title.get_rect()
        titleRect.center = ((CONST.width / 2), (CONST.title_height / 2))
        screen.blit(title, titleRect)
        pygame.display.flip()





    

    

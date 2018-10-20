# PONG: an experiment in terrible motion controls
# By: Jarod Honas and Reece Berens
# Created: 10/19/2018
# HACK K-State Project

import random, pygame, sys
#Maybe -> from pygame.locals import *

FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

# STANDARD COLORS
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

#Set Buttons
#SELECT = something
#GOBACK = something
#MOTION READOUTS

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('PONG')

    showStartScreen()
    while True:
        runGame()

def runGame():
    #Set Positions
    

    #Draw onto SURF
    DISPLAYSURF.fill(BGCOLOR)
    drawPaddles()
    drawBall()


def terminate():
    pygame.quit()
    sys.exit()

def drawPaddles():
    #PaddleLeft
	paddleLeft = pygame.Rect(0,0, 50, 150)
	pygame.draw.rect(DISPLAYSURF, WHITE, paddleLeft)
	#PaddleRight
	paddleRight = pygame.Rect(500,500, 50, 150)
	pygame.draw.rect(DISPLAYSURF, WHITE, paddleRight)

def drawBall():
	pygame.draw.circle(DISPLAYSURF, WHITE,(0,0), 50)

def showStartScreen():
	pass
	while True:
		val = 1
		#wait till confirmation



# PONG: an experiment in terrible motion controls
# By: Jarod Honas and Reece Berens
# Created: 10/19/2018
# HACK K-State Project

import random, pygame, sys
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
PADDLEWIDTH = 50
PADDLEHEIGHT = 150
leftPaddleX = 0
leftPaddleY = 0
rightPaddleX = WINDOWWIDTH-PADDLEWIDTH
rightPaddleY = 0

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
    #showStartScreen()
    while True:
        runGame()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
		
def runGame():
	#Set Positions
	#Draw onto SURF
	DISPLAYSURF.fill(BGCOLOR)
	drawPaddles()
	drawBall()
	pygame.display.update()
	FPSCLOCK.tick(FPS)
"""
def terminate():
    pygame.quit()
    sys.exit()
"""
def drawPaddles():
    #PaddleLeft
	paddleLeft = pygame.Rect(leftPaddleX,leftPaddleY, PADDLEWIDTH, PADDLEHEIGHT)
	pygame.draw.rect(DISPLAYSURF, WHITE, paddleLeft)
	#PaddleRight
	paddleRight = pygame.Rect(rightPaddleX,rightPaddleY, PADDLEWIDTH, PADDLEHEIGHT)
	pygame.draw.rect(DISPLAYSURF, WHITE, paddleRight)

def drawBall():
	pygame.draw.circle(DISPLAYSURF, WHITE,(200,200), 50)

def showStartScreen():
	pass
	while True:
		val = 1
		#wait till confirmation

if __name__ == '__main__':
    main()



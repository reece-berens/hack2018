# PONG: an experiment in terrible motion controls
# By: Jarod Honas and Reece Berens
# Created: 10/19/2018
# HACK K-State Project

import random, pygame, sys
from pygame.locals import *
from hardware import *
import RPi.GPIO as GPIO
from multiprocessing import Process, Value

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()
FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
PADDLEWIDTH = 50
PADDLEHEIGHT = 150
leftPaddleX = 0
leftPaddleY = 0
leftPaddleYApproach = 0
rightPaddleX = WINDOWWIDTH-PADDLEWIDTH
rightPaddleY = 0
rightPaddleYApproach = 0
ballX = 200
ballY = 200
ballRadius = 25
xVel = 2
yVel = 2
rightPoints = 0
leftPoints = 0

leftSensor = DistanceSensor("left", 13, 11)
rightSensor = DistanceSensor("right", 37, 38)



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
    global senLeft, senRight, leftPaddleY, rightPaddleY, rightPaddleYApproach, leftPaddleYApproach
    #Set Positions
    #getPaddlePosistions()
    updateBall()
    if(senLeft.value <= 480 and senLeft.value >= 0):
        leftPaddleYApproach = senLeft.value
    if(senRight.value <= 480 and senRight.value >= 0):
        rightPaddleYApproach = senRight.value
    approachSpeed = 6
    if(leftPaddleY-leftPaddleYApproach > 1):
        leftPaddleY -= approachSpeed
    if(leftPaddleY-leftPaddleYApproach < 1):
        leftPaddleY += approachSpeed
    if(rightPaddleY-rightPaddleYApproach > 1):
        rightPaddleY -= approachSpeed
    if(rightPaddleY-rightPaddleYApproach < 1):
        rightPaddleY += approachSpeed 
    #Draw onto SURF
    DISPLAYSURF.fill(BGCOLOR)
    drawPaddles()
    drawBall()
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def updateBall():
    global ballX, ballY, yVel, xVel, leftPoints, rightPoints
    ballX = ballX + xVel
    ballY = ballY + yVel
    if(ballY-ballRadius< 0):
        yVel = abs(yVel)
    if(ballY+ballRadius>WINDOWHEIGHT):
        yVel = abs(yVel)*-1
    if(ballX+ballRadius>rightPaddleX and (ballY > rightPaddleY and ballY < rightPaddleY+PADDLEHEIGHT)):
        xVel = abs(xVel) * -1
    if(ballX-ballRadius<leftPaddleX+PADDLEWIDTH and (ballY > leftPaddleY and ballY < leftPaddleY+PADDLEHEIGHT)):
	    xVel = abs(xVel)
    if(ballX+ballRadius>WINDOWWIDTH): #Out of bounds right
        leftPoints += 1
        ballSpawn(-1)
    if(ballX-ballRadius < 0): #Out of bounds lef
        rightPoints += 1
        ballSpawn(1)
        
def getPaddlePositions(senLeft, senRight):
    while True:
        #global leftPaddleY, rightPaddleY
        clampedLeftDist = 480-(leftSensor.getDistance()/50) * 480
        clampedRightDist = 480-(rightSensor.getDistance()/50) * 480
        senLeft.value = clampedLeftDist
        senRight.value = clampedRightDist

    
def ballSpawn(xMod):
    global ballX, ballY, xVel, yVel
    randX = 2 * xMod
    randY = random.randint(1, 3)
    xVel = randX
    yVel = randY
    ballX = 200
    ballY = 200

def drawPaddles():
    #PaddleLeft
	paddleLeft = pygame.Rect(leftPaddleX,leftPaddleY, PADDLEWIDTH, PADDLEHEIGHT)
	pygame.draw.rect(DISPLAYSURF, WHITE, paddleLeft)
	#PaddleRight
	paddleRight = pygame.Rect(rightPaddleX,rightPaddleY, PADDLEWIDTH, PADDLEHEIGHT)
	pygame.draw.rect(DISPLAYSURF, WHITE, paddleRight)

def drawBall():
	global ballX, ballY, DISPLAYSURF
	pygame.draw.circle(DISPLAYSURF, WHITE,(ballX,ballY), ballRadius)

def showStartScreen():
	pass
	while True:
		val = 1
		#wait till confirmation

if __name__ == '__main__':
    global senLeft, senRight
    senLeft = Value('d', 0)
    senRight = Value('d', 0)
    p = Process(target = getPaddlePositions, args=(senLeft, senRight))
    p.start()
    main()



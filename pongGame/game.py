# PALM PONG: an experiment in terrible motion controls
# By: Jarod Honas and Reece Berens
# Music By: Cody Adams
# Created: 10/19/2018
# HACK K-State Project

import random, pygame, sys
from pygame.locals import *
from hardware import *
import RPi.GPIO as GPIO
from multiprocessing import Process, Value
import time
from leaderboard import *

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()
FPS = 60
WINDOWWIDTH = 1920 #was 640
WINDOWHEIGHT = 1080 #was 480
PADDLEWIDTH = 50
PADDLEHEIGHT = 300
leftPaddleX = 0
leftPaddleY = int(WINDOWHEIGHT/2)
leftPaddleYApproach = 0
rightPaddleX = WINDOWWIDTH-PADDLEWIDTH
rightPaddleY = int(WINDOWHEIGHT/2)
rightPaddleYApproach = 0
ballX = int(WINDOWWIDTH/2)
ballY = int(WINDOWHEIGHT/2)
ballRadius = 25
xVel = 4
yVel = 2
rightPoints = 0
leftPoints = 0
rallyCount = 0
gameState = 0
winner = 0


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

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, leftPaddleY, rightPaddleY, leftPoints, rightPoints, rallyCount, ballX, ballY, xVel, yVel, winner, window
    pygame.init()
    pygame.mixer.music.load("hack 1 audio.ogg")
    pygame.mixer.music.play(-1)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('PALM PONG')
    while True:
        if(gameState == 0):
            showStartScreen()
            #RESET VALUES
            ballX = int(WINDOWWIDTH/2)
            ballY =  int(WINDOWHEIGHT/2)
            yVel = random.randint(1, 3)
            xVel = 5
            leftPaddleY = int(WINDOWHEIGHT/2)
            rightPaddleY = int(WINDOWHEIGHT/2)
            leftPoints = 0
            rightPoints = 0
            rallyCount = 0
            winner = 0
        runGame()
        if(gameState == 0):
            time.sleep(2)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
		
def runGame():
    global senLeft, senRight, leftPaddleY, rightPaddleY, rightPaddleYApproach, leftPaddleYApproach
    #Set Positions
    #getPaddlePosistions()
    updateBall()
    
    #MOTION READOUTS
    if(senLeft.value <= WINDOWHEIGHT and senLeft.value >= 0):
        leftPaddleYApproach = senLeft.value
    if(senRight.value <= WINDOWHEIGHT and senRight.value >= 0):
        rightPaddleYApproach = senRight.value
        
    #Paddle Speed and Smoothing
    approachSpeed = 12
    mod = 4
    if(leftPaddleY-leftPaddleYApproach > 1):
        leftPaddleY -= int(abs(leftPaddleY-leftPaddleYApproach)/100)*mod
    if(leftPaddleY-leftPaddleYApproach < 1):
        leftPaddleY += int(abs(leftPaddleY-leftPaddleYApproach)/100)*mod
    if(rightPaddleY-rightPaddleYApproach > 1):
        rightPaddleY -= int(abs(rightPaddleY-rightPaddleYApproach)/100) *mod
    if(rightPaddleY-rightPaddleYApproach < 1):
        rightPaddleY += int(abs(rightPaddleY-rightPaddleYApproach)/100) *mod
        
    #Draw onto SURF
    DISPLAYSURF.fill(BGCOLOR)
    drawPaddles()
    drawBall()
    drawGameText()
    drawWinner()
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def updateBall():
    global ballX, ballY, yVel, xVel, leftPoints, rightPoints, rallyCount, gameState
    ballX += xVel
    ballY += yVel
    xCheck = xVel
    rallyMod = 1
    if(ballY-ballRadius< 125): #Top Bound
        yVel = abs(yVel)
    if(ballY+ballRadius>WINDOWHEIGHT-60): #Bottom Bound
        yVel = abs(yVel)*-1
    if(ballX+ballRadius>rightPaddleX and (ballY > rightPaddleY and ballY < rightPaddleY+PADDLEHEIGHT)):
        xVel = abs(xVel) * -1 #Right Paddle Collision
        rallyMod = -1
    if(ballX-ballRadius<leftPaddleX+PADDLEWIDTH and (ballY > leftPaddleY and ballY < leftPaddleY+PADDLEHEIGHT)):
	    xVel = abs(xVel) #Left Paddle Collision
    if(ballX+ballRadius>WINDOWWIDTH): #Out of bounds right
        leftPoints += 1
        if(leftPoints >= 100):
            gameState = 0
            versusWinner(1)
            return
        ballSpawn(-1)
    if(ballX-ballRadius < 0): #Out of bounds left
        rightPoints += 1
        if(rightPoints >= 100):
            gameState = 0
            versusWinner(2)
            return
        ballSpawn(1)
    if(xVel != xCheck):
        xVel += 1 * rallyMod
        rallyCount += 1
        
def getPaddlePositions(senLeft, senRight):
    while True:
        topBound = 25 #Max Centimeter height accepted from sensor
        clampedLeftDist = WINDOWHEIGHT-((leftSensor.getDistance()/topBound) * WINDOWHEIGHT)
        clampedRightDist = WINDOWHEIGHT-((rightSensor.getDistance()/topBound) * WINDOWHEIGHT)
        senLeft.value = clampedLeftDist
        senRight.value = clampedRightDist

    
def ballSpawn(xMod):
    global ballX, ballY, xVel, yVel, gameState
    if(gameState == 2): #COOP RESET
        coopWinner(xMod)
        gameState = 0
        return
    randX = 5 * xMod
    randY = random.randint(1, 3)
    xVel = randX
    yVel = randY
    ballX = int(WINDOWWIDTH/2)
    ballY = int(WINDOWHEIGHT/2)

def drawPaddles():
    #PaddleLeft
	paddleLeft = pygame.Rect(leftPaddleX,leftPaddleY, PADDLEWIDTH, PADDLEHEIGHT)
	pygame.draw.rect(DISPLAYSURF, WHITE, paddleLeft)
	#PaddleRight
	paddleRight = pygame.Rect(rightPaddleX,rightPaddleY, PADDLEWIDTH, PADDLEHEIGHT)
	pygame.draw.rect(DISPLAYSURF, WHITE, paddleRight)

def drawBall():
	global ballX, ballY, DISPLAYSURF
	pygame.draw.circle(DISPLAYSURF, WHITE,(int(ballX),int(ballY)), ballRadius)

def drawGameText():
    global gameState, DISPLAYSURF, leftPoints, rightPoints
    if(gameState == 1): #Versus Match
        subFont = pygame.font.Font('freesansbold.ttf', 25)
        subSurf = subFont.render(str(leftPoints) + ' | ' + str(rightPoints), True, WHITE)
        drawRectSub = pygame.Rect(int(WINDOWWIDTH/2-50), int(50), 0,0)
        DISPLAYSURF.blit(subSurf, drawRectSub)
    if(gameState == 2): #Coop Match
        subFont = pygame.font.Font('freesansbold.ttf', 25)
        subSurf = subFont.render('Rally: ' + str(rallyCount), True, WHITE)
        drawRectSub = pygame.Rect(int(WINDOWWIDTH/2-50), int(50), 0,0)
        DISPLAYSURF.blit(subSurf, drawRectSub)
        
def versusWinner(val):
    global winner
    winner = 1
    if(val == 2):
        winner = 2
    
def coopWinner(val):
    global winner
    postScore("AAA", rallyCount)
    winner = 3

def drawWinner():
    global DISPLAYSURF
    if(winner == 1):
        subFont = pygame.font.Font('freesansbold.ttf', 100)
        subSurf = subFont.render('LEFT WINS!', True, WHITE)
        drawRectSub = pygame.Rect(int(WINDOWWIDTH/2 - 300), int(WINDOWHEIGHT/2 - 300), 0,0)
        DISPLAYSURF.blit(subSurf, drawRectSub)
    if(winner == 2):
        subFont = pygame.font.Font('freesansbold.ttf', 100)
        subSurf = subFont.render('RIGHT WINS!', True, WHITE)
        drawRectSub = pygame.Rect(int(WINDOWWIDTH/2 - 300), int(WINDOWHEIGHT/2 - 300), 0,0)
        DISPLAYSURF.blit(subSurf, drawRectSub)
    if(winner == 3):
        subFont = pygame.font.Font('freesansbold.ttf', 100)
        subSurf = subFont.render('RALLY COUNT: ' + str(rallyCount), True, WHITE)
        drawRectSub = pygame.Rect(int(WINDOWWIDTH/2 - 300), int(WINDOWHEIGHT/2 - 300), 0,0)
        DISPLAYSURF.blit(subSurf, drawRectSub)
    

def showStartScreen():
	global DISPLAYSURF, senLeft, senRight, gameState
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf = titleFont.render('PALM PONG', True, WHITE)
	drawRect = pygame.Rect(int(WINDOWWIDTH/2 - 300), int(WINDOWHEIGHT/2 - 300), 0,0)
	subFont = pygame.font.Font('freesansbold.ttf', 25)
	subSurf = subFont.render('LEFT SENSOR : VERSUS || COOP : RIGHT SENSOR', True, WHITE)
	drawRectSub = pygame.Rect(int(WINDOWWIDTH/2 - 300), int(WINDOWHEIGHT/2 - 200), 0,0)
	while True:
            DISPLAYSURF.fill(BGCOLOR)
            DISPLAYSURF.blit(titleSurf, drawRect)
            DISPLAYSURF.blit(subSurf, drawRectSub)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            if(senLeft.value > 0):
                gameState = 1
                return
            if(senRight.value > 0):
                gameState = 2
                return
		
                                    

if __name__ == '__main__':
    lcd = LCD()
    l = Process(target = lcd.displayLeaderboard)
    l.start()
    global senLeft, senRight
    senLeft = Value('d', WINDOWHEIGHT/2)
    senRight = Value('d', WINDOWHEIGHT/2)
    p = Process(target = getPaddlePositions, args=(senLeft, senRight))
    p.start()
    main()



#!/usr/bin/env python
import random
import threading
import signal
import sys
import pygame
from pygame.locals import *
import math
from moleThread import MoleThread
from threading import Thread
import Tkinter
import tkMessageBox

windowWidth = 1300
windowHeight = 680
imageWidth = 106
imageHeight = 116
lifeWidth = 27
lifeHeight = 29
grass_color = (0,130,64)
locations = []
threads = []
lives = []
for i in range(0, (int)(math.floor(windowHeight / (10 +imageHeight)))):
    for j in range(0, (int)(math.floor(windowWidth/ (10 + imageWidth)))):
        locations.append([j * (10 + imageWidth), i * (10 + imageHeight)])

def signal_handler(signal, frame):
    print('You exited the program\n')
    for i in range(0, len(threads) - 1):
        threads[i].stop()
    sys.exit(0)
'''
* This function will create all the threads and mole sprites we need for the game
@param{numberOfMoles} - The total number of threads/moles we will be creating
@param{semaphore} - This semaphore is instantiatied with the maximum number
of moles that can be popped up at once
@param{pygame sprite group} - this group holds all the mole sprites
'''
def startThreads(numberOfMoles, semaphore, _moleGroup, lifeGroup, livesSemaphore, livesRemaining, deathGroup):
    threads = []
    for i in range(numberOfMoles):
        location = locations[random.randint(0, len(locations) - 1)]
        threadMole = pygame.sprite.Sprite()
        threadMole.pos = i
        threadMole.isUp = False
        threadMole.image = pygame.image.load("empty.png").convert_alpha()
        threadMole.rect = Rect(location[0], location[1], imageWidth, imageHeight)
        _moleGroup.add(threadMole)
        thread = MoleThread(i, semaphore, threadMole, lifeGroup, livesSemaphore, livesRemaining, lives, deathGroup)
        thread.setDaemon(True)
        thread.start()
    return threads

'''
*
'''
def makeLives():
    startX = windowWidth - (lifeWidth + 5) * 10
    yPos = windowHeight - lifeHeight - 5
    returnGroup = pygame.sprite.Group()
    for i in range (0, 9):
        life = pygame.sprite.Sprite()
        life.rect = Rect(startX + i * lifeWidth, yPos, lifeWidth, lifeHeight)
        life.image = pygame.image.load("tiny_mole.png")
        returnGroup.add(life)
        lives.append(life)

    return returnGroup

def playAgain():
    return tkMessageBox.askyesno("Play Again","Would you like to play again?")


'''
* This function creates the pygame object and handles the main game loop
@param{numberOfMoles} - maximum number of moles/threads we will make
@param{semaphore} - this semaphore prevents us from going showing too many moles
at one time.
'''
def game(numberOfMoles, semaphore):
    livesSemaphore = threading.BoundedSemaphore(9)
    livesRemaining = 10
    playerScore = 0
    # initialize game engine
    pygame.init()
    # set screen width/height and caption
    size = [windowWidth, windowHeight]
    screen = pygame.display.set_mode(size, FULLSCREEN)

    pygame.display.set_caption('My Game')
    myfont = pygame.font.SysFont("monospace", 48)

    moleGroup = pygame.sprite.Group()
    # Create lives
    lifeGroup = makeLives()
    deathGroup = pygame.sprite.Group()
    # initialize clock. used later in the loop.
    clock = pygame.time.Clock()

    threads = startThreads(numberOfMoles, semaphore, moleGroup, lifeGroup, livesSemaphore, livesRemaining, deathGroup)
    # Loop until the user clicks close button
    done = False
    while done == False:
        scoretext = myfont.render("Score = "+str(playerScore), 1, (0,0,0))
        # write event handlers here
        x = 0
        y = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP: x,y = event.pos
            if event.type == pygame.QUIT:
                # for i in range(0, len(threads) - 1):
                #     threads[i].stop()
                done = True
        # write game logic here
        for mole in moleGroup:
            if mole.rect.collidepoint(x, y):
                if mole.isUp:
                    mole.image = pygame.image.load("empty.png").convert_alpha()
                    playerScore += 1
                    mole.isUp = False

        if(len(lives) == 0):
            if playAgain():
                done = True
                main()
            else:
                done = True
        # clear the screen before drawing
        screen.fill((grass_color))
        # write draw code here
        moleGroup.draw(screen)
        lifeGroup.draw(screen)
        deathGroup.draw(screen)
        screen.blit(scoretext, (5, 10))
        pygame.display.update()

        clock.tick(60)

    # close the window and quit
    pygame.quit()


'''
* Main function for our program
'''
def main():
    # Make sure we have the correct number of arguments
    if len(sys.argv) != 3:
        print('incorrect number of arguments')
        exit(0)

    # Make sure the arguments are actually numbers
    try:
        numberOfMoles = int(sys.argv[1])
        maxMoles = int(sys.argv[2])
    except ValueError:
        print('Your command line arguments should be input as follows <number of moles> <max moles at at time>\n')

    # check to see if there are too many moles to display
    if numberOfMoles >= len(locations):
        print('That is too many moles to display. Please use less than ' + (str)(len(locations)) + ' moles')
        exit(1)

    # make sure we aren't trying to make more threads than we have moles
    if maxMoles > numberOfMoles:
        print('Your maximum number of moles is greater than the amount of moles on screen')

    signal.signal(signal.SIGINT, signal_handler)
    semaphore = threading.BoundedSemaphore(value=maxMoles)
    game(numberOfMoles, semaphore)

main()

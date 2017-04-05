#!/usr/bin/env python
import random
import threading
import signal
import sys
import pygame
from pygame.locals import *
import math
from moleThread import MoleThread


windowWidth = 1300
windowHeight = 680
imageWidth = 106
imageHeight = 116
grass_color = (0,130,64)

locations = []
threads = []
for i in range(0, (int)(math.floor(windowHeight / (10 +imageHeight)))):
    for j in range(0, (int)(math.floor(windowWidth/ (10 + imageWidth)))):
        locations.append([j * (10 + imageWidth), i * (10 + imageHeight)])

def signal_handler(signal, frame):
    print('You exited the program\n')
    for i in range(0, len(threads) - 1):
        threads[i].stop()
    sys.exit(0)

def startThreads(numberOfMoles, semaphore, _moleGroup):
    threads = []
    for i in range(numberOfMoles):
        location = locations[random.randint(0, len(locations) - 1)]
        threadMole = pygame.sprite.Sprite()
        threadMole.pos = i
        threadMole.isUp = False
        threadMole.image = pygame.image.load("empty.png").convert_alpha()
        threadMole.rect = Rect(location[0], location[1], imageWidth, imageHeight)
        _moleGroup.add(threadMole)
        thread = MoleThread(i, semaphore, threadMole)
        thread.start()
    return threads

def game(numberOfMoles, semaphore):
    playerScore = 0
    # initialize game engine
    pygame.init()
    # set screen width/height and caption
    size = [windowWidth, windowHeight]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('My Game')

    moleGroup = pygame.sprite.Group()
    # initialize clock. used later in the loop.
    clock = pygame.time.Clock()

    threads = startThreads(numberOfMoles, semaphore, moleGroup)
    print('you made it!')
    # Loop until the user clicks close button
    done = False
    while done == False:
        # write event handlers here
        x = 0
        y = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP: x,y = event.pos
            if event.type == pygame.QUIT:
                for i in range(0, len(threads) - 1):
                    threads[i].stop()
                done = True
        # write game logic here

        for mole in moleGroup:
            if mole.rect.collidepoint(x, y):
                if mole.isUp:
                    mole.image = pygame.image.load("empty.png").convert_alpha()
                    playerScore += 1
        # clear the screen before drawing
        screen.fill((grass_color))
        # write draw code here
        moleGroup.draw(screen)
        pygame.display.update()

        clock.tick(60)

    # close the window and quit
    pygame.quit()

def main():
    # Handle the command line arguments
    if len(sys.argv) != 3:
        print('incorrect number of arguments')
        exit(0)

    try:
        numberOfMoles = int(sys.argv[1])
        maxMoles = int(sys.argv[2])
    except ValueError:
        print('Your command line arguments should be input as follows <number of moles> <max moles at at time>\n')

    #check to see if there are too many moles to display
    print(len(locations))
    if numberOfMoles >= len(locations):
        print('That is too many moles to display. Please use less than ' + (str)(len(locations)) + ' moles')
        exit(1)

    if maxMoles > numberOfMoles:
        print('Your maximum number of moles is greater than the amount of moles on screen')

    signal.signal(signal.SIGINT, signal_handler)

    semaphore = threading.BoundedSemaphore(value=maxMoles)

    game(numberOfMoles, semaphore)

main()

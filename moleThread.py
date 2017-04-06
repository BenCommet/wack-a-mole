import threading
import time
import random
import pygame
from pygame.locals import *

'''
* This class creates a thread that builds on the threading.Thread class. It adds
methods that handle popping up moles and putting them down.
'''
class MoleThread(threading.Thread):
    '''
    * Constructor of the class
    @param{int} moleNum - This integer represents the position of the moleNum
    @param{semaphore} - This semaphore is instantiatied with the maximum number
    of moles that can be popped up at once
    @param{sprite} - this is a pygame sprite object, we need it to manipulate what
    the user sees
    '''
    def __init__(self, moleNum, molesUp, moleSprite, lifeGroup, livesSemaphore, livesRemaining, lives, deathGroup):
        threading.Thread.__init__(self)
        self.moleNum = moleNum
        self.molesUp = molesUp
        self.moleSprite = moleSprite
        self.lifeGroup = lifeGroup
        self.livesSemaphore = livesSemaphore
        self.livesRemaining = livesRemaining
        self.deathGroup = deathGroup
        self.lives = lives
        self.frames = ['empty_hole', 'mole_up.png']
        self.animationTime = 50

    '''
    * This function is called on startup of a thread. It will sleep for a random
    period of time and then call the moleUp function
    '''
    def run(self):
        frand = random.random() * 7 + 3
        time.sleep(frand)
        self.moleUp()

    '''
    *
    '''
    def removeLife(self):
        currentLife = self.lives.pop()
        self.deathGroup.add(currentLife)
        self.lifeGroup.remove(currentLife)
        currentLife.image = pygame.image.load("tiny_mole_fade.png").convert_alpha()

    '''
    * This function acquires from the molesUp semaphore and changes the appearance of
    a mole to reflect the fact that is now up. A random period of time is generated
    '''
    def moleUp(self):
        self.molesUp.acquire()
        self.moleSprite.isUp = True
        self.moleSprite.image = pygame.image.load("mole_up.png").convert_alpha()
        time.sleep(random.random()*4 + 1)
        self.moleDown()

    '''
    * This function will make the mole go down
    '''
    def moleDown(self):
        self.molesUp.release()
        if self.moleSprite.isUp:
            self.moleSprite.image = pygame.image.load("empty.png").convert_alpha()
        if self.moleSprite.isUp:
            self.livesSemaphore.acquire()
            self.removeLife()
        #prevent the user from being able to click on the invisible sprite and get points
        self.moleSprite.isUp = False
        self.run()

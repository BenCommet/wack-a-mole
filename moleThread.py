import threading
import time
import random
import pygame
from pygame.locals import *

'''
This class creates a thread that builds on the threading.Thread class. It adds
methods that handle popping up moles and putting them down.
'''
class MoleThread(threading.Thread):
    '''
    Constructor of the class
    @param{int} moleNum - This integer represents the position of the moleNum
    @param{semaphore} - This semaphore is instantiatied with the maximum number
    of moles that can be popped up at once
    @param{sprite} - this is a pygame sprite object, we need it to manipulate what
    the user sees
    '''
    def __init__(self, moleNum, semaphore, moleSprite):
        threading.Thread.__init__(self)
        self.moleNum = moleNum
        self.semaphore = semaphore
        self.moleSprite = moleSprite
        self.frames = ['empty_hole', 'mole_up.png']
        self.animationTime = 50

    '''
    This function is called on startup of a thread. It will sleep for a random
    period of time and then call the moleUp function
    '''
    def run(self):
        frand = random.random() * 7 + 3
        time.sleep(frand)
        self.moleUp()

    '''
    This function is called to kill off a thread
    '''
    def stop(self):
        print('stopping')
        return 0

    '''
    This function acquires from a semaphore and changes the appearance of a mole
    to reflect the fact that is now up. A random period of time is generated
    '''
    def moleUp(self):
        self.semaphore.acquire()
        self.moleSprite.isUp = True
        self.moleSprite.image = pygame.image.load("mole_up.png").convert_alpha()
        time.sleep(random.random()*4 + 1)
        self.moleDown()

    '''
    
    '''
    def moleDown(self):
        self.semaphore.release()
        if self.moleSprite.isUp:
            self.moleSprite.image = pygame.image.load("empty.png").convert_alpha()
        self.run()

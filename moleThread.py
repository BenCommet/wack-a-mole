import threading
import time
import random
import pygame
from pygame.locals import *

class MoleThread(threading.Thread):
    def __init__(self, moleNum, semaphore, moleSprite):
        threading.Thread.__init__(self)
        self.moleNum = moleNum
        self.semaphore = semaphore
        self.moleSprite = moleSprite

    def run(self):
        frand = random.random() * 7 + 3
        time.sleep(frand)
        self.moleUp()

    def stop(self):
        return 0

    def moleUp(self):
        self.semaphore.acquire()
        self.moleSprite.isUp = True
        self.moleSprite.image = pygame.image.load("mole_up.png").convert_alpha()
        time.sleep(random.random()*4 + 1)
        self.moleDown()

    def moleDown(self):
        self.semaphore.release()
        if self.moleSprite.isUp:
            self.moleSprite.image = pygame.image.load("empty.png").convert_alpha()
        self.run()

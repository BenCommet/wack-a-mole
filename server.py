#!/usr/bin/env python
import time
import random
import threading
import signal

def randSleep(moleNum):
    frand = random.random() * 7 + 3
    time.sleep(frand)
    wackTheMole(moleNum)
    randSleep(moleNum)

def wackTheMole(moleNum):
    print("wacking: %d", moleNum)

semaphores =[]
threads = []
for i in range(5):
    thread = threading.Thread(target=randSleep, args =(i,))
    threads.append(thread)
    thread.start()
    semaphore = threading.Semaphore()
    semaphores.append(semaphore)

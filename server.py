#!/usr/bin/env python
import time
import random
import threading
import signal
import sys
import flask
# from flask import Flask, render_template
# from flask_socketio import send, emit

# Handle the command line arguments
if len(sys.argv) != 3:
    print('incorrect number of arguments')
    exit(0)

try:
    numberOfMoles = int(sys.argv[1])
    maxMoles = int(sys.argv[2])
except ValueError:
    print('Your command line arguments should be input as follows <number of moles> <max moles at at time>\n')
def signal_handler(signal, frame):
    print('You exited the program\n')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

semaphore = threading.BoundedSemaphore(value=maxMoles)

def randSleep(moleNum):
    frand = random.random() * 7 + 3
    time.sleep(frand)
    print(moleUp(moleNum))

def moleUp(moleNum):
    semaphore.acquire()
    return random.random()*2 + .5

def moleDown(moleNum):
    semaphore.release()
    randSleep(moleNum)

# threads = []
# for i in range(numberOfMoles):
#     thread = threading.Thread(target=randSleep, args =(i,))
#     threads.append(thread)
#     thread.start()

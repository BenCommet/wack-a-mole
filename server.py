#!/usr/bin/env python
import time
import random
import threading
import signal
import sys
import flask
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
# Handle the command line arguments
if len(sys.argv) != 3:
    print('incorrect number of arguments')
    exit(0)

try:
    numberOfMoles = int(sys.argv[1])
    maxMoles = int(sys.argv[2])
except ValueError:
    print('Your command line arguments should be input as follows <number of moles> <max moles at at time>\n')

threads = []
def signal_handler(signal, frame):
    print('You exited the program\n')
    sys.exit(0)
    for i in threads:
        i.exit()


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

# for i in range(numberOfMoles):
#     thread = threading.Thread(target=randSleep, args =(i,))
#     threads.append(thread)
#     thread.start()

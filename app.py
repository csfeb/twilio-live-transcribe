import audioop
import base64
import json
import os
from flask import Flask, request
from flask_socketio import SocketIO
import vosk
import redis

app = Flask(__name__)
socketio = SocketIO(app)
model = vosk.Model('model')
r = redis.from_url(os.environ['REDIS_URL'])

CL = '\x1b[0K'
BS = '\x08'

@app.route("/")
def hello():
    return 'Hello, World!'

@socketio.on('connect')
def onConnect():
    print('connect', request)
    print('connect', request.sid)
    r.sadd('conn', request.sid)
    send({'state': 'Connected', 'sid': request.sid})

@socketio.on('disconnect')
def onDisconnect():
    print('disconnect', request)
    print('disconnect', request.sid)
    r.srem('conn', request.sid)
    send({'state': 'Disconnected', 'sid': request.sid})

if __name__ == '__main__':
    print('Starting server...')
    socketio.run(app)
    print('Started server.')

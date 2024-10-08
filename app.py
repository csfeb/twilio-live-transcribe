import audioop
import base64
import json
import os
from flask import Flask, request
from flask_socketio import SocketIO
import vosk
import redis

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
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

@socketio.on('disconnect')
def onDisconnect():
    print('disconnect', request)
    print('disconnect', request.sid)
    r.srem('conn', request.sid)

@socketio.event
def test():
    send(request.sid)

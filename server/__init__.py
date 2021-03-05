from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_socketio import SocketIO, send, emit, join_room
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = '65rdxchu87'
CORS(app, supports_credentials=True)

socket = SocketIO(app, cors_allowed_origins="*")
app.host = 'localhost'
app.debug = True

#---public page---
@app.route('/')
def home():
	return send_from_directory('../client/', 'index.html')

@socket.on('message')
def handleMessage(msg):
    print('Message:', msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socket.run(app, host="127.0.0.1", port=5000)

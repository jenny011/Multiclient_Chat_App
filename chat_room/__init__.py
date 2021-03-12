from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_socketio import SocketIO, send, emit, join_room, disconnect
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = '65rdxchu87'
CORS(app, supports_credentials=True)

socket = SocketIO(app, cors_allowed_origins="*")
app.host = 'localhost'
app.debug = True

active_users = {}

#---public page---
@app.route('/')
def public():
	return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	if username in active_users:
		return render_template('login.html', err='Username already exists!')
	else:
		active_users[username] = ""
		print("-----pretend to give a page of active users-----")
	return render_template('index.html', username=username)

@app.route('/logout', methods=['GET'])
def logout():
	return redirect(url_for('public'))


@socket.on('connect')
def on_connect():
	print("Hi", request.sid)

@socket.on('message')
def handleMessage(msg):
	print(request.sid, "sent:", msg)
	send(msg, broadcast=True)

@socket.on('disconnect')
def on_disconnect():
	print("Bye", request.sid)
	return redirect(url_for('public'))

@socket.on('join_room')
def on_disconnect(msg):
	user = msg['username']
	print("Hi", user)
	active_users[user] = request.sid
	send(user + " joined", broadcast=True)

@socket.on('leave_room')
def on_disconnect(msg):
	user = msg['username']
	print("Bye", user)
	active_users.pop(user)
	send(user + " left", broadcast=True)

@socket.on('disconnect')
def on_disconnect():
	print("Bye", request.sid)

# if __name__ == '__main__':
#     socket.run(app, host="127.0.0.1", port=5000)

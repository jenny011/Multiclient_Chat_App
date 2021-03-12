from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_socketio import SocketIO, send, emit, join_room, disconnect
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = '65rdxchu87'
CORS(app, supports_credentials=True)

socket = SocketIO(app, cors_allowed_origins="*")
app.host = 'localhost'
app.debug = True

usernames = []
active_users = {}

#---public page---
@app.route('/')
def public():
	return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	if username in usernames:
		return render_template('login.html', err='Username already exists!')
	else:
		print("-----pretend to give a page of active users-----")
	return render_template('index.html', username=username)

@socket.on('logout_req')
def logout_req():
	#active_users.pop(username)
	emit('logout_res', {}, callback=disconnect())

@socket.on('connect')
def on_connect():
	#active_users[request.sid] = username
	print("Hi", request.sid)
	send(request.sid + " joined", broadcast=True)

@socket.on('message')
def handleMessage(msg):
	print(request.sid, "sent:", msg)
	send(msg, broadcast=True)

@socket.on('disconnect')
def on_disconnect():
	print("Bye", request.sid)
	send(request.sid + " left", broadcast=True)

@socket.on('client_connect')
def on_disconnect(msg):
	print("Hi", msg['username'])

@socket.on('client_disconnect')
def on_disconnect(msg):
	print("Bye", msg['username'])
	return redirect(url_for('public'))

# if __name__ == '__main__':
#     socket.run(app, host="127.0.0.1", port=5000)

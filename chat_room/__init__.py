from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_socketio import SocketIO, send, emit, join_room, disconnect
from flask_cors import CORS
from flask_login.utils import logout_user
from flask_login import login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = '65rdxchu87'
CORS(app, supports_credentials=True)

socket = SocketIO(app, cors_allowed_origins="*")
app.host = 'localhost'
app.debug = True

###---------------------data store---------------------###
###---------------------data store---------------------###
###---------------------data store---------------------###
active_users = {}
active_rooms = {}


###---------------------HTTP routes---------------------###
###---------------------HTTP routes---------------------###
###---------------------HTTP routes---------------------###
#---go to login page---
@app.route('/')
def public():
	return render_template('login.html')

#---go to entrance page---
@app.route('/login', methods=['POST'])
def login():
	# if not current_user.is_authenticated:
	# 	username = request.form['username']
	# 	password = request.form['password']
	#   user = User.query.get(username)
	# 	login_user(user)
	username = request.form['username']
	session['username'] = username
	print(session)
	# commented out for testing
	# if username in active_users:
	# 	return render_template('login.html', err='Username already exists!')
	# else:
	active_users[username] = []
	rooms = [room for room in active_rooms.keys()]
	users = []
	for user in active_users.keys():
		if user != username:
			users.append(user)
	print("rooms", rooms)
	print("users", users)
	return render_template('entrance.html', username=username, rooms=rooms, users=users)

#---go to chat page---
@app.route('/chat_room', methods=['POST'])
def chat_room():
	target_room = request.form['target']
	try:
		username = session['username']
		print("----Emit socket event: join a room----")
		return render_template('chat.html', username=username)
	except:
		return redirect(url_for("login"))

@app.route('/chat_user', methods=['POST'])
def chat_user():
	print(request)
	target_user = request.form['target']
	try:
		username = session['username']
		#TODO
		print("----Emit socket event: create a room----")
		return render_template('chat.html', username=username)
	except:
		return redirect(url_for("login"))

#---leave_chat---
@app.route('/leave_chat', methods=['GET'])
def leave_chat():
	try:
		username = session['username']
		#TODO: remove user from room, remove room from user
		rooms = [room for room in active_rooms.keys()]
		users = []
		for user in active_users.keys():
			if user != username:
				users.append(user)
		print("rooms", rooms)
		print("users", users)
		return render_template('entrance.html', username=username, rooms=rooms, users=users)
	except:
		return redirect(url_for('login'))

#---log out---
@app.route('/logout', methods=['GET'])
def logout():
	print(session)
	username = session['username']
	active_users.pop(username)
	if 'username' in session:
		session.pop('username')
	return redirect(url_for('public'))



###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
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
	send(user + " left", broadcast=True)

@socket.on('disconnect')
def on_disconnect():
	print("Bye", request.sid)

# if __name__ == '__main__':
#     socket.run(app, host="127.0.0.1", port=5000)

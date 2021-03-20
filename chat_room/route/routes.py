from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_socketio import SocketIO, send, emit, join_room, disconnect
from flask_cors import CORS
# from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from chat_room import app, socket, login, all_users, active_users, active_rooms
from chat_room.route.utils import *
from chat_room.model.models import *
# from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


###---------------------HTTP routes---------------------###
###---------------------HTTP routes---------------------###
###---------------------HTTP routes---------------------###
#---go to login page---
@app.route('/')
def public():
	return render_template('index.html')

@app.route('/goToRegister', methods=['GET'])
def goToRegister():
    return render_template('register.html')

@app.route('/goToLogin', methods=['GET'])
def goToLogin():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username in all_users:
        return render_template('register.html', err='Username already exists!')
    new_user = User(username, password)
    all_users[username] = new_user
    print(all_users.keys())
    return render_template('login.html')

#---go to entrance page---
@app.route('/login', methods=['POST'])
def login():
    #try:
    username = request.form['username']
    password = request.form['password']
    user = all_users[username]
    if not user:
        return render_template('register.html', err='Please register!')
    if not user.check_password(password):
        return render_template('login.html', err="Username and password don't match!")
    session["username"] = username
    active_users[username] = []
    rooms = get_active_rooms()
    users = get_active_users(username)
    return render_template('entrance.html', username=username, rooms=rooms, users=users)
    # except:
    #     return render_template('login.html', err="Unkown error")

#---go to chat page---
@app.route('/chat_room', methods=['POST'])
def chat_room():
    target_room = request.form['target']
    # try:
    username = session["username"]
    print("----Emit socket event: join a room----")
    return render_template('chat.html', username=username)
	# except:
	# 	return redirect(url_for("login"))

@app.route('/chat_user', methods=['POST'])
def chat_user():
    target_user = request.form['target']
    # try:
    username = session["username"]
    #TODO
    print("----Emit socket event: create a room----")
    return render_template('chat.html', username=username)
	# except:
	# 	return redirect(url_for("login"))

#---leave_chat---
@app.route('/leave_chat', methods=['GET'])
def leave_chat():
	try:
		username = session["username"]
		rooms = [room for room in active_rooms.keys()]
		users = []
		for user in active_users.keys():
			if user != username:
				users.append(user)
		return render_template('entrance.html', username=username, rooms=rooms, users=users)
	except:
		return redirect(url_for('login'))

#---log out---
@app.route('/logout', methods=['GET'])
def logout():
    username = session["username"]
    active_users.pop(username)
    session.pop("username")
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
	#TODO: add room to user, add user to room
	# active_users[user] = request.sid
    send(user + " joined", broadcast=True)

@socket.on('leave_room')
def on_disconnect(msg):
    user = msg['username']
    print("Bye", user)
	#TODO: remove user from room, remove room from user
    send(user + " left", broadcast=True)

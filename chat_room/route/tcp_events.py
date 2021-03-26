from flask import Flask, request, json, jsonify, session, flash
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from chat_room import socket, login, all_users, active_users, all_rooms
from chat_room.route.utils import *
from chat_room.model.user import *
from chat_room.model.room import *


###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
@socket.on('connect')
def on_connect():
	print("--------", all_rooms)
	print("Hi", request.sid)

@socket.on('message')
def handleMessage(msg):
	print(request.sid, "sent:", msg)
	send(msg, broadcast=True)

@socket.on('disconnect')
def on_disconnect():
    print("Bye", request.sid)
    return redirect(url_for('public'))


@socket.on('create_room')
def on_create_room(msg):
	print("--------", all_rooms)
	username = msg['username']
	user = msg['user']
	print("Hi, create", username, user)
	if not user:
		print("Create my own room", username)
		new_room = create_room(username, [username])
		handle_join_room(username, new_room.room_ID)
	else:
		# if all_users[user].rooms and all_users[user].rooms[0] in all_rooms:
		# 	print("Exist room with target user", user)
		# 	ret, members = all_rooms[user].join(username)
		# 	print(members)
		# 	if ret:
		# 		print("create -> Join success")
		# 		handle_join_room(username, user)
		# 	else:
		# 		send("Room is full")
		# else:
		print("Create room with target user", user)
		new_room = create_room(user, [username, user])
		handle_join_room(username, new_room.room_ID)

@socket.on('join_room')
def on_join_room(msg):
	username = msg['username']
	room = msg['room']
	print("Joining, ", username, room)
	ret, members = all_rooms[room].join(username)
	print("Join success:", members)
	if ret:
		handle_join_room(username, room)
	else:
		send("Room is full")

@socket.on('leave_room')
def on_leave_room(msg):
	username = msg['username']
	room = msg['room']
	print("Leaving, ", username, room)
	ret, members = all_rooms[room].leave(username)
	print(members)
	if ret:
		leave_room(room)
		all_users[username].leave_room(room)
		emit("client_left", f'{username} left', room=room)

@socket.on('send_msg')
def send_message(msg):
	print(request.sid, "sent:", msg["msg"])
	send(msg["msg"], room=msg["room"])

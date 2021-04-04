import json
from flask import Flask, request, jsonify, session, flash
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_cors import CORS
import chat_room
from .utils import *
from ..model.user import *
from ..model.room import *


###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
#---------------connection----------------------------
@socket.on('connect')
def on_connect():
	print("Hi --------", all_rooms.keys())
	print("Connect")

@socket.on('disconnect')
def on_disconnect():
    print("Disconnect")
    return redirect(url_for('public'))


#------------create, join, leave----------------------
@socket.on('create_room')
def on_create_room(msg):
	print("Create --------", all_rooms.keys())
	print(msg)
	username = msg['username']
	user_id = msg['user']
	if not user_id:
		print(f'{username} Create my own room')
		new_room = create_room(username, [username])
		handle_join_room(username, new_room.id)
	else:
		for room_id in all_users[username].rooms.keys():
			print("===", username, room_id, all_rooms[room_id].members)
			if user_id in all_rooms[room_id].members:
				handle_join_room(username, room_id)
				return
		print(f'{username} Create room with target user {user_id}')
		#JENNY: add vs join
		new_room = create_room(f'{username}, {user_id}', [username, user_id])
		handle_join_room(username, new_room.id)

@socket.on('join_room')
def on_join_room(msg):
	username = msg['username']
	room_id = msg['room']
	print(f'{username} joining {room_id}')
	success, ret = all_rooms[room_id].join(username)
	if success:
		print(f'{room_id} members:', ret)
		handle_join_room(username, room_id)
	else:
		send(ret)

@socket.on('leave_room')
def on_leave_room(username):
	user = all_users[username]
	room_id = user.current_room_id
	print(f'{username} leaving {room_id}')
	success, ret = all_rooms[room_id].leave(username)
	if success:
		print(f'{username} left {room_id}, remaining members:', ret)
		handle_leave_room(username, room_id)
	else:
		send(ret)


#---------------messaging------------------------
@socket.on('message')
def handleMessage(msg):
	print(msg)
	msg_decoded = json.loads(msg)
	username = msg_decoded["username"]
	# msg = msg_decoded["msg"]
	user = all_users[username]
	room_id = user.current_room_id
	send(msg, room=room_id)

# @socket.on('send_msg')
# def send_message(msg):
# 	print(request.sid, "sent:", msg["msg"])
# 	send(msg["msg"], room=msg["room"])

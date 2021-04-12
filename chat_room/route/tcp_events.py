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

@socket.on('say_hi')
def say_hi(username):
	user = all_users[username]
	user.update_sid(request.sid)
	user.current_room_id = None
	print(all_users[username].sid)

@socket.on('disconnect')
def on_disconnect():
    print("Disconnect")
    return redirect(url_for('public'))


#------------invite, join----------------------

@socket.on('invite')
def on_invite(msg):
	msg = json.loads(msg)
	username = msg['username']
	user_id = msg['user']
	room_id = msg['room']
	if not room_id:
		#f'{username}, {user_id}'
		room_id = create_room("", [username])
		all_rooms[room_id].name = room_id
	else:
		if user_id in all_rooms[room_id]:
			send('user already in this room')
		if all_rooms[room].is_full():
			send('too many people in this room')
	# Tell user B
	ret = {"msg": f'{username} invited you to join room {room_id}', "username": username, "room": room_id}
	emit("client_invited", json.dumps(ret), room=all_users[user_id].sid)
	# Add user A
	handle_add_room(username, room_id)
	handle_join_room(username, room_id)


# @socket.on('accept')
# def on_accept(msg):
# 	# Add user B
# 	# msg = json.loads(msg)
# 	# user_id = msg["username"]
# 	# room_id = msg["room"]
# 	on_add_room(msg)

# @socket.on('reject')
# def on_reject(msg):
# 	username = msg['username']
# 	user_id = msg['user']
# 	room = msg['room_id']
# 	emit("client_refused", {"msg": f'{username} refused to join room {room}', "user": user_id}, user=all_users[user_id].sid)

@socket.on('add_room')
def on_add_room(msg):
	msg = json.loads(msg)
	username = msg['username']
	room_id = msg['room']
	if room_id in all_rooms:
		if all_rooms[room_id].is_full():
			send('too many people in this room')
		print(f'{username} joining {room_id}')
		success, ret = all_rooms[room_id].add(username)
		if success:
			print(f'{room_id} members:', ret)
			handle_add_room(username, room_id)
		else:
			send(ret)
	else:
		emit('refresh', room_id)


@socket.on('join_room')
def on_join_room(msg):
	msg = json.loads(msg)
	username = msg['username']
	room_id = msg['room']
	handle_join_room(username, room_id)


@socket.on('switch_room')
def on_switch_room(msg):
	msg = json.loads(msg)
	username = msg["username"]
	room = msg["room"]
	handle_switch_room(username, room)


#---------------leave------------------

@socket.on('leave_room')
def on_leave_room(username):
	user = all_users[username]
	room_id = user.current_room_id
	print(f'{username} leaving {room_id}')
	success, ret = all_rooms[room_id].remove(username)
	if success:
		print(f'{username} left {room_id}, remaining members:', ret)
		handle_leave_room(username, room_id)
	else:
		send(ret)

@socket.on('leave_page')
def on_leave_page(username):
	user = all_users[username]
	#user.current_room_id = None
	handle_leave_page(username)



@socket.on('dismiss_room')
def on_dismiss_room(room_id):
	room = all_rooms[roome_id]
	success, ret = room.close()
	if success:
		print(f'{room_id} is dismisssed now')
		for user in ret:
			handle_leave_room(user, room_id)
	else:
		send(ret)

# @socket.on('leave_room')
# def on_leave_room(msg):
# 	msg_decoded = json.loads(msg)
# 	username = msg_decoded['username']
# 	user = all_users[username]
# 	room_id = user.current_room_id
# 	# for clientjs go to room
# 	if not ('room' in msg_decoded and msg_decoded['room'] == room_id):
# 		if room_id:
# 			print(f'{username} leaving {room_id}')
# 			success, ret = all_rooms[room_id].remove(username)
# 			if success:
# 				# print(f'{username} left {room_id}, remaining members:', ret)
# 				handle_leave_room(username, room_id)
# 			else:
# 				send(ret)


#---------------messaging------------------------
@socket.on('message')
def handleMessage(msg):
	# print(msg)
	msg_decoded = json.loads(msg)
	username = msg_decoded["username"]
	# msg = msg_decoded["msg"]
	user = all_users[username]
	room_id = user.current_room_id
	msg_decoded["room"] = room_id
	send(json.dumps(msg_decoded), room=room_id)

# @socket.on('send_msg')
# def send_message(msg):
# 	print(request.sid, "sent:", msg["msg"])
# 	send(msg["msg"], room=msg["room"])

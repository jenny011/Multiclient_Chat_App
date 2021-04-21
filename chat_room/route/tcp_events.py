import json
from flask import Flask, request, jsonify, session, flash
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_cors import CORS
import chat_room
from .utils import *
from ..model.user import *
from ..model.room import *
import time
from datetime import datetime


###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
#---------------connection----------------------------
@socket.on('connect')
def on_connect():
	print("Connect")

@socket.on('say_hi')
@login_required
def say_hi(username):
	if current_user.id == username:
		current_user.update_sid(request.sid)
		print(username, current_user.sid)
		for room_id in current_user.rooms.keys():
			join_room(room_id)
		broadcastStatusChange(current_user, "active")

@socket.on('disconnect')
def on_disconnect():
	print("Disconnect")
	current_user.current_room_id = None
	return redirect(url_for('public'))


#------------invite, join----------------------

@socket.on('invite')
def on_invite(msg):
	msg = json.loads(msg)
	username = msg['username']
	user_ids = msg['users']
	roomname = msg['room']
	room_id = ""
	for user_id in user_ids:
		if not active_users[user_id]:
			emit('refreshUser', user_id)
			return
	if not room_id:
		#f'{username}, {user_id}'
		room_id = create_room(roomname, [username], len(user_ids) + 1)
		if not room_id:
			send(f'You can only create a room with {room_member_limit} users')
			return
		if not roomname:
			all_rooms[room_id].name = room_id
	else:
		if all_rooms[room_id].is_full():
			send('Room is full')
			return
	# Add user A
	handle_add_room(username, room_id)
	handle_join_room(username, room_id)
	# Tell user B
	for user_id in user_ids:
		ret = {"msg": f'{username} invited you to join room {roomname}', "username": username, "room": room_id}
		emit("client_invited", json.dumps(ret), room=all_users[user_id].sid)

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
			send('Room is full')
			return
		print(f'{username} joining {room_id}')
		success, ret = all_rooms[room_id].add(username)
		if success:
			print(f'{room_id} members:', ret)
			handle_add_room(username, room_id)
		else:
			send(ret)
	else:
		emit('refreshRoom', room_id)


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
		print(ret)

@socket.on('leave_page')
def on_leave_page(username):
	user = all_users[username]
	#user.current_room_id = None
	handle_leave_page(username)

@socket.on('set_inactive')
def on_set_inactive(username):
	user = all_users[username]
	room_id = user.current_room_id
	user.leave_page()
	active_users[username] = False
	broadcastStatusChange(user, "inactive")
	disconnect()

@socket.on('dismiss_room')
def on_dismiss_room(room_id):
	room = all_rooms[roome_id]
	success, ret = room.close()
	if success:
		print(f'{room_id} is dismisssed now')
		for user in ret:
			handle_leave_room(user, room_id)
	else:
		print(ret)

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
	room_id = current_user.current_room_id
	if room_id:
		msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		msg_decoded["room"] = room_id
		msg_decoded["time"] = msg_time
		target = msg_decoded["target"]
		if target and not all_rooms[room_id].is_member(target):
			target = ""
			msg_decoded["target"] = ""
		processed_msg = json.dumps(msg_decoded)
		if target:
			send(processed_msg, room=all_users[target].sid)
			send(processed_msg, room=current_user.sid)
		else:
			send(processed_msg, room=room_id)
		#--------record-------
		handle_record_msg(room_id, processed_msg)

@socket.on('fetch_history')
def on_fetch_history(msg):
	#msg: username, room, boundary, count
	#每次返回10条历史记录
	msg_decoded = json.loads(msg)
	username = msg_decoded["username"]
	room_id = msg_decoded["room"]
	boundary = msg_decoded["boundary"]
	pointer = msg_decoded["pointer"]
	handle_fetch_msg(username, room_id, boundary, pointer)

# @socket.on('send_msg')
# def send_message(msg):
# 	print(request.sid, "sent:", msg["msg"])
# 	send(msg["msg"], room=msg["room"])

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
	if not room_id:
		#f'{username}, {user_id}'
		room_id = create_room(roomname, [username])
		if not roomname:
			all_rooms[room_id].name = room_id
	else:
		if all_rooms[room].is_full():
			send('too many people in this room')
		# if user_id in all_rooms[room_id]:
		# 	send('user already in this room')
	# Add user A
	handle_add_room(username, room_id)
	handle_join_room(username, room_id)
	# Tell user B
	for user_id in user_ids:
		ret = {"msg": f'{username} invited you to join room {room_id}', "username": username, "room": room_id}
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
		print(ret)

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
		print(ret)

@socket.on('fetch_history')
def on_fetch_history(msg):
	#msg: username, room, boundary, count
	#每次返回10条历史记录
	username = msg["username"]
	room_id = msg["room"]
	boundary = msg["boundary"]
	count = msg["count"]
	handle_fetch_msg(username, room_id, boundary, count)

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
	msg_decoded["room"] = room_id
	target = msg_decoded["target"]
	if target:
		send(json.dumps(msg_decoded), room=all_users[target].sid)
		send(json.dumps(msg_decoded), room=current_user.sid)
	else:
		# msg = msg_decoded["msg"]
		send(json.dumps(msg_decoded), room=room_id)
	#--------record-------
	Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
	handle_record_msg(room_id, username, target, Time, msg)
	print(all_rooms[room_id].msg)
	#---------------------

# @socket.on('send_msg')
# def send_message(msg):
# 	print(request.sid, "sent:", msg["msg"])
# 	send(msg["msg"], room=msg["room"])

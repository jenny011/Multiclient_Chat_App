from flask import Flask, send_from_directory, render_template, redirect, url_for, json, jsonify, make_response
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
import chat_room
from datetime import datetime
from ..model.user import *
from ..model.room import *

DATETIME_FORMAT="%Y-%m-%d %H:%M"

@login.user_loader
def load_user(username):
    return all_users[username]

def get_all_rooms():
    rooms = []
    for room_id, room in all_rooms.items():
        rooms.append({"id": room_id, "name": room.name})
    return rooms

def get_all_rooms_except_mine(username):
    user = all_users[username]
    rooms = []
    for room_id, room in all_rooms.items():
        if room_id not in user.rooms.keys():
            rooms.append({"id": room_id, "name": room.name})
    return rooms

def get_all_rooms_and_users():
    rooms = []
    for room_id, room in all_rooms.items():
        rooms.append({"id": room_id, "name": room.name, "users":", ".join(room.members)})
    return rooms

def get_active_users(username):
    users = []
    for user, status in active_users.items():
        if status and user != username:
            users.append(user)
    return users

#------create, join, leave------
def create_room(room_name, users):
    if available_room_ids:
        room_id = available_room_ids.pop(0)
    else:
        room_id = str(chat_room.next_room_id)
        chat_room.next_room_id += 1
    new_room = Room(room_name, room_id, users)
    all_rooms[room_id] = new_room
    return room_id

def handle_join_room(username, room_id):
    user = all_users[username]
    user.join_room(room_id)
    #----fetch history----
    boundary = all_rooms[room_id].get_msg_length()-1
    handle_fetch_msg(username, room_id, boundary, 0)
    #---------------------
    ret = {"username": username, "room": room_id, "roomname": all_rooms[room_id].get_name()}
    emit("client_joined", json.dumps(ret), room=user.sid)


def handle_switch_room(username, room_id):
    user = all_users[username]
    if user.current_room_id:
        user.leave_page()
    user.join_room(room_id)
    ret = {"username": username, "room": room_id, "roomname": all_rooms[room_id].get_name()}
    emit("client_joined", json.dumps(ret), room=user.sid)

def handle_leave_page(username):
    user = all_users[username]
    all_users[username].leave_page()
    emit("client_left", username, room=user.sid)

def handle_add_room(username, room_id):
    join_room(room_id)
    all_users[username].add_room(room_id, datetime.now())
    ret = {"username": username, "room": room_id}
    emit("client_added", json.dumps(ret), room=room_id)

def handle_leave_room(username, room_id):
    if username in all_users:
        all_users[username].leave_room(room_id)
    emit("client_removed", username, room=room_id)
    leave_room(room_id)

def handle_record_msg(room_id, sender, receiver, time, message):
    room = all_rooms[room_id]
    room.record_msg(sender, receiver, time, message)
    return

def handle_fetch_msg(username, room_id, boundary, count):
    ###send msg boundary
	if boundary <= 10:
		chat_history = all_rooms[room_id].fetch_msg(0, boundary)
	else:
		chat_history = all_rooms[room_id].fetch_msg(boundary-count-10, boundary-count)
	ret = {"msg": chat_history, "boundary": boundary}
	send(json.dumps(ret), room=all_users[username].sid)



###
# def handle_join_room(username, room_id):
#     all_users[username].join_room(room_id)
#
# def handle_add_room(username, room_id, target_user=None):
#     join_room(room_id)
#     all_users[username].join_room(room_id)
#     if target_user:
#         all_users[user].join_room(room_id)
#     all_rooms[room_id].join(username)
#     emit("client_joined", {"msg": f'{username} joined', "room": room_id}, room=room_id)
#
# def handle_leave_page(username, room_id):
#     all_users[username].leave_page(room_id)
#     emit("client_left", f'{username} left this page', room=room_id)
#
#
# def handle_leave_room(username, room_id):
#     leave_room(room_id)
#     if username in all_users:
#         all_users[username].leave_room(room_id)
#
#     emit("client_left", f'{username} left', room=room_id)

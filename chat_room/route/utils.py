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

def get_active_users_in_room(room_id):
    users = []
    for user in all_rooms[room_id].members:
        if active_users[user]:
            users.append(user)
    return users

#------create, join, leave------
def create_room(room_name, users, user_number):
    if user_number > room_member_limit:
        return ""
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
    msg_history_len = len(all_rooms[room_id].msg)
    if msg_history_len < 10:
        last_ten_msgs = all_rooms[room_id].msg
    else:
        last_ten_msgs = all_rooms[room_id].msg[msg_history_len-10 : ]
    ret = {"username": username, "room": room_id, "roomname": all_rooms[room_id].name, "active_users": get_active_users_in_room(room_id), "boundary": msg_history_len, "last_ten_msgs": last_ten_msgs}
    emit("client_joined", json.dumps(ret), room=room_id)

def handle_switch_room(username, room_id):
    user = all_users[username]
    old_room_id = user.current_room_id
    if old_room_id:
        user.leave_page()
        emit("client_left", username, room=old_room_id)
    user.join_room(room_id)
    msg_history_len = len(all_rooms[room_id].msg)
    if msg_history_len < 10:
        last_ten_msgs = all_rooms[room_id].msg
    else:
        last_ten_msgs = all_rooms[room_id].msg[msg_history_len-10 : ]
    ret = {"username": username, "room": room_id, "roomname": all_rooms[room_id].name, "active_users": get_active_users_in_room(room_id), "boundary": msg_history_len, "last_ten_msgs": last_ten_msgs}
    emit("client_joined", json.dumps(ret), room=room_id)

def handle_leave_page(username):
    user = all_users[username]
    room_id = user.current_room_id
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

def handle_record_msg(room_id, message):
    room = all_rooms[room_id]
    room.record_msg(message)

def handle_fetch_msg(username, room_id, boundary, pointer):
    ###send msg boundary
    if boundary <= 10:
        chat_history = all_rooms[room_id].fetch_msg(0, boundary)
    else:
        ptr2 = boundary-pointer
        ptr1 = ptr2-10
        if ptr1 < 0:
            ptr1 = 0
        chat_history = all_rooms[room_id].fetch_msg(ptr1, ptr2)
    ret = {"history": chat_history, "boundary": boundary}
    print(ret)
    emit("history", json.dumps(ret), room=all_users[username].sid)

def broadcastStatusChange(user, status):
    for room in user.rooms.keys():
        emit(f'client_{status}', json.dumps({"username": user.id, "room": room, "active_users": get_active_users_in_room(room)}), room=room)


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

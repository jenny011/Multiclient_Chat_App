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

@login.unauthorized_handler
def unauthorized_callback():
       return redirect(url_for('goToLogin'))

@login.user_loader
def load_user(username):
    if username in all_users:
        return all_users[username]
    return None

def get_all_rooms():
    rooms = []
    for room_id, room in all_rooms.items():
        rooms.append({"id": room_id, "name": room.name})
    return rooms

def get_all_rooms_except_mine(username):
    user = all_users[username]
    rooms = []
    for room_id, room in all_rooms.items():
        if room_id not in user.rooms.keys() and not room.private and not room.is_full():
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

def get_my_last_ten_msgs(username, room_id, msg_history_len):
    room = all_rooms[room_id]
    last_ten_msgs = []
    ptr = msg_history_len - 1
    n_msgs = 0
    while ptr >= 0 and n_msgs < 10:
        this_msg = json.loads(room.msg[ptr])
        if this_msg["username"] == username or this_msg["target"] == username or not this_msg["target"]:
            last_ten_msgs.append(room.msg[ptr])
            n_msgs += 1
        ptr -= 1
    last_ten_msgs.reverse()
    return last_ten_msgs


#---------create, add---------
def create_room(room_name, username, users, user_number, private_chat):
    if user_number > room_member_limit:
        return ""
    if available_room_ids:
        room_id = available_room_ids.pop(0)
    else:
        room_id = str(chat_room.next_room_id)
        chat_room.next_room_id += 1
    new_room = Room(room_name, room_id, username, users, private_chat)
    all_rooms[room_id] = new_room
    return room_id

def handle_add_room(username, room_id):
    join_room(room_id)
    all_users[username].add_room(room_id, datetime.now())
    ret = {"username": username, "room": room_id}
    emit("client_added", json.dumps(ret), room=room_id)


#-------join, switch, leave------
def handle_join_room(username, room_id):
    user = all_users[username]
    user.join_room(room_id)

    room = all_rooms[room_id]
    msg_history_len = len(room.msg)
    last_ten_msgs = []
    if msg_history_len > 0:
        last_ten_msgs = get_my_last_ten_msgs(username, room_id, msg_history_len)

    ret = {"username": username, "room": room_id, "roomname":room.name, "private_chat":room.private, "active_users":get_active_users_in_room(room_id), "boundary": msg_history_len-1, "last_ten_msgs": last_ten_msgs}
    emit("client_joined", json.dumps(ret), room=room_id)

def handle_switch_room(username, room_id):
    user = all_users[username]

    room = all_rooms[room_id]
    msg_history_len = len(room.msg)
    last_ten_msgs = []
    if msg_history_len > 0:
        last_ten_msgs = get_my_last_ten_msgs(username, room_id, msg_history_len)

    old_room_id = user.current_room_id
    if old_room_id:
        user.leave_page()
        emit("client_left", username, room=old_room_id)
    user.join_room(room_id)

    ret = {"username":username, "room":room_id, "roomname":room.name, "private_chat":room.private, "active_users":get_active_users_in_room(room_id), "boundary": msg_history_len-1, "last_ten_msgs": last_ten_msgs}
    emit("client_joined", json.dumps(ret), room=room_id)

def handle_leave_page(username):
    user = all_users[username]
    room_id = user.current_room_id
    all_users[username].leave_page()
    emit("client_left", username, room=user.sid)


#-------remove--------
def handle_leave_room(username, room_id):
    if username in all_users:
        all_users[username].leave_room(room_id)
    emit("client_removed", json.dumps({'username':username, 'room':room_id}), room=room_id)
    leave_room(room_id)


#-------chat history------
def handle_record_msg(room_id, message):
    room = all_rooms[room_id]
    room.record_msg(message)

def handle_fetch_msg(username, room_id, boundary, ptr1, ptr2, direction):
    chat_history, ptr1, ptr2 = all_rooms[room_id].fetch_msg(username, boundary, ptr1, ptr2, direction)
    ret = {"history": chat_history, "boundary": boundary, "ptr1": ptr1, "ptr2": ptr2}
    emit("history", json.dumps(ret), room=all_users[username].sid)

def broadcastStatusChange(user, status):
    for room in user.rooms.keys():
        emit(f'client_{status}', json.dumps({"username": user.id, "room": room, "active_users": get_active_users_in_room(room)}), room=room)

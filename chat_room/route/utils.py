from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import chat_room
#from chat_room import app, socket, login, all_users, active_users, all_rooms
from chat_room.model.user import *
from chat_room.model.room import *
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

def get_all_rooms():
    return [room for room in all_rooms.keys()]

def get_active_users(username):
    users = []
    for user in active_users.keys():
        if user != username:
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
    all_rooms[new_room.id] = new_room
    return new_room

def handle_join_room(username, room_id, target_user=None):
    join_room(room_id)
    all_users[username].join_room(room_id)
    if target_user:
        all_users[user].join_room(room_id)
    emit("client_joined", {"msg": f'{username} joined', "room": room_id}, room=room_id)

def handle_leave_room(username, room_id):
    leave_room(room_id)
    if username in all_users:
        all_users[username].leave_room(room_id)
    emit("client_left", f'{username} left', room=room_id)

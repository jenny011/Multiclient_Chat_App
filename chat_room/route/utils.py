from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_socketio import SocketIO, send, emit, join_room, disconnect
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from chat_room import app, socket, login, all_users, active_users, active_rooms
from chat_room.model.models import *
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


def get_active_rooms():
    return [room for room in active_rooms.keys()]

def get_active_users(username):
    users = []
    for user in active_users.keys():
        if user != username:
            users.append(user)
    return users

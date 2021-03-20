from flask import Flask, request, json, jsonify, session, flash
from flask_socketio import SocketIO, send, emit, join_room, disconnect
from flask_cors import CORS
from chat_room import socket, all_users, active_users, active_rooms
from chat_room.route.utils import *
from chat_room.model.models import *


###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
###---------------------TCP events---------------------###
@socket.on('connect')
def on_connect():
	print("Hi", request.sid)

@socket.on('message')
def handleMessage(msg):
	print(request.sid, "sent:", msg)
	send(msg, broadcast=True)

@socket.on('disconnect')
def on_disconnect():
    print("Bye", request.sid)
    return redirect(url_for('public'))

@socket.on('join_room')
def on_disconnect(msg):
    user = msg['username']
    print("Hi", user)
	#TODO: add room to user, add user to room
	# active_users[user] = request.sid
    send(user + " joined", broadcast=True)

@socket.on('leave_room')
def on_disconnect(msg):
    user = msg['username']
    print("Bye", user)
	#TODO: remove user from room, remove room from user
    send(user + " left", broadcast=True)

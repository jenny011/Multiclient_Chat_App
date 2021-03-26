from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from chat_room import app, socket, login, all_users, active_users, all_rooms
from chat_room.model.user import *
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class Room:
    def __init__(self,room_name,ID,users):
        self.room_name = room_name
        self.room_ID = ID
        self.members = users
        self.number = len(users)
        self.status = True

    '''
    True: success
    False: member already in room
    1: room already closed
    2: room full
    '''
    def join(self, user):
        if self.status == False:
            print("room already closed")
            return 1
        if user not in self.members:
            if self.number == 5:
                return 2
            self.members.append(user)
            self.number += 1
        return True, self.members

    '''
    True: success
    False: error
    1: room close
    '''
    def leave(self, user):
        if user not in self.members:
            print("person already left")
            return False
        self.members.remove(user)
        self.number -= 1
        if self.number == 0:
            self.close_room()
            return 1
        return True, self.members

    def close(self):
        if self.status == False:
            print("room already closed")
            return False
        self.status = False
        return True


"""
if __name__ == "__main__":
    room1 = Room("Room1",1,"a","b")
    print(room1.members)
    print(room1.number)
    room1.join("c")
    print(room1.members)
    print(room1.number)
    room1.leave("a")
    print(room1.members)
    print(room1.number)
    print(room1.status)

    room1.leave("b")
    room1.leave("c")
    print(room1.members)
    print(room1.status)

    room1.join("a")
"""


# @socket.on('invite')
# #only invite one user at a time
# def on_invite(msg):
#     #attributes needed
#     if ID == "":
#         create_room(room_name, user1, user2)
#         send("successfully invited", broadcast = False)
#     else:
#
#         result, members = Room[ID].join_room(user2)
#         #members could be sent
#         if result == 1:
#             send("this room is already closed, please try another one", broadcast = False)
#         if result == False:
#             send("you are already in this room", broadcast = False)
#         if result == 2:
#             send("this room is already full", broadcast = False)
#         active_users[user] = request.sid
#         send(user + " joined", broadcast=True)


"""
@socket.on("create_room")
def on_create(msg):
    return
"""
"""
@socket.on("accept")
def on_accept(msg):
    return
"""


# @socket.on('join_room')
# def on_join(msg):
#     user = msg['username']
#     #ID needs to be fetched
#     result, members = ID.join_room(user)
#     #members could be sent
#     if result == 1:
#         send("this room is already closed, please try another one", broadcast = False)
#     if result == False:
#         send("you are already in this room", broadcast = False)
#     if result == 2:
#         send("this room is already full", broadcast = False)
#     active_users[user] = request.sid
#     send(user + " joined", broadcast=True)
#
# @socket.on('leave_room')
# def on_leave(msg):
#     user = msg['username']
#     result, members = ID.leave_room(user)
#     if result == False:
#         send("user already left", broadcast = False)
#     if result == 1:
#         send(user + " left," + "Room" + ID "closed", broadcast=True)
# 	active_users.pop(user)
# 	send(user + " left", broadcast=True)
#
# @socket.on('close_room')
# def on_close(msg):
# 	user = msg['username']
#     result = close_room(user)
#     if result == False:
#         send("Room" + ID + "already closed", broadcast = False)
# 	send("Room" + ID "closed", broadcast=True)
    #all users in this room need to be freed

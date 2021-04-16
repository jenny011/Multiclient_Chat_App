from flask import Flask, send_from_directory, render_template, redirect, url_for, json, jsonify, make_response
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_cors import CORS
import chat_room
from .user import *

room_member_limit = 5

class Room:
    def __init__(self, name, id, users, limit=room_member_limit):
        self.name = name
        self.id = id
        self.members = users
        self.number = len(users)
        self.status = True
        self.private = False
        self.limit = limit
        self.msg = []

    def get_name(self):
        return self.name

    def get_msg_length(self):
        return len(self.msg)

    def is_full(self):
        return self.number >= self.limit

    def is_member(self, username):
        return username in self.members

    '''True/False, detailed msg'''
    def add(self, user):
        if self.status == False:
            return False, "Room closed"
        if user not in self.members:
            if self.number == 5:
                return False, "Room full"
            self.members.append(user)
            self.number += 1
        return True, self.members

    '''True/False, detailed msg'''
    def remove(self, user):
        if user not in self.members:
            return False, "User already left"
        # JENNY: DEBUG
        self.members.remove(user)
        self.number -= 1
        if self.number == 0:
            self.close()
            return True, "All users left, room closed"
        return True, self.members

    def close(self):
        if self.status == False:
            return False, "Room already closed"
        self.status = False
        chat_room.all_rooms.pop(self.id)
        chat_room.available_room_ids.append(self.id)
        return True, "Room closed successfully"

    def record_msg(self, sender, receiver, time, message):
        self.msg.append((sender, receiver, time, message))
        #print(self.msg)
        return

    def fetch_msg(self, ptr1, ptr2):
        result = self.msg[ptr1:ptr2]
        return result


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
#     if id == "":
#         create_room(room_name, user1, user2)
#         send("successfully invited", broadcast = False)
#     else:
#
#         result, members = Room[id].join_room(user2)
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
#     #id needs to be fetched
#     result, members = id.join_room(user)
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
#     result, members = id.leave_room(user)
#     if result == False:
#         send("user already left", broadcast = False)
#     if result == 1:
#         send(user + " left," + "Room" + id "closed", broadcast=True)
# 	active_users.pop(user)
# 	send(user + " left", broadcast=True)
#
# @socket.on('close_room')
# def on_close(msg):
# 	user = msg['username']
#     result = close_room(user)
#     if result == False:
#         send("Room" + id + "already closed", broadcast = False)
# 	send("Room" + id "closed", broadcast=True)
    #all users in this room need to be freed

from flask import Flask, send_from_directory, render_template, redirect, url_for, json, jsonify, make_response
from flask_socketio import SocketIO, send, emit, disconnect, join_room, leave_room
from flask_cors import CORS
import chat_room
from .user import *

room_member_limit = 5

class Room:
    def __init__(self, name, id, users, private_chat, limit=room_member_limit):
        self.name = name
        self.id = id
        self.members = users
        self.number = len(users)
        self.status = True
        self.private = private_chat
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

    def record_msg(self, message):
        self.msg.append(message)
        return

    def fetch_msg(self, username, boundary, ptr1, ptr2, direction):
        n_msgs = 0
        result = []
        if direction == "prev":
            ptr2 = ptr1 + 1
            while n_msgs < 10 and ptr1 >= 0:
                this_msg = json.loads(self.msg[ptr1])
                if this_msg["username"] == username or this_msg["target"] == username or not this_msg["target"]:
                    result.append(self.msg[ptr1])
                    n_msgs += 1
                ptr1 -= 1
            result.reverse()
        elif direction == "next":
            ptr1 = ptr2 - 1
            while n_msgs < 10 and ptr2 <= boundary:
                this_msg = json.loads(self.msg[ptr2])
                if this_msg["username"] == username or this_msg["target"] == username or not this_msg["target"]:
                    result.append(self.msg[ptr2])
                    n_msgs += 1
                ptr2 += 1
        return result, ptr1, ptr2

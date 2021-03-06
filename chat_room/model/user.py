from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from chat_room import *

class User(UserMixin):
    def __init__(self, username, password, current_room_id=None):
        self.id = username
        self.password = self.set_password(password)
        # roomID -> time
        self.rooms = {}
        self.current_room_id = current_room_id
        self.sid = None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_sid(self, sid):
        self.sid = sid

    # open a chat interface
    def join_room(self, room_id):
        self.current_room_id = room_id

    def add_room(self, room_id, t):
        print("join", self.id, room_id, self.current_room_id, self.rooms)
        self.rooms[room_id] = t

    def leave_room(self, room_id):
        if self.current_room_id == room_id:
            print("leave", self.id, room_id, self.current_room_id, self.rooms)
            self.current_room_id = None
            self.rooms.pop(room_id)

    # leave the current chat interface, don't remove myself from the chat room
    def leave_page(self):
        self.current_room_id = None


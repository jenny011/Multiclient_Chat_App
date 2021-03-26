from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from chat_room import *

@login.user_loader
def load_user(username):
    return all_users[username]

class User(UserMixin):
    def __init__(self, username, password, rooms={}, current_room_id=None):
        self.id = username
        self.password = self.set_password(password)
        # roomID -> msg queue
        self.rooms = rooms
        self.current_room_id = current_room_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # open a chat interface (get all the buffered msgs)
    def join_room(self, room_id):
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.current_room_id = room_id

    # leave the current chat interface, don't remove myself from the chat room
    def leave_room(self, room_id):
        if self.current_room_id == room_id:
            self.current_room_id = None

    # buffer a msg if room_id != current_room_id
    def enqueue_msg(room_id, msg):
        self.rooms[room_id].append(msg)

    def dequeue_msg(room_id):
        for msg in self.rooms[room_id]:
            yield msg

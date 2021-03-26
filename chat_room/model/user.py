from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from chat_room import *

@login.user_loader
def load_user(username):
    return all_users[username]

class User(UserMixin):
    def __init__(self, username, password, rooms=[]):
        self.id = username
        self.password = self.set_password(password)
        # a list of room ids which the user is in
        self.rooms = rooms

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def join_room(self, room):
        self.rooms.append(room)
        return True

    def leave_room(self, room):
        self.rooms.remove(room)
        return True

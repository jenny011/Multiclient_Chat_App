from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from chat_room import login, registered_users

@login.user_loader
def load_user(username):
    return registered_users[username]

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = self.set_password(password)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

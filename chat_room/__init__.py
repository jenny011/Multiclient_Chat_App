from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_socketio import SocketIO, send, emit, join_room, disconnect
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = '65rdxchu87'
app.host = 'localhost'
app.debug = True
CORS(app, supports_credentials=True)

login = LoginManager(app)
login.login_view = 'login' # force user to login
login.login_message = "Please login first"

socket = SocketIO(app, cors_allowed_origins="*")


###---------------------data store---------------------###
###---------------------data store---------------------###
###---------------------data store---------------------###
# username -> User object
all_users = {}
# roomid -> room object
count = 0
all_rooms = {}
# [online usernames]
active_users = {}


from chat_room.model.user import *
from chat_room.model.room import *
from chat_room.route import http_reqs, tcp_events, utils

for i in range(10):
	id = str(i)
	all_users[id] = User(id, id)


# if __name__ == '__main__':
#     socket.run(app, host="127.0.0.1", port=5000)

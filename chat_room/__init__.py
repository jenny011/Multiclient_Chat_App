from flask import Flask, send_from_directory, render_template, redirect, url_for, json, jsonify, make_response
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
# next available room ID
next_room_id = 0
# a queue of available room IDs (str) released by closed rooms
available_room_ids = []
# roomID -> room object
all_rooms = {}
# username -> ?
active_users = {}


from .model import user, room
from .route import http_reqs, tcp_events, utils


for i in range(10):
	username = str(i)
	all_users[username] = user.User(username, username)


# if __name__ == '__main__':
#     socket.run(app, host="127.0.0.1", port=5000)

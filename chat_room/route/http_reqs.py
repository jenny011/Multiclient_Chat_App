from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, make_response
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import chat_room
from .utils import *
from ..model.user import *
from ..model.room import *


###---------------------HTTP routes---------------------###
###---------------------HTTP routes---------------------###
###---------------------HTTP routes---------------------###
#---go to login page---
@app.route('/')
def public():
	return render_template('index.html')

@app.route('/goToRegister', methods=['GET'])
def goToRegister():
    return render_template('register.html')

@app.route('/goToLogin', methods=['GET'])
def goToLogin():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username in all_users:
        return render_template('register.html', err='Username already exists!')
    new_user = User(username, password)
    all_users[username] = new_user
    print(all_users.keys())
    return render_template('login.html')

#---go to entrance page---
@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	if username not in active_users:
		password = request.form['password']
		user = all_users[username]
		if not user:
			return render_template('register.html', err='Please register!')
		if not user.check_password(password):
			return render_template('login.html', err="Username and password don't match!")
		login_user(user)
		active_users[username] = True
		return redirect(url_for("chat"))
	elif current_user.is_authenticated:
		return redirect(url_for("chat"))
	else:
		active_users.pop(username)
		return render_template('login.html', err="Unknown error")

@app.route('/chat', methods=['GET'])
@login_required
def chat():
	username = current_user.id
	room_ids = get_all_rooms()
	user_ids = get_active_users(username)
	return render_template('interface.html', username=username, rooms=room_ids, users=user_ids)

@app.route('/updateLists', methods=['GET'])
@login_required
def update_lists():
	username = current_user.id
	room_ids = get_all_rooms()
	user_ids = get_active_users(username)
	return make_response(jsonify({"rooms": room_ids, "users": user_ids}), 200)

#---go to chat page---
@app.route('/add_to_room', methods=['POST'])
@login_required
def chat_room():
	room_id = request.form['room']
	username = current_user.id
	room = all_rooms[target_room_id]
	room.join(username)
	all_users[username].join_room(room_id)
	print(username, current_user.rooms)
	socket.emit('display_room', jsonify([{"name": room.name, "users": ",".join(room.members)}]))
	return 0
	# return render_template('interface.html', username=username, target_room=target_room_id, target_user="")


@app.route('/invite_user', methods=['POST'])
@login_required
def chat_user():
	user_id = request.form['user']
	username = current_user.id
	print(username, current_user.rooms)
	socket.emit('add_room_invitation', jsonify())
	return 0
	# return render_template('interface.html', username=username, target_user=target_user_id, target_room="")




#---leave_room---
@app.route('/leave_room', methods=['GET'])
@login_required
def leave_room():
	return redirect(url_for("chat"))


#---log out---
@app.route('/logout', methods=['GET'])
@login_required
def logout():
	username = current_user.id
	if username in active_users:
		active_users.pop(username)
	logout_user()
	return redirect(url_for('public'))

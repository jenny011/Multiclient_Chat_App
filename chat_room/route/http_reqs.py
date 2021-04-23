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
	if current_user.is_authenticated:
		active_users[current_user.id] = True
		return redirect(url_for("chat"))
	return render_template('index.html')

@app.route('/goToRegister', methods=['GET'])
def goToRegister():
    return render_template('register.html')

@app.route('/goToLogin', methods=['GET'])
def goToLogin():
    return render_template('login.html')


#---register, login---
@app.route('/register', methods=['POST'])
def register():
	if current_user.is_authenticated:
		active_users[current_user.id] = True
		return redirect(url_for("chat"))
	else:
		username = request.form['username']
		password = request.form['password']
		if username in all_users:
			return render_template('register.html', err='Username already exists!')
		new_user = User(username, password)
		all_users[username] = new_user
		print(all_users.keys())
		active_users[username] = False
	return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	if current_user.is_authenticated:
		active_users[current_user.id] = True
		return redirect(url_for("chat"))
	else:
		if username in all_users and not active_users[username]:
			password = request.form['password']
			user = all_users[username]
			if not user:
				return render_template('register.html', err='Please register!')
			if not user.check_password(password):
				return render_template('login.html', err="Username and password don't match!")
			login_user(user)
			active_users[username] = True
			return redirect(url_for("chat"))
		else:
			if username in active_users:
				active_users[username] = False
				return render_template('login.html', err="Unknown error, try again")
			else:
				return render_template('login.html', err="Please register!")



#----chat interface----
@app.route('/chat', methods=['GET'])
@login_required
def chat():
	username = current_user.id
	return render_template('interface.html', username=username)

@app.route('/updateLists', methods=['GET'])
@login_required
def update_lists():
	username = current_user.id
	room_ids = get_all_rooms_except_mine(username)
	user_ids = get_active_users(username)
	return make_response(jsonify({"rooms": room_ids, "users": user_ids}), 200)

@app.route('/updateMyRooms', methods=['GET'])
@login_required
def update_my_rooms():
	user = all_users[current_user.id]
	rooms = []
	for k in user.rooms.keys():
		room = all_rooms[k]
		current = k == user.current_room_id
		rooms.append({'id': k, 'name': room.name, 'users': ", ".join(room.members), 'current':current})
	return make_response(jsonify(rooms), 200)


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
		active_users[username] = False
	logout_user()
	return redirect(url_for('public'))

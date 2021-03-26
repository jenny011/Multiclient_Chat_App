from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, session, flash, make_response
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from chat_room import app, login, all_users, active_users, all_rooms
from chat_room.route.utils import *
from chat_room.model.user import *
from chat_room.model.room import *
from flask_login import UserMixin


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
	password = request.form['password']
	user = all_users[username]
	if not user:
		return render_template('register.html', err='Please register!')
	if not user.check_password(password):
		return render_template('login.html', err="Username and password don't match!")
	login_user(user)
	active_users[username] = True
	rooms = get_all_rooms()
	users = get_active_users(username)
	return render_template('entrance.html', username=username, rooms=rooms, users=users)

@app.route('/updateLists', methods=['GET'])
@login_required
def update_lists():
	username = current_user.id
	rooms = get_all_rooms()
	users = get_active_users(username)
	return make_response(jsonify({"rooms": rooms, "users": users}))

#---go to chat page---
@app.route('/chat_room', methods=['POST'])
@login_required
def chat_room():
	target_room = request.form['target']
	username = current_user.id
	print(username, current_user.rooms)
	print("----Emit socket event: join a room----")
	return render_template('chat.html', username=username, target_room=target_room, target_user="")


@app.route('/chat_user', methods=['POST'])
@login_required
def chat_user():
    target_user = request.form['target']
    username = current_user.id
    #TODO
    print("----Emit socket event: create a room----")
    return render_template('chat.html', username=username, target_user=target_user, target_room="")

#---leave_chat---
@app.route('/leave_chat', methods=['GET'])
@login_required
def leave_chat():
	username = current_user.id
	rooms = get_all_rooms()
	users = get_active_users(username)
	return render_template('entrance.html', username=username, rooms=rooms, users=users)


#---log out---
@app.route('/logout', methods=['GET'])
@login_required
def logout():
	username = current_user.id
	active_users.pop(username)
	logout_user()
	return redirect(url_for('public'))

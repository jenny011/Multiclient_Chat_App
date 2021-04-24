# Multiclient Chat App
<b>Spring 2021 Computer Networking Course Project</b><br>
<b>Jingyi Zhu, Yannan Fei</b><br>
Github repository: <a href="https://github.com/jenny011/Multiclient_Chat_App">https://github.com/jenny011/Multiclient_Chat_App</a><br>
Presentation Video: <a></a>

## Please Note that
1. Python 3.6+ is required for the server to behave properly.<br>
2. Please logout of all the users when you halt the server.
All the data are stored at the server.
Once the server is stopped, the logged-in users remain logged-in.
Everything else happened in the app is erased.<br>
3. Safari and Firefox periodically drop inactive TCP connections after timeout.
If you find the chat interface not working (eg. messages not being sent, images not being displayed), please simply refresh the page.<br>
4. For a better user experience, please give the browser windows a reasonable size.<br>


## How to Install and Run our Multiclient Chat App

### (Optional, but recommended) Virtual Environment Setup
If you have Anaconda: <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html">Anaconda Python virtural environment</a></br>
In the terminal, run: <br>
`$ conda create -n myenv python=3` <br>
`$ conda activate myenv` <br>

### Install and run the server
#### Please use Python 3.6+.
1. Download this github repository as a folder `Multiclient_Chat_App`.</br>
2. In the terminal, go into the folder `Multiclient_Chat_App`.</br>
3. Run the commands: <br>
`$ export FLASK_APP=chat_room` <br>
`$ pip install -e .` <br>
`$ flask run` <br>

#### If the above installation does not work
`$ pip install` these packages: 'Flask', 'Flask-SocketIO', 'flask-login', 'flask-cors', 'numpy', 'Werkzeug' <br>
`$ python run.py` in folder `Multiclient_Chat_App` <br>

#### Run the server after installation
Run the commands in the folder `Multiclient_Chat_App`: <br>
`$ export FLASK_APP=chat_room` <br>
`$ flask run` <br>


### Run the clients
1. Open <b>ONE</b> browser per client (user).<br>
We recommend using Chrome, Chrome Incognito, Safari, Safari Incognito, Firefox and Firefox Incognito. <br>
Safari might not work when you run the app for the first time. In that case, you can restart the server.<br>
2. In each browser, go to `http://localhost:5000`. <br>


## Operating instructions —— How to Use the App
Our app requires users to register and then login.<br>
Our app periodically retrieves a list of available chat rooms and active users. It can detect out-of-date information in user requests and handle the requests gracefully.<br>
Our app saves the following chat status:<br>
1. the chat rooms which each user has joined
2. the chat history of all the chat rooms

### Register and login
1. Register users with unique username and password.
2. Login users.

### Chat Interface Elements and Functionalities
#### Left panel
1. `"logout" button`: <br>
Click the button to logout of the app.<br>
The user is not removed from any chat room on logout.<br>
2. `My chat rooms`: <br>
A list of the chat room which the user is in.<br>
The active room button has a white background and does not do anything when clicked.<br>
The user can click on a room to switch to the active chat room.<br>
Notifications are displayed for the rooms which he/she is not currently chatting in.<br>

#### Right panel
<b>`User Home version`:</b> A list of chat rooms and active users.<br>
1. The user can join an existing chat room if it is not full.<br>
2. The user can also create a new chat room with one or more active users and he/she must provide a room name.<br>
On room creation, the room can be set as private (only the users chosen can see and join it) or non-private (all users can see and join it).<br>
Rooms in the chat app has a size limit. A room can have at most 5 users. If a room is full, it will not be visible to the users in the `User Home`.<br>
A user will automatically join a chat room and switch to that chat room if someone else created a room with him/her.

<b>`Chat room version`:</b> A list of action buttons, a message display box and a message sending box.<br>
1. Private rooms have a "*" after the room name.<br>
2. `"search" button`: go to the `User Home Version`.<br>
3. `"chat history" button`: View chat histories that were sent before the user started chatting in the room.<br>
4. `"leave this room" button`: Remove the user him/herself from the chat room.<br>
5. `message display box`: where the messages are displayed. The messages with borders are private messages, otherwise, they are public messages of the chat room.<br>
6. `users dropdown menu`: The user can send public messages to everyone in the chat room by selecting "send to everyone" from the dropdown menu.<br>
The user can also send private messages to an active user in the chat room selected from the dropdown menu.<br>
7. `message text box`: The user can type in a message to be sent.<br>
8. `"send" button`: The user can send messages by clicking this button or tapping "enter" on the keyboard.<br>
9. `"emoji" button`: A modal of eight emojis is displayed after the button is clicked. The user can click on an emoji to end to the chat room publicly or privately (users dropdown menu also works here).<br>


## A List of Files —— The Structure of the `MultiClient_Chat_App` Folder
### Multiclient_Chat_App/
#### chat_room/
##### __init__.py
	Define all the variables for app, login-manager, socket and data storage.
##### model/
	1. room.py: the chat room object
	2. user.py: the user object
##### route/
	1. http_reqs.py: handle AJAX requests such as register and login.
	2. tcp_events.py: handle TCP events such as joining chat rooms and sending messages.
##### templates/
	1. index.html: entrance page
	2. register.html: register page
	3. login.html: login page
	4. interface.html: user home and chat interface page
##### static/
	1. client.js: client side of our application. Send AJAX requests, handle AJAX responses and handle TCP events. 
	2. model.js: HTML element generator 
	3. utils.js: utility functions
	4. interface.css: styling script for interface.html
	5. images/: a folder which stores the emojis
#### run.py
	Run the app.
#### setup.py
	Configuration and specify the packages to be pip installed.


## Thank you!


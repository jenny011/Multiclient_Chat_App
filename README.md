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
If you find the chat interface not working (eg. messages not being sent), please simply refresh the page.<br>
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


## How to Use the App (Operating instructions)
### Register and login
You can login with pre-registered users, username 1 to 10. Password is the same as username.<br>
You can also register your own user.<br>


### Chat Interface Functionalities
#### Left panel
1. `"logout" button`: <br>
Click the button to logout of the app.
The user is not removed from any chat room on logout.<br>
2. <i>My chat rooms:</i> <br>
A list of the chat room which the user is in.
The user can click on a room to switch the active chat room.
Notifications are displayed for the rooms which he/she is not currently chatting in.<br>

#### Right panel
<i><b>Entrance version:</b></i> A list of chat rooms and active users.<br>
1. The user can join an existing chat room if it is not full.<br>
2. The user can also create a new chat room with one or more active users and he/she must provide a room name.<br>
On room creation, the room can be set as private (only the users chosen can see and join it) or non-private (all users can see and join it).<br>
Rooms in the chat app has a size limit. A room can have at most 5 users.<br>

<i><b>Chat room version:</b></i> A list of action buttons, a message display box and a message sending box. <br>
1. <i>"search" button:</i> go to the entrance version.<br>
2. <i>"chat history" button:</i> view chat histories that were sent before the user started chatting in the room.<br>
3. <i>"leave this room" button:</i> remove the user him/herself from the room.<br>
4. <i>message display box:</i> where the messages are displayed. The messages with borders are private messages, otherwise, they are public messages of the chat room.<br>
5. <i>message sending box:</i> The user can select an active target user in the dropdown menu to send private messages to. The user can also send public messages to everyone in the chat room.<br>

## Thank you!

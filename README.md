#This is the main branch
Commit ONLY Jenny's updates and merged updates to the main branch

# Multiclient Chat App
Spring 2021 Computer Networking Course Project <br>
Jingyi Zhu, Yannan Fei

## Install and run the project
### Please use Python 3+. <br>
0. Create a Python virtual environment (Strongly recommend).
<a href="https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html">Anaconda Python virtural environment</a></br>
`$ conda create -n myenv python=3` <br>
`$ conda activate myenv` <br>
1. Download this github repository as a folder `Multiclient_Chat_App`.</br>
2. In the terminal, go into the folder `Multiclient_Chat_App`.</br>
`$ export FLASK_APP=chat_room` </br>
`$ pip install -e .` </br>
`$ flask run` <br>
#### If the above installation does not work
`$ pip install` these packages: 'Flask', 'Flask-SocketIO', 'flask-login', 'flask-cors', 'numpy', 'Werkzeug' <br>
`$ python run.py` in folder `Multiclient_Chat_App` <br>
### Please Note that
All the data are stored at the server. <br>
Once the server is stopped, everything happened in the app will be erased. <br>

## Use the app
### Open the app, register and login
Open ONE browser per user. </br> You can use Chrome, Chrome Incognito, Safari, Firefox, etc. <br>
Safari might not work when you run the app for the first time. In that case, you can restart the server.<br>
On each browser, go to `http://localhost:5000`. <br>
You can login with pre-registered users, username 1 to 10. Password is the same as username. <br>
You can also register your own user. <br>

### Funtionalities
#### Left panel
1. <i>"logout" button:</i> logout of the app. The use is not removed from any chat room.<br>
2. <i>My chat rooms:</i> a list of the chat room which the user is in. The user can click on a room to switch the right panel to that chat room. The user can also receive notifications for the rooms which he/she is not currently chatting in.<br>
#### Right panel
<i><b>Entrance version:</b></i> A list of chat rooms and active users. The user can create a new chat room with an active user and he/she must provide a room name. The user can join an existing chat instead. <br>
<i><b>Chat room version:</b></i> A list of action buttons, a message display box and a message sending box. <br>
1. <i>"search" button:</i> go to the entrance version. <br>
2. <i>"chat history" button:</i> view chat histories that were sent before the user started chatting in the room. <br>
3. <i>"leave this room" button:</i> remove the user him/herself from the room. <br>
4. <i>message display box:</i> where the messages are displayed. The messages with borders are private messages, otherwise, they are public messages of the chat room. <br>
5. <i>message sending box:</i> The user can select an active target user in the dropdown menu to send private messages to. The user can also send public messages to everyone in the chat room. <br>
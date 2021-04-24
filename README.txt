---------------------------------------------
 | Checkout Our Documentation on Github :) |
---------------------------------------------
We have prepared a more readble README.md on our Github page.
Github page: https://github.com/jenny011/Multiclient_Chat_App
It contains contents of both HOWTO.txt and README.txt.

---------------------
 |Please Note that |
---------------------
1. Please use Python 3.6+.
2. Please logout of all the users when you halt the server.
  All the data are stored at the server.
  Once the server is stopped, the logged-in users remain logged-in.
  Everything else happened in the app is erased.
3. Safari and Firefox periodically drop inactive TCP connections after timeout.
  If you find the chat interface not working (eg. messages not being sent), please simply refresh the page.
4. For a better user experience, please give the browser windows a reasonable size.

----------------------------------------------------------------------------------------
# Operating instructions —— How to Use the App #
Our app requires users to register and then login.
Our app periodically retrieves a list of available chat rooms and active users.
It can detect out-of-date information in user requests and handle the requests gracefully.
Our app saves the following chat status:
  1. the chat rooms which each user has joined
  2. the chat history of all the chat rooms

## Register and login ##
  1. Register users with unique username and password.
  2. Login users.

## Chat Interface Elements and Functionalities ##
### Left panel
1. `"logout" button`:
  Click the button to logout of the app.
  The user is not removed from any chat room on logout.
2. `My chat rooms`:
  A list of the chat room which the user is in.
  The active room button has a white background and does not do anything when clicked.
  The user can click on a room to switch the active chat room.
  Notifications are displayed for the rooms which he/she is not currently chatting in.

### Right panel
`User Home version`: A list of chat rooms and active users.
  1. The user can join an existing chat room if it is not full.
  2. The user can also create a new chat room with one or more active users and he/she must provide a room name.
    On room creation, the room can be set as private (only the users chosen can see and join it) or non-private (all users can see and join it).
    Rooms in the chat app has a size limit. A room can have at most 5 users. If a room is full, it will not be visible to the users in the `User Home`.
    A user will automatically join a chat room and switch to that chat room if someone else created a room with him/her.

`Chat room version`: A list of action buttons, a message display box and a message sending box.
  1. Private rooms have a "*" after the room name.
  2. `"search" button`: go to the `User Home Version`.
  3. `"chat history" button`: View chat histories that were sent before the user started chatting in the room.
  4. `"leave this room" button`: Remove the user him/herself from the chat room.
  5. `message display box`: where the messages are displayed. The messages with borders are private messages, otherwise, they are public messages of the chat room.
  6. `users dropdown menu`: The user can send public messages to everyone in the chat room by selecting "send to everyone" from the dropdown menu.
                        The user can also send private messages to an active user in the chat room selected from the dropdown menu.
  7. `message text box`: The user can type in a message to be sent.
  8. `"send" button`: The user can send messages by clicking this button or tapping "enter" on the keyboard.
  9. `"emoji" button`: A modal of eight emojis is displayed after the button is clicked.
                        The user can click on an emoji to end to the chat room publicly or privately (users dropdown menu also works here).

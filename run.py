from chat_room import app, socket

if __name__ == '__main__':
    socket.run(app, host="127.0.0.1", port=5000)

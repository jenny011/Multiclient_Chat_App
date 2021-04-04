from chat_room import app, socket

if __name__ == '__main__':
    socket.run(app, host="localhost", port=5000)

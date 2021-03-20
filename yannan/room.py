class Room:
    def __init__(self,room_name,ID,user1,user2):
        self.room_name = room_name
        self.room_ID = ID
        self.number = 2
        self.member = [user1,user2]
        self.status = True

    def join_room(self, user):
        if self.status == False:
            print("room already closed")
            return 1
        if user in self.member:
            return False
        if self.number = 5:
            return 2
        self.member.append(user)
        self.number+=1
        return True, self.member
        #True: success
        #False: member already in room
        #1: room already closed
        #2: room full

    def leave_room(self, user):
        if user not in self.member:
            print("person already left")
            return False
        self.member.remove(user)
        self.number -= 1
        if self.number == 0:
            self.close_room()
            return 1
        return True, self.member
        #True: success
        #False: error
        #1: room close

    def close_room(self):
        if self.status == False:
            print("room already closed")
            return False
        self.status = False
        return True

Room = {}
count = 0
def create_room(room_name,user1,user2):
    ID = count
    room = Room(room_name, ID, user1, user2)
    count += 1      
    Room[ID] = room
    count += 1
    return True


"""
if __name__ == "__main__":
    room1 = Room("Room1",1,"a","b")
    print(room1.member)
    print(room1.number)
    room1.join_room("c")
    print(room1.member)
    print(room1.number)
    room1.leave_room("a")
    print(room1.member)
    print(room1.number)
    print(room1.status)
    
    room1.leave_room("b")
    room1.leave_room("c")
    print(room1.member)
    print(room1.status)
    
    room1.join_room("a")
"""


@socket.on('invite')
#only invite one user at a time
def on_invite(msg):
    #attributes needed
    if ID == "":
        create_room(room_name, user1, user2)
        send("successfully invited", broadcast = False)
    else:
        
        result, members = Room[ID].join_room(user2)
        #members could be sent
        if result == 1:
            send("this room is already closed, please try another one", broadcast = False)
        if result == False:
            send("you are already in this room", broadcast = False)
        if result == 2:
            send("this room is already full", broadcast = False)
        active_users[user] = request.sid
        send(user + " joined", broadcast=True)


"""
@socket.on("create_room")
def on_create(msg):
    return
"""
"""
@socket.on("accept")
def on_accept(msg):
    return
"""


@socket.on('join_room')
def on_join(msg):
	user = msg['username']
    #ID needs to be fetched
    result, members = ID.join_room(user)
    #members could be sent
    if result == 1:
        send("this room is already closed, please try another one", broadcast = False)
    if result == False:
        send("you are already in this room", broadcast = False)
    if result == 2:
        send("this room is already full", broadcast = False)
    active_users[user] = request.sid
	send(user + " joined", broadcast=True)
    
@socket.on('leave_room')
def on_leave(msg):
	user = msg['username']
    result, members = ID.leave_room(user)
    if result == False:
        send("user already left", broadcast = False)
    if result == 1:
        send(user + " left," + "Room" + ID "closed", broadcast=True)
	active_users.pop(user)
	send(user + " left", broadcast=True)

@socket.on('close_room')
def on_close(msg):
	user = msg['username']
    result = close_room(user)
    if result == False:
        send("Room" + ID + "already closed", broadcast = False)
	send("Room" + ID "closed", broadcast=True)
    #all users in this room need to be freed
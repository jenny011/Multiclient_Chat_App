var socket = io.connect("http://localhost:5000");
var interval = 3000;

$(document).ready(function() {
  socket.on('connect', function(){
    socket.emit('say_hi', username);
    console.log("connected", username);
  });

  socket.on('reconnect', function(){
    socket.emit('say_hi', username);
    console.log("reconnected", username);
  });

  socket.on('disconnect', function(){
    clearInterval(refreshEntrance);
    socket.emit('leave_room', username);
  });

  //-----refresh entrance list-----
  sendRequest("updateLists", "GET", null, updateLists);
  var refreshEntrance = setInterval(sendRequest, interval, "updateLists", "GET", null, updateLists);

  $(".room-item").on("submit", joinRoom);
  $(".user-item").on("submit", inviteUser);

  //-----rooms list-----
  sendRequest("updateMyRooms", "GET", null, updateMyRooms);

  //-----messaging-----
  //---system messages---
  socket.on('client_invited', function(data) {
    let msg = JSON.parse(data);
    socket.emit('add_room', JSON.stringify({"username": username, "room": msg.room}));
    alert(msg.msg);
  });

  socket.on('client_joined', function(user){
    if (user == username) {
      clearInterval(refreshEntrance);
      sendRequest("updateMyRooms", "GET", null, updateMyRooms);
      $("#entrance-container").hide();
      $("#interface-container").show();
      $("#messages").empty();
    }
  });

  socket.on('client_left', function(user){
    if (user == username) {
      sendRequest("updateLists", "GET", null, updateLists);
      sendRequest("updateMyRooms", "GET", null, updateMyRooms);
      var refreshEntrance = setInterval(sendRequest, interval, "updateLists", "GET", null, updateLists);
      $("#entrance-container").show();
      $("#interface-container").hide();
      $("#messages").empty();
    }
  });

  socket.on('client_added', function(msg){
    let msg_decoded = JSON.parse(msg);
    let user = msg_decoded.username;
    if (user == username) {
      socket.emit('join_room', msg);
      sendRequest("updateMyRooms", "GET", null, updateMyRooms);
    } else {
      let displayMsg = replaceSymbols(user) + " joined";
      $("#messages").append('<div class="system-msg"><i>' + displayMsg + '</i></div>');
    }
    $("#msg-container").animate({ scrollTop: $('#msg-container').prop("scrollHeight") }, 1000);
  });

  socket.on('client_removed', function(user){
    if (user == username) {
      sendRequest("updateLists", "GET", null, updateLists);
      sendRequest("updateMyRooms", "GET", null, updateMyRooms);
      var refreshEntrance = setInterval(sendRequest, interval, "updateLists", "GET", null, updateLists);
      $("#interface-container").hide();
      $("#entrance-container").show();
      $("#messages").empty();
    } else {
      let displayMsg = replaceSymbols(user) + " left";
      $("#messages").append('<div class="system-msg"><i>' + displayMsg + '</i></div>');
    }
    $("#msg-container").animate({ scrollTop: $('#msg-container').prop("scrollHeight") }, 1000);
  });

  //---user messages---
  socket.on('message', function(msg){
    let myMsg = JSON.parse(replaceSymbols(msg));
    if (myMsg.username == username) {
      $("#messages").append(rightMsg(myMsg.username, myMsg.msg));
    }  else {
      $("#messages").append(leftMsg(myMsg.username, myMsg.msg));
    }
    $("#msg-container").animate({ scrollTop: $('#msg-container').prop("scrollHeight") }, 1000);
  });

  socket.on('refresh', function(room_id){
    alert("Room " + room_id + " has been dismissed.");
    sendRequest("updateLists", "GET", null, updateLists);
    sendRequest("updateMyRooms", "GET", null, updateMyRooms);
  })

  $("#sendBtn").on("click", function(event){
    event.preventDefault();
    let msgText = $('#myMsg').val();
    if (msgText) {
      let msg = {"username": username, "msg": msgText}
      socket.send(JSON.stringify(msg));
      // socket.emit("send_msg", {'msg': msg, 'room': target_room});
      $('#myMsg').val('');
    }
  });

  //-----leave-----
  $("#leave_room").on("click", function(){
    socket.emit("leave_room", username);
  });

  $("#logout").on("click", function(){
    //socket.emit("leave_room", {'username': username, 'room': target_room});
    // socket.emit("leave_room", JSON.stringify({'username':username}));
    socket.disconnect();
  });

  //-----leave-----
  $("#search").on("click", function(){
    socket.emit("leave_page", username);
  });
});


$(document).keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      event.preventDefault();
      $("#sendBtn").click();
    }
});


function updateLists(data) {
  $("#rooms").empty();
  $("#users").empty();
  for (let i=0; i<data['rooms'].length; i++) {
    let id = data['rooms'][i]['id'];
    $("#rooms").append(roomsList(id, data['rooms'][i]['name']));
    $("#room-id-"+id).submit(joinRoom);
  }
  for (let i=0; i<data["users"].length; i++) {
    let id = data['users'][i];
    $("#users").append(usersList(id));
    $("#user-id-"+id).submit(inviteUser);
  }
};

function joinRoom(event){
  event.preventDefault();
  let data = $(this).serializeArray();
  let msg = {'username': username, 'room': data[0].value};
  socket.emit('add_room', JSON.stringify(msg));
}

function inviteUser(event) {
  event.preventDefault();
  let data = $(this).serializeArray();
  let msg = {'username': username, 'user': data[0].value, 'room': ""};
  socket.emit('invite', JSON.stringify(msg));
}

function updateMyRooms(data) {
  $("#chats").empty();
  for (let i=0; i<data.length; i++) {
    if (data[i].current) {
      $("#chats").append(active_chatbox(data[i].id, data[i].name, data[i].users));
    } else {
      $("#chats").append(chatbox(data[i].id, data[i].name, data[i].users));
      $("#chats form").submit(goToRoom);
    }
  };
};

function goToRoom(event){
  event.preventDefault();
  let data = $(this).serializeArray();
  let msg = {'username': username, 'room': data[0].value};
  socket.emit('switch_room', JSON.stringify(msg));
}

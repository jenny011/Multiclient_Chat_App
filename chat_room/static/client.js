var socket = io.connect("http://localhost:5000");

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
    socket.emit('leave_room', JSON.stringify({'username':username}));
  });

  //-----refresh entrance list-----
  sendRequest("updateLists", "GET", null, updateLists);
  var refreshEntrance = setInterval(sendRequest, 5000, "updateLists", "GET", null, updateLists);

  $(".room-item").on("submit", joinRoom);
  $(".user-item").on("submit", joinUser);

  //-----rooms list-----
  sendRequest("updateMyRooms", "GET", null, updateMyRooms);
  var refreshMyRooms = setInterval(sendRequest, 5000, "updateMyRooms", "GET", null, updateMyRooms);

  //-----messaging-----
  //---system messages---
  socket.on('client_joined', function(user){
    if (user == username) {
      clearInterval(refreshEntrance);
      sendRequest("updateMyRooms", "GET", null, updateMyRooms);
      $("#entrance-container").hide();
      $("#interface-container").show();
      $("#messages").empty();
    } else {
      let displayMsg = replaceSymbols(user) + " joined";
      $("#messages").append('<div class="system-msg"><i>' + displayMsg + '</i></div>');
    }
    $("#msg-container").animate({ scrollTop: $('#msg-container').prop("scrollHeight") }, 1000);
  });

  socket.on('client_left', function(user){
    // refreshEntrance = setInterval(sendRequest, 500, "updateLists", "GET", null, updateLists);
    if (user == username) {
      sendRequest("updateLists", "GET", null, updateLists);
      sendRequest("updateMyRooms", "GET", null, updateMyRooms);
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
    //socket.emit("leave_room", {'username': username, 'room': target_room});
    // socket.emit("leave_room", JSON.stringify({'username':username}));
    var refreshEntrance = setInterval(sendRequest, 5000, "updateLists", "GET", null, updateLists);
    sendRequest("updateMyRooms", "GET", null, updateMyRooms);
    $("#entrance-container").hide();
    $("#interface-container").show();
    $("#messages").empty();
  });

  $("#logout").on("click", function(){
    //socket.emit("leave_room", {'username': username, 'room': target_room});
    socket.emit("leave_room", JSON.stringify({'username':username}));
    socket.disconnect();
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
    $("#user-id-"+id).submit(joinUser);
  }
};

function joinRoom(event){
  event.preventDefault();
  let data = $(this).serializeArray();
  let msg = {'username': username, 'room': data[0].value};
  socket.emit('join_room', JSON.stringify(msg));
}

function joinUser(event) {
  event.preventDefault();
  let data = $(this).serializeArray();
  let msg = {'username': username, 'user': data[0].value};
  socket.emit('create_room', JSON.stringify(msg));
}

function updateMyRooms(data) {
  $("#chats").empty();
  for (let i=0; i<data.length; i++) {
    $("#chats").append(chatbox(data[i].id, data[i].name, data[i].users));
    $("#chats form").submit(goToRoom);
  };
};

function goToRoom(event){
  event.preventDefault();
  let data = $(this).serializeArray();
  let msg = {'username': username, 'room': data[0].value};
  socket.emit('leave_room', JSON.stringify(msg));
  socket.emit('join_room', JSON.stringify(msg));
}

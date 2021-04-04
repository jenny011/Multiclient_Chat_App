$(document).ready(function() {
  var refreshEntrance = setInterval(sendRequest, 2000, "updateLists", "GET", null, updateLists);

  var socket = io.connect("http://localhost:5000");

  socket.on('connect', function(){
    //socket.emit('get_room', username);
    console.log("connected", username);
  });

  socket.on('disconnect', function(){
    clearInterval(refreshEntrance);
    socket.emit('leave_room', username);
  });

  socket.on('display_room', function(msg){
    let myMsg = JSON.parse(replaceSymbols(msg));
    for (let i=0; i++; i<myMsg.length) {
      $("#chats").append(chatbox(myMsg[i].name, myMsg[i].users));
    };
  });

  socket.on('undisplay_room', function(msg){
    let myMsg = JSON.parse(replaceSymbols(msg));
    for (let i=0; i++; i<myMsg.length) {
      $("#"+myMsg.id).remove();
    };
  });

  socket.on('client_joined', function(user){
    if (user == username) {
      $("#entrance-container").hide();
      $("#interface-container").show();
    }
    clearInterval(refreshEntrance);
    let displayMsg = replaceSymbols(user) + " joined";
    $("#messages").append('<div class="system-msg"><i>' + displayMsg + '</i></div>');
  });

  socket.on('client_left', function(user){
    // refreshEntrance = setInterval(sendRequest, 500, "updateLists", "GET", null, updateLists);
    if (user == username) {
      $("#interface-container").hide();
      $("#entrance-container").show();
    }
    let displayMsg = replaceSymbols(user) + " left";
    $("#messages").append('<div class="system-msg"><i>' + displayMsg + '</i></div>');
  });

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

  $(".room-item").on("submit", function(event){
    event.preventDefault();
    var data = $(this).serializeArray();
    socket.emit('join_room', {'username': username, 'room': data[0].value});
  });

  $(".user-item").on("submit", function(event){
    event.preventDefault();
    var data = $(this).serializeArray();
    socket.emit('create_room', {'username': username, 'user': data[0].value});
  });

  $("#leave_room").on("click", function(){
    //socket.emit("leave_room", {'username': username, 'room': target_room});
    console.log(username);
    socket.emit("leave_room", username);
  });

  $("#logout").on("click", function(){
    //socket.emit("leave_room", {'username': username, 'room': target_room});
    socket.emit("leave_room", username);
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

function updateLists(data, socket) {
  $("#rooms").empty();
  $("#users").empty();
  for (let i=0; i<data['rooms'].length; i++) {
    let id = data['rooms'][i]['id'];
    $("#rooms").append(roomsList(id, data['rooms'][i]['name']));
    $("#room-id-"+id).submit(refreshRoomList);
  }
  for (let i=0; i<data["users"].length; i++) {
    let id = data['users'][i];
    $("#users").append(usersList(id));
    $("#user-id-"+id).submit(refreshUserList);
  }
};

function refreshRoomList(event){
  event.preventDefault();
  var data = $(this).serializeArray();
  socket.emit('add_room', {'username': username, 'room': data.value});
}

function refreshUserList(event) {
  event.preventDefault();
  var data = $(this).serializeArray();
  socket.emit('create_room', {'username': username, 'user': data.value});
}

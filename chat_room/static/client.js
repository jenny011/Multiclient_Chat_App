$(document).ready(function() {

  var socket = io.connect("http://127.0.0.1:5000");

  socket.on('connect', function(){
    console.log(target_room, target_user);
    if (target_room) {
      socket.emit('join_room', {'username': username, 'room': target_room});
      console.log("joined the room ", target_room);
    } else {
      socket.emit('create_room', {'username': username, 'user': target_user});
      console.log("created with user ", target_user);
    }
  });

  socket.on('disconnect', function(){
    socket.emit('leave_room', username);
  });

  socket.on('client_joined', function(msg){
    let displayMsg = replaceSymbols(msg.msg);
    $("#messages").append('<div class="system-msg"><i>' + displayMsg + '</i></div>');
  });

  socket.on('client_left', function(msg){
    let displayMsg = replaceSymbols(msg);
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

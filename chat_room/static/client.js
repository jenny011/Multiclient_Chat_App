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
    $("#messages").append('<li><i>' + msg.msg + '</i></li>');
  });

  socket.on('client_left', function(msg){
    $("#messages").append('<li><i>' + msg + '</i></li>');
  });

  socket.on('message', function(msg){
    $("#messages").append('<li>' + msg + '</li>');
  });

  $("#sendBtn").on("click", function(){
    let msg = {"username": username, "msg": $('#myMsg').val()};
    socket.send(JSON.stringify(msg));
    // socket.emit("send_msg", {'msg': msg, 'room': target_room});
    $('#myMsg').val('');
  });

  $("#leave_chat").on("click", function(){
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

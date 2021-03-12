$(document).ready(function() {
  var socket = io.connect("http://127.0.0.1:5000");

  socket.on('connect', function(){
    socket.emit('join_room', {'username': username });
  });

  socket.on('disconnect', function(){
    socket.emit('leave_room', {'username': username });
  });

  socket.on('client_left', function(msg){
    $("#messages").append('<li><i>' + msg + '</i></li>');
  });

  socket.on('message', function(msg){
    $("#messages").append('<li>' + msg + '</li>');
  });

  $("#sendBtn").on("click", function(){
    socket.send($('#myMsg').val());
    $('#myMsg').val('');
  });

  $("#logout").on("click", function(){
    socket.emit("leave_room", {'username': username });
  });
});

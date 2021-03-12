$(document).ready(function() {
  var socket = io.connect("http://127.0.0.1:5000");

  socket.on('connect', function(){
    socket.emit('client_connect', {'username': 'username'});
  });

  socket.on('logout_res', function(msg, cb){
    if (cb) {
      cb();
    }
  });

  socket.on('disconnect', function(){
    socket.emit('client_disconnect', {'username': 'username'});
  });

  socket.on('message', function(msg){
    $("#messages").append('<li>' + msg + '</li>');
  });

  $("#sendBtn").on("click", function(){
    socket.send($('#myMsg').val());
    $('#myMsg').val('');
  });

  $("#logout").on("click", function(){
    socket.emit("logout_req");
  });
});

//-----entrance-----
function roomsList(id, name) {
  return "<li class='list-group-item'> <form class='room-item' id='room-id-" + id + "'> <input class='d-none form-control-plaintext' type='text' name='room' value=" + id + " readonly> <span>" + name + "</span> <input class='btn btn-sm btn-primary float-right' type='submit' value='Join'> </form> </li>";
}

function usersList(user) {
  return "<li class='list-group-item'> <form class='user-item' id='user-id-" + user + "'> <input class='d-none form-control-plaintext' type='text' name='user' value=" + user + " readonly> <input class='btn btn-sm btn-outline-primary' type='submit' value=" + user + "> </form> </li>";
}

//-----chat display-----
function leftMsg(user, msg) {
  return '<div class="user-msg-box left-box"><div class="user-box"><div class="user-id">' + user + '</div><div class="user-avatar"><i class="fa fa-2x fa-user-circle-o" aria-hidden="true"></i></div></div><div class="user-msg left-msg">' + msg + '</div></div>';
}

function rightMsg(user, msg) {
  return '<div class="user-msg-box right-box"><div class="user-box"><div class="user-id">' + user + '</div><div class="user-avatar"><i class="fa fa-2x fa-user-circle" aria-hidden="true"></i></div></div><div class="user-msg right-msg">' + msg + '</div></div>';
}

//-----chat room display-----
function chatbox(id, name, users) {
  return '<form class="chat-box"> <input class="d-none form-control-plaintext" type="text" name="room" value=' + id + ' readonly> <input class="btn btn-sm btn-outline-primary" type="submit" value=' + name + '> <div class="room-box room-users">' + users + '</div> </form>';
}

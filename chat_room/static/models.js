function leftMsg(user, msg) {
  return '<div class="user-msg-box left-box"><div class="user-box"><div class="user-id">' + user + '</div><div class="user-avatar"><i class="fa fa-2x fa-user-circle-o" aria-hidden="true"></i></div></div><div class="user-msg left-msg">' + msg + '</div></div>'
}

function rightMsg(user, msg) {
  return '<div class="user-msg-box right-box"><div class="user-box"><div class="user-id">' + user + '</div><div class="user-avatar"><i class="fa fa-2x fa-user-circle" aria-hidden="true"></i></div></div><div class="user-msg right-msg">' + msg + '</div></div>'
}

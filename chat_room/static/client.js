var socket = io.connect("http://localhost:5000");
var interval = 5000;
var msg_buffer = new Map();
var current_room = null;
var boundary = -1;
var pointer = 0;

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
    current_room = null;
  });

  //-----refresh entrance list-----
  sendRequest("updateLists", "GET", null, updateLists);
  //DEBUG: what if freeze and then target user logs out?
  // var refreshEntrance = setInterval(sendRequest, interval, "updateLists", "GET", null, updateLists);
  var refreshEntrance = setInterval(freezeOrUpdate, interval);

  //-----rooms list-----
  sendRequest("updateMyRooms", "GET", null, updateMyRooms);

  //-----------messaging-----------
  socket.on('client_active', function(msg){
    let msg_decoded = JSON.parse(msg);
    let active_users = msg_decoded.active_users;
    updateRecvrList(msg_decoded.room, msg_decoded.active_users);
  });

  socket.on('client_inactive', function(msg){
    let msg_decoded = JSON.parse(msg);
    let active_users = msg_decoded.active_users;
    updateRecvrList(msg_decoded.room, msg_decoded.active_users);
  });

  socket.on('client_invited', function(data) {
    let msg = JSON.parse(data);
    socket.emit('add_room', JSON.stringify({"username": username, "room": msg.room}));
    alert(msg.msg);
  });

  socket.on('client_joined', function(msg){
    let msg_decoded = JSON.parse(msg);
    let user = msg_decoded.username;
    let room = msg_decoded.room;
    let roomname = msg_decoded.roomname;
    if (user == username) {
      boundary = msg_decoded.boundary;
      let last_ten_msgs = msg_decoded.last_ten_msgs;
      if (boundary == 0) {
        $("prev-history").addClass("disabled");
        $("next-history").addClass("disabled");
      }

      clearInterval(refreshEntrance);
      sendRequest("updateMyRooms", "GET", null, updateMyRooms);
      $("#entrance-container").hide();
      $("#interface-container").show();
      $('#room-header').text(roomname);
      $("#messages").empty();
      current_room = room;

      if (msg_buffer.has(room) && msg_buffer.get(room).length > 0) {
        let buffered_msgs = msg_buffer.get(room);
        //display 10-len(buffer) history msgs
        if (buffered_msgs.length < last_ten_msgs.length){
          for (let i=0; i<last_ten_msgs.length - buffered_msgs.length; i++) {
            let one_msg = JSON.parse(last_ten_msgs[i]);
            console.log("history",one_msg.target);
            displayMessage(one_msg.username, one_msg.target, one_msg.msg, one_msg.target != "", i==one_msg.length-1);
          };
        }
        //display buffered msgs
        for (let i=0; i<buffered_msgs.length; i++) {
          displayMessage(buffered_msgs[i].username, buffered_msgs[i].target, buffered_msgs[i].msg, buffered_msgs[i].private, i==buffered_msgs.length-1);
        }
        msg_buffer.set(room, []);
      } else {
        for (let i=0; i<last_ten_msgs.length; i++) {
          //display 10 history msgs
          let one_msg = JSON.parse(last_ten_msgs[i]);
          displayMessage(one_msg.username, one_msg.target, one_msg.msg, one_msg.target != "", i==one_msg.length-1);
        };
      };
    };
    updateRecvrList(room, msg_decoded.active_users);
  });

  socket.on('client_left', function(user){
    if (user == username) {
      sendRequest("updateLists", "GET", null, updateLists);
      sendRequest("updateMyRooms", "GET", null, updateMyRooms);
      var refreshEntrance = setInterval(freezeOrUpdate, interval)
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
      let displayMsg = escapeHtml(user) + " joined";
      $("#messages").append('<div class="system-msg"><i>' + displayMsg + '</i></div>');
    };
    $("#msg-container").animate({ scrollTop: $('#msg-container').prop("scrollHeight") }, 1000);
  });

  socket.on('client_removed', function(user){
    if (user == username) {
      sendRequest("updateLists", "GET", null, updateLists);
      sendRequest("updateMyRooms", "GET", null, updateMyRooms);
      var refreshEntrance = setInterval(freezeOrUpdate, interval);
      $("#interface-container").hide();
      $("#entrance-container").show();
      $("#messages").empty();
    } else {
      let displayMsg = escapeHtml(user) + " left";
      $("#messages").append('<div class="system-msg"><i>' + displayMsg + '</i></div>');
      $("#private option[value='" + user + "']").remove();
    }
    $("#msg-container").animate({ scrollTop: $('#msg-container').prop("scrollHeight") }, 1000);
  });

  //---------user messages---------
  socket.on('message', function(msg){
    let msg_decoded = null;
    try{
      msg_decoded = JSON.parse(msg);
      msg_decoded.msg = escapeHtml(msg_decoded.msg);
      msg_decoded.target = escapeHtml(msg_decoded.target);
    } catch (err) {
      alert(msg);
      return;
    };
    let room = msg_decoded.room;
    let private = msg_decoded.target != "";
    //console.log(msg_decoded.username, msg_decoded.msg, private);
    if (room != current_room) {
      if (msg_buffer.has(room)) {
        let msgs = msg_buffer.get(room);
        msgs.push({"username":msg_decoded.username, "target":msg_decoded.target, "msg":msg_decoded.msg, "private":private});
        msg_buffer.set(room, msgs);
      } else {
        let msgs = [{"username":msg_decoded.username, "target":msg_decoded.target, "msg":msg_decoded.msg, "private":private}];
        msg_buffer.set(room, msgs);
      }
      let unread_number = msg_buffer.get(room).length <= 99 ? msg_buffer.get(room).length.toString() : "...";
      $("#notification-" + room + " span").text(unread_number);
      $("#notification-" + room).removeClass("d-none");
    } else {
      displayMessage(msg_decoded.username, msg_decoded.target, msg_decoded.msg, private, true);
    };
  });

  socket.on('history', function(msg){
    $("#history-messages").empty();
    msg_decoded = JSON.parse(msg);
    let history_msgs = msg_decoded.history;
    for (let i=0; i<history_msgs.length; i++) {
      //display 10 history msgs
      let one_msg = JSON.parse(history_msgs[i]);
      displayHistoryMessage(one_msg.username, one_msg.target, one_msg.msg, one_msg.target != "");
    };
  });

  socket.on('refreshRoom', function(room_id){
    alert("Room " + room_id + " has been dismissed.");
    sendRequest("updateLists", "GET", null, updateLists);
    sendRequest("updateMyRooms", "GET", null, updateMyRooms);
  });

  socket.on('refreshUser', function(user){
    alert("User " + user + " is not active any more.");
    sendRequest("updateLists", "GET", null, updateLists);
    sendRequest("updateMyRooms", "GET", null, updateMyRooms);
  });


//-----------------DOM----------------
  $(".room-item").on("submit", joinRoom);
  $("#active-users-list").submit(inviteUser);

  $("#msgform").on("submit", function(event){
    event.preventDefault();
    let data = $(this).serializeArray();
    let target = data[0].value;
    let msgText = data[1].value;
    if (msgText) {
      if (target) {
        let msg = {"username": username, "msg": msgText, "target": target};
        socket.send(JSON.stringify(msg));
      } else {
        let msg = {"username": username, "msg": msgText, "target": target};
        socket.send(JSON.stringify(msg));
        // socket.emit("send_msg", {'msg': msg, 'room': target_room});
      };
      $('#myMsg').val('');
    };
  });

  //-----leave-----
  $("#leave_room").on("click", function(){
    if (msg_buffer.has(current_room)) {
      msg_buffer.delete(current_room);
    }
    current_room = null;
    socket.emit("leave_room", username);
  });

  $("#logout").on("click", function(){
    current_room = null;
    //DEBUG: emit an event, others update user list on logout
    // $("#private option[value='" + username + "']").remove();
    socket.emit("set_inactive", username);
  });

  //-----search-----
  $("#search").on("click", function(){
    current_room = null;
    socket.emit("leave_page", username);
  });

  //-----prev & next 10-----
  $("#history-page-btn").on("click", function(){
    console.log(boundary);
    socket.emit("fetch_history", JSON.stringify({"username":username, "room":current_room, "boundary":boundary, "pointer":pointer}));
  });

  $("#prev-history").on("click", function(){
    if (pointer < boundary) {
      pointer = pointer + 10;
      socket.emit("fetch_history", JSON.stringify({"username":username, "room":current_room, "boundary":boundary, "pointer":pointer}));
    }
  });

  $("#next-history").on("click", function(){
    if (pointer > 0) {
      pointer = pointer - 10;
      if (pointer <= 0) {
        pointer = 0;
      };
      socket.emit("fetch_history", JSON.stringify({"username":username, "room":current_room, "boundary":boundary, "pointer":pointer}));
    }
  });
});


//-----------
$(document).keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      event.preventDefault();
      $("#sendBtn").click();
    };
});

function freezeOrUpdate() {
  if (!$("#users input[type='checkbox']").prop('checked')) {
    sendRequest("updateLists", "GET", null, updateLists);
  };
}

function displayMessage(user, target, msg, private, scroll) {
  displayMsgHelper("#messages", user, target, msg, private, scroll);
}

function displayHistoryMessage(user, target, msg, private) {
  displayMsgHelper("#history-messages", user, target, msg, private, false);
};

function displayMsgHelper(div_id, user, target, msg, private, scroll) {
  if (private) {
    if (user == username) {
      $(div_id).append(rightPrivateMsg(user, "(to " + target + ")",  msg));
    } else {
      if (target == username) {
        $(div_id).append(leftPrivateMsg(user, msg));
      };
    };
  } else {
    if (user == username) {
      $(div_id).append(rightMsg(user, msg));
    } else {
      $(div_id).append(leftMsg(user, msg));
    };
  };
  if (scroll) {
    $("#msg-container").animate({ scrollTop: $('#msg-container').prop("scrollHeight") }, 800);
  };
}

//------Update Entrance-----
function updateLists(data) {
  $("#rooms").empty();
  $("#users").empty();
  for (let i=0; i<data['rooms'].length; i++) {
    let id = data['rooms'][i]['id'];
    $("#rooms").append(roomsList(id, data['rooms'][i]['name']));
    $("#room-id-"+id).submit(joinRoom);
  }
  for (let i=0; i<data["users"].length; i++) {
    let user = data['users'][i];
    $("#users").append(usersList(user));
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
  if (data.length >= 2 && data[0].value) {
    let users = [];
    for (var i = 1; i < data.length; i++) {
      users.push(data[i].value);
    }
    let msg = {'username': username, 'users': users, 'room': data[0].value};
    socket.emit('invite', JSON.stringify(msg));
    $('#newroom-name').val('');
  };
}

//------Update Left Panel-----
function updateMyRooms(data) {
  $("#chats").empty();
  for (let i=0; i<data.length; i++) {
    if (data[i].current) {
      $("#chats").append(active_chatbox(data[i].id, data[i].name));
    } else {
      let unread_number = 0;
      if (msg_buffer.has(data[i].id)) {
        unread_number = msg_buffer.get(data[i].id).length;
      };
      $("#chats").append(chatbox(data[i].id, data[i].name, unread_number));
      $("#chat-form-"+data[i].id).submit(goToRoom);
    }
  };
};

function goToRoom(event){
  event.preventDefault();
  let data = $(this).serializeArray();
  let msg = {'username': username, 'room': data[0].value};
  socket.emit('switch_room', JSON.stringify(msg));
}

function updateRecvrList(room, active_users){
  if (room == current_room) {
    $('#private option').each(function() {
        if ( $(this).val() ) {
            $(this).remove();
        }
    });
    active_users.forEach(user => {
      if (user != username) {
        $("#private").append(new Option(user, user));
      };
    });
  };
}

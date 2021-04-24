var socket = io.connect("http://localhost:5000");
var interval = 5000;
var msg_buffer = new Map();
var current_room = null;
var boundary = -1;
var ptr1 = -1;
var ptr2 = -1;
var refreshEntrance = null;

$(document).ready(function() {
  /** TCP socket connection **/
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


  /** entrance prep **/
  //-----refresh entrance list, my rooms list-----
  sendRequest("updateLists", "GET", null, updateLists);
  refreshEntrance = setInterval(freezeOrUpdate, interval);
  sendRequest("updateMyRooms", "GET", null, updateMyRooms);


  /** TCP events **/
  //-----refresh content-----
  socket.on('refreshRoom', function(room_id){
    alert("The room has been dismissed.");
    sendRequest("updateLists", "GET", null, updateLists);
    sendRequest("updateMyRooms", "GET", null, updateMyRooms);
  });

  socket.on('refreshUser', function(user){
    alert("User " + user + " is not active any more.");
    sendRequest("updateLists", "GET", null, updateLists);
    sendRequest("updateMyRooms", "GET", null, updateMyRooms);
  });


  //-----------client status-----------
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


  //-----------client chat room actions-----------
  socket.on('client_invited', function(data) {
    let msg = JSON.parse(data);
    socket.emit('add_room', JSON.stringify({"username": username, "room": msg.room}));
    alert(msg.msg);
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
      toggleInterface(false);
    } else {
      let displayMsg = escapeHtml(user) + " left";
      $("#messages").append('<div class="system-msg"><i>' + displayMsg + '</i></div>');
      $("#private option[value='" + user + "']").remove();
    }
    $("#msg-container").animate({ scrollTop: $('#msg-container').prop("scrollHeight") }, 1000);
  });


  //-----------client chat page actions-----------
  socket.on('client_joined', function(msg){
    let msg_decoded = JSON.parse(msg);
    let user = msg_decoded.username;
    let room = msg_decoded.room;
    let roomname = msg_decoded.roomname;
    let private_chat = msg_decoded.private_chat;

    if (user == username) {
      //set the boundary
      boundary = msg_decoded.boundary;
      ptr1 = boundary;
      ptr2 = boundary + 1;
      let last_ten_msgs = msg_decoded.last_ten_msgs;
      //toggle interface
      toggleInterface(true);
      if (private_chat) {
        $('#room-header').text(roomname + "*");
      } else {
        $('#room-header').text(roomname);
      };
      current_room = room;
      //display buffered and history messages
      if (msg_buffer.has(room) && msg_buffer.get(room).length > 0) {
        //if this room has buffered msgs
        let buffered_msgs = msg_buffer.get(room);
        //display 10-len(buffer) history msgs
        if (buffered_msgs.length < last_ten_msgs.length){
          for (let i=0; i<last_ten_msgs.length; i++) {
            let one_msg = JSON.parse(last_ten_msgs[i]);
            let this_target = escapeHtml(one_msg.target);
            displayMessage(one_msg.username, this_target, escapeHtml(one_msg.msg), this_target != "", i==last_ten_msgs.length-1);
          };
        } else {
          for (let i=0; i<buffered_msgs.length; i++) {
            let one_msg = JSON.parse(buffered_msgs[i]);
            let this_target = escapeHtml(one_msg.target);
            displayMessage(one_msg.username, this_target, escapeHtml(one_msg.msg), one_msg.private, i==buffered_msgs.length-1);
          }
        }
        msg_buffer.set(room, []);
      } else {
        //if this room DOESNT have buffered msgs
        for (let i=0; i<last_ten_msgs.length; i++) {
          //display 10 history msgs
          let one_msg = JSON.parse(last_ten_msgs[i]);
          let this_target = escapeHtml(one_msg.target);
          displayMessage(one_msg.username, this_target, escapeHtml(one_msg.msg), this_target != "", i==last_ten_msgs.length-1);
        };
      };
    };
    updateRecvrList(room, msg_decoded.active_users);
  });

  socket.on('client_left', function(user){
    if (user == username) {
      toggleInterface(false);
    }
  });

  //---------user messages---------
  socket.on('message', function(msg){
    let msg_decoded = null;
    try{
      msg_decoded = JSON.parse(msg);
      msg_decoded.msg = escapeHtml(msg_decoded.msg);
      msg_decoded.target = escapeHtml(msg_decoded.target);
    } catch (err) {
      console.log(err);
      alert("An error occurred, try again.");
      return;
    };
    let room = msg_decoded.room;
    let private = msg_decoded.target != "";

    if (room != current_room) {
      if (msg_buffer.has(room)) {
        let msgs = msg_buffer.get(room);
        if (!private || msg_decoded.target == username || msg_decoded.username == username) {
          msgs.push(JSON.stringify({"username":msg_decoded.username, "target":msg_decoded.target, "msg":msg_decoded.msg, "private":private}));
          msg_buffer.set(room, msgs);
        }
      } else {
        if (!private || msg_decoded.target == username || msg_decoded.username == username) {
          let msgs = [JSON.stringify({"username":msg_decoded.username, "target":msg_decoded.target, "msg":msg_decoded.msg, "private":private})];
          msg_buffer.set(room, msgs);
        }
      }
      let unread_number = msg_buffer.get(room).length <= 99 ? msg_buffer.get(room).length.toString() : "...";
      $("#notification-" + room + " span").text(unread_number);
      $("#notification-" + room).removeClass("d-none");
    } else {
      displayMessage(msg_decoded.username, msg_decoded.target, msg_decoded.msg, private, true);
    };
  });


  //---------chat history---------
  socket.on('history', function(msg){
    $("#history-messages").empty();
    msg_decoded = JSON.parse(msg);
    ptr1 = msg_decoded.ptr1;
    ptr2 = msg_decoded.ptr2;
    if (ptr1 < 0) {
      $("#prev-history").addClass("disabled");
    } else {
      $("#prev-history").removeClass("disabled");
    };
    if (ptr2 >= boundary) {
      $("#next-history").addClass("disabled");
    } else {
      $("#next-history").removeClass("disabled");
    };

    let history_msgs = msg_decoded.history;
    for (let i=0; i<history_msgs.length; i++) {
      //display 10 history msgs
      let one_msg = JSON.parse(history_msgs[i]);
      displayHistoryMessage(one_msg.username, escapeHtml(one_msg.target), escapeHtml(one_msg.msg), one_msg.target != "");
    };
  });


//-----------------DOM----------------
  $(".room-item").on("submit", joinRoom);
  $("#active-users-list").submit(inviteUser);

  //----send msg----
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
      };
      $('#myMsg').val('');
    };
  });

  //----send emoji----
  $(".emoji").on("click", function(){
    event.preventDefault();
    let target = $("#msgform #private").children("option:selected").val();
    let emoji = "[/" + $(this).attr("id") + "]";
    if (target) {
      let msg = {"username": username, "msg": emoji, "target": target};
      socket.send(JSON.stringify(msg));
    } else {
      let msg = {"username": username, "msg": emoji, "target": target};
      socket.send(JSON.stringify(msg));
    };
  })

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
    socket.emit("set_inactive", username);
  });

  //-----search-----
  $("#search").on("click", function(){
    current_room = null;
    socket.emit("leave_page", username);
  });

  //-----prev & next 10-----
  $("#history-page-btn").on("click", function(){
    fetchHistory("prev");
  });

  $("#prev-history").on("click", function(){
    if (ptr1 >= 0) {
      fetchHistory("prev");
    }
  });

  $("#next-history").on("click", function(){
    if (ptr2 <= boundary) {
      fetchHistory("next");
    }
  });

});


//-----refresh request------
function freezeOrUpdate() {
  if (!$("#users input[type='checkbox']").prop('checked')) {
    sendRequest("updateLists", "GET", null, updateLists);
  };
}

//-----Toggle Interface-----
function toggleInterface(chatOn){
  if (chatOn) {
    clearInterval(refreshEntrance);
    sendRequest("updateMyRooms", "GET", null, updateMyRooms);
    $("#interface-container").show();
    $("#entrance-container").hide();
    $("#messages").empty();
  } else {
    sendRequest("updateLists", "GET", null, updateLists);
    sendRequest("updateMyRooms", "GET", null, updateMyRooms);
    refreshEntrance = setInterval(freezeOrUpdate, interval);
    $("#interface-container").hide();
    $("#entrance-container").show();
    $("#messages").empty();
  }
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
  if (data.length >= 3 && data[0].name == "newroom-private" && data[1].name == "newroom-name" && data[2].name.startsWith("user")) {
    createRoomWithUser(data, 2, data[1].value, data[0].value);
  } else if (data.length >= 2 && data[0].name == "newroom-name" && data[1].name.startsWith("user")) {
    createRoomWithUser(data, 1, data[0].value, 'off');
  };
}

function createRoomWithUser(data, roomIndex, rooms, is_private){
  let users = [];
  for (var i = roomIndex; i < data.length; i++) {
    users.push(data[i].value);
  }
  let msg = {'username': username, 'users': users, 'room': rooms, 'private_chat': is_private};
  $("#newroom-private").prop('checked', false);
  socket.emit('invite', JSON.stringify(msg));
  $('#newroom-name').val('');
}

//------Left Panel Actions-----
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

//-----Right Panel Actions-----
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

$(document).keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      event.preventDefault();
      $("#sendBtn").click();
    };
});

function fetchHistory(direction) {
  socket.emit("fetch_history", JSON.stringify({"username":username, "room":current_room, "boundary":boundary, "ptr1":ptr1, "ptr2":ptr2, "direction":direction}));
}

//-----display messages-----
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

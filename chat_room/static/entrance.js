$(document).ready(function() {
  setInterval(sendRequest, 10000, "updateLists", "GET", null, updateLists);
  // $(".userBtn").on("click", function(e){
  //   value = $(this).text();
  //   data = {'action': 'user', 'target': value};
  //   console.log(data);
  //   sendRequest("chat", "POST", data, null);
  // });
});

function updateLists(data) {
  $("#rooms").empty();
  $("#users").empty();
  for (let i=0; i<data['rooms'].length; i++){
    $("#rooms").append("<li class='list-group-item'> <form action='/join_chat_room' method='POST'> <input class='d-none form-control-plaintext' type='text' name='target' value=" + data['rooms'][i]['id'] + " readonly> <span>" + data['rooms'][i]['name'] + "</span> <input class='btn btn-sm btn-primary float-right' type='submit' value='Join'> </form> </li>");
  }
  for (let i=0; i<data["users"].length; i++){
    $("#users").append("<li class='list-group-item'> <form action='/start_chat_user' method='POST'> <input class='btn btn-sm btn-outline-primary' type='submit' name='target' value=" + data['users'][i] + "> </form> </li>");
  }
};

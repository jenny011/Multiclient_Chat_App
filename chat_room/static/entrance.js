$(document).ready(function() {
  setInterval(sendRequest, 1000, "updateLists", "GET", null, updateLists);
  // $(".userBtn").on("click", function(e){
  //   value = $(this).text();
  //   data = {'action': 'user', 'target': value};
  //   console.log(data);
  //   sendRequest("chat", "POST", data, null);
  // });
});

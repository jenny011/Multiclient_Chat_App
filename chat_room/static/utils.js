var emoji_strs = ["[/laugh]", "[/surprised]", "[/cry]", "[/hug]", "[/sun]", "[/rabbit]", "[/good]", "[/peace]"];

function goToPage(route, delay) {
  setTimeout("window.location.replace('http://localhost:5000/" + route + "')", delay);
}

function goToPageNewTab(route, delay) {
  setTimeout("window.open('http://localhost:5000/" + route + "')", delay);
}

function sendRequest(route, type, data, successHandler){
  $.ajax({
    url: "http://localhost:5000/" + route,
    type: type,
    data: data,
    success: (res) => {
      if (successHandler){
        successHandler(res);
      };
    },
    error: (err) => {
      alert("request error");
      console.log(err);
    }
  });
}

function escapeHtml(msg) {
  if (emoji_strs.includes(msg)) {
    let emoji_name = msg.slice(2,msg.length-1);
    return '<img src="/static/images/' + emoji_name + '.png" alt="' + emoji_name + '" height="60">';
  } else {
    return msg
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
  };
 }

function goToPage(route, delay) {
  setTimeout("window.location.replace('http://localhost:5000/" + route + "')", delay);
}

function goToPageNewTab(route, delay) {
  setTimeout("window.open('http://localhost:5000/" + route + "')", delay);
}

function sendRequest(route, type, data, successHandler){
  console.log("update room and user lists");
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

function replaceSymbols(msg) {
  let ret = msg.replaceAll("<", "&lt;");
  ret = ret.replaceAll(">", "&gt;");
  return ret;
}

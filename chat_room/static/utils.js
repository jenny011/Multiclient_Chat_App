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
// 
// function replaceSymbols(msg) {
//   let ret = msg.replaceAll("<", "&lt;");
//   ret = ret.replaceAll(">", "&gt;");
//   return ret;
// }

function escapeHtml(msg) {
    return msg
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

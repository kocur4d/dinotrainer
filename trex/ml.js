let mlCanvas;

function sendBase64 (base64) {
  var httpPost = new XMLHttpRequest();
  var path = "http://127.0.0.1:8000/upload";
  var data = JSON.stringify({image: base64});
  httpPost.open("POST", path, true);
  httpPost.onreadystatechange = function(err) {
    if (httpPost.readyState == 4 && httpPost.status == 200) {
      // TODO: handle successful response
      console.log('---ok', httpPost.responseText);
      document.dispatchEvent(new KeyboardEvent('keydown', {'keyCode': 38}))
    } else {
      // TODO: handle error
      console.log('---err', err);
    }
  };
  // Set the content type of the request to json since that's what's being sent
  httpPost.setRequestHeader('Content-Type', 'application/json');
  httpPost.send(data);
};

function tic() {
  if(!Runner.instance_.crashed)
    sendBase64(mlCanvas.toDataURL());
}

function mlMain() {
  mlCanvas = document.getElementById("gamecanvas");
  setInterval(tic, 100);
}

addLoadEvent(mlMain);

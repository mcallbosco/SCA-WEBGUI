document.getElementById('WaitText').hidden = true;
var url = "ws:13.58.90.158:8008";


document.getElementById('files').addEventListener('change', handleFileSelect, false);
function handleFileSelect(event) {
    document.getElementById('consoleOutputArea').textContent = " ";
    var files = event.target.files; // Get selected files

    // get text content of the file
    var file = files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
        var codeInput = e.target.result;
        //make sure the code is not too long
        if(codeInput.length > 10000){
            document.getElementById('consoleOutputArea').textContent = "Error: File is too large";
            return;
        }
        
        uploadCode(codeInput);
        document.getElementById ('SCAinfoBanner').hidden = true;
        document.getElementById('WaitText').hidden = false;
        document.getElementById ('htmlarea').hidden = true;


    }
    reader.readAsText(file);
  }


function uploadCode(codeInput){
    socket = new WebSocket(url);
    //wait for connect

    socket.onopen = function(event) {
        console.log("Connected to server");
        socket.send(codeInput);
    }
    socket.onerror = function(event) {
        document.getElementById('consoleOutputArea').textContent = ("Error: " + event.data + " Please try again later");
    }


    
    socket.onmessage = function(event) {
        if(!event.data.startsWith("Error")){
            //get the path of the file
            document.getElementById ('htmlarea').hidden = false;

            document.getElementById ('htmlarea').innerHTML = event.data;
            document.getElementById ('SCAinfoBanner').hidden = true;
            document.getElementById ('WaitText').hidden = true;

        }
        else{
            document.getElementById('consoleOutputArea').textContent = event.data;
            document.getElementById('WaitText').hidden = true;

        }
        
    }

}


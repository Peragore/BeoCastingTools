var socket = new WebSocket("ws://localhost:8766");
messages = document.createElement('ul');

socket.onmessage = function (event) {
            console.log(event.data);
            document.getElementById('dancer').style.backgroundImage = event.data;
            };


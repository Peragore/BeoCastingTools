let socket = new WebSocket("ws://localhost:8766")
socket.onopen = function(e) {
  // alert("[open] Connection established");
  // alert("Sending to server");
  socket.send("My name is John");
};

let cached_message = '';
socket.onmessage = async function(event) {
  let message = event.data;
  let messageElem = document.createElement('div');
  let element = document.getElementById('ticker');
  let element2 = document.getElementById('ticker2');
  let element3 = document.getElementById('ticker3');


  let width = getWidthOfText(message, element.style.fontFamily, element.style.fontSize);

  if (message.localeCompare(cached_message) != 0) {

    cached_message = message;
  }
  messageElem.textContent = cached_message;
  element.innerHTML = cached_message;
  element2.innerHTML = cached_message;
  element3.innerHTML = cached_message;
  let desiredSpeed = 5;
  let time = width/desiredSpeed;
  element.style.animation = 'marquee ' + time + 's linear 1 forwards';
  while(element.getBoundingClientRect().right > 1920){
    await new Promise(r => setTimeout(r, 10));
  }
  element2.style.animation = 'marquee2 ' + time + 's linear infinite ';
  element3.style.animation = 'marquee3 ' + time + 's linear infinite ' + time/2 + 's';
};

// while(true){
//
//
//     let messageElem = document.createElement('div');
//     let element = document.getElementById('ticker');
//     let element2 = document.getElementById('ticker2');
//
//
//     let width = getWidthOfText(cached_message, element.style.fontFamily, element.style.fontSize);
//     messageElem.textContent = cached_message;
//     element.innerHTML = cached_message;
//     element2.innerHTML = cached_message;
//
//     let desiredSpeed = 30;
//     let time = width/desiredSpeed
//     element.style.animation = 'marquee ' + time + 's linear 1 forwards';
//     element2.style.animation = 'marquee2 ' + time + 's linear infinite ' + time/2 + 's';
//
//
//
// }

function getWidthOfText(txt, fontname, fontsize){
    if(getWidthOfText.c === undefined){
        getWidthOfText.c=document.createElement('canvas');
        getWidthOfText.ctx=getWidthOfText.c.getContext('2d');
    }
    var fontspec = fontsize + ' ' + fontname;
    if(getWidthOfText.ctx.font !== fontspec)
        getWidthOfText.ctx.font = fontspec;
    return getWidthOfText.ctx.measureText(txt).width;
}

function readText(filePath) {
    let client = new XMLHttpRequest();
    client.open('GET', filePath);
    client.onreadystatechange = function(){return client.responseText};
    client.send();
}




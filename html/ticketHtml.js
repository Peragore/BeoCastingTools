let socket = new WebSocket("ws://localhost:8766")
socket.onopen = function(e) {
  // alert("[open] Connection established");
  // alert("Sending to server");
  socket.send("My name is John");
};

let cached_message = '';
socket.onmessage = function(event) {
  let message = event.data;
  let messageElem = document.createElement('div');
  let element = document.getElementById('ticker');

  let width = getWidthOfText(message, element.style.fontFamily, element.style.fontSize);
  let calc_width = width;
  if (message.localeCompare(cached_message) != 0) {

    cached_message = message;
  }
  messageElem.textContent = cached_message;
  element.innerHTML = cached_message;
  let desiredSpeed = 5;
  let time = width/desiredSpeed
  element.style.animation = 'marquee linear infinite ' + time + 's';
};


socket.onerror = function(error) {
  alert(`[error] ${error.message}`);
};

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

var timeFor10Px = 0.2;
var animationSettings = 'marquee linear infinite';
var $marque = $('.marque');

$marque.each( function() {
  var outerWidth = $(this).outerWidth();
  var calc = outerWidth / 10 * timeFor10Px;
  $(this).css('animation', animationSettings + ' ' + calc + 's');
});

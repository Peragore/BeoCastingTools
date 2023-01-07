console.log("hello");
function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

//usage:
readTextFile("../json/datastream.json", function(text){
    var data = JSON.parse(text);
    // console.log(data)
    let scores = data.scores;
    let score_keys = Object.keys(scores);
    let p1_score = scores[score_keys[0]];
    let p2_score = scores[score_keys[1]];
    let images = data.images;
    // console.log(images)
    document.getElementById('right_text_id').textContent = p1_score;
    document.getElementById('left_text_id').textContent = p2_score;
    document.getElementById('right_player_id').style.content = images[0];
    document.getElementById('left_player_id').style.content = images[1];
    document.getElementById('right_player_race').style.content = images[2];
    document.getElementById('left_player_race').style.content = images[3];




});

function reset_animation(){
    let right_splash = document.getElementById('right_splash_id');
    let left_splash = document.getElementById('left_splash_id');
    right_splash.style.animation = 'none';
    left_splash.style.animation = 'none';
    right_splash.offsetHeight;
    left_splash.offsetHeight;
    right_splash.style.animation = null;
    left_splash.style.animation = null;
}

window.addEventListener('obsSourceActiveChanged', function (event){
    if (event.detail.active){
    readTextFile("../json/datastream.json", function(text){
        var data = JSON.parse(text);
        // console.log(data)
        let scores = data.scores;
        let score_keys = Object.keys(scores);
        let p1_score = scores[score_keys[0]];
        let p2_score = scores[score_keys[1]];
        let images = data.images;
        console.log(images)
        document.getElementById('right_text_id').textContent = p1_score;
        document.getElementById('left_text_id').textContent = p2_score;
        document.getElementById('right_player_id').style.content = images[0];
        document.getElementById('left_player_id').style.content = images[1];
        document.getElementById('right_player_race').style.content = images[2];
        document.getElementById('left_player_race').style.content = images[3];
    });
    console.log('Transitioning')
    reset_animation();
    } else {

    }
});

// document.getElementById('right_text_id').textContent = data

// const color = "#FFF" /* white outline */
// const r = 10 /* width of outline in pixels */
// const n = Math.ceil(2*Math.PI*r) /* number of shadows */
// var str = 'Test'
// for(var i = 0;i<n;i++) /* append shadows in n evenly distributed directions */
// {
// const theta = 2*Math.PI*i/n
// str += (r*Math.cos(theta))+"px "+(r*Math.sin(theta))+"px 0 "+color+(i==n-1?"":",")
// }
// console.log(str)
// document.getElementById('right_text').style.textShadow = str
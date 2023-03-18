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

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

readTextFile("../json/datastream.json", function(text){
    var data = JSON.parse(text);
    // console.log(data)
    let aligulac = data.aligulac_bo5;
    let scores = data.scores;
    let Player_Names = Object.keys(scores);
    // console.log(images)
    document.getElementById('player1').textContent = Player_Names[0];
    document.getElementById('player2').textContent = Player_Names[1];
    document.getElementById('H2H1').textContent = aligulac[0];
    document.getElementById('H2H2').textContent = aligulac[1];
    document.getElementById('Form1').textContent = aligulac[2];
    document.getElementById('Form2').textContent = aligulac[3];
    document.getElementById('WinChance1').textContent = aligulac[4][0];
    document.getElementById('WinChance2').textContent = aligulac[4][1];
    document.getElementById('MeanRes').textContent = aligulac[4][2];

    sleep(1000)
    textFit(document.getElementsByClassName("p1container"));
    textFit(document.getElementsByClassName("p2container"));
    textFit(document.getElementsByClassName("H2H1"));
    textFit(document.getElementsByClassName("H2H2"));
    textFit(document.getElementsByClassName("Form1"));
    textFit(document.getElementsByClassName("Form2"));
    textFit(document.getElementsByClassName("WinChance1"));
    textFit(document.getElementsByClassName("WinChance2"));
    textFit(document.getElementsByClassName("MeanRes"));

});

window.addEventListener('obsSourceActiveChanged', function (event){
    if (event.detail.active){
        var data = JSON.parse(text);
        // console.log(data)
        let aligulac = data.aligulac_bo5;
        let scores = data.scores;
        let Player_Names = Object.keys(scores);
        // console.log(images)
        document.getElementById('player1').textContent = Player_Names[0];
        document.getElementById('player2').textContent = Player_Names[1];
        document.getElementById('H2H1').textContent = aligulac[0];
        document.getElementById('H2H2').textContent = aligulac[1];
        document.getElementById('Form1').textContent = aligulac[2];
        document.getElementById('Form2').textContent = aligulac[3];
        document.getElementById('WinChance1').textContent = aligulac[4][0];
        document.getElementById('WinChance2').textContent = aligulac[4][1];
        document.getElementById('MeanRes').textContent = aligulac[4][2];

        sleep(1000)
        textFit(document.getElementsByClassName("p1container"));
        textFit(document.getElementsByClassName("p2container"));
        textFit(document.getElementsByClassName("H2H1"));
        textFit(document.getElementsByClassName("H2H2"));
        textFit(document.getElementsByClassName("Form1"));
        textFit(document.getElementsByClassName("Form2"));
        textFit(document.getElementsByClassName("WinChance1"));
        textFit(document.getElementsByClassName("WinChance2"));
        textFit(document.getElementsByClassName("MeanRes"));
    } else {

    }
});





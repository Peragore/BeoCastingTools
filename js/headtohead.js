

document.getElementById("demo").onclick = function() {image("Lambo.png")};
function image(thisImage){
    let img = document.createElement("IMG");
    img.src = "../img/"+thisImage;
    document.getElementById('imageDiv').appendChild(img);
    document.getElementById("demo").innerHTML = "CLICK"
    document.write("test")
}

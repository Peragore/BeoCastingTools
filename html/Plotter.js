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

readTextFile("../json/datastream.json", function(text){
    var txtdata = JSON.parse(text);
    var supply_delta = txtdata['supply_delta_up']
    var supply_delta2 = txtdata['supply_delta_down']
    var p2_supply = txtdata['p2_supply']
    var p2_time = txtdata['p2_time']
    var p1_supply = txtdata['p1_supply']
    var p1_time = txtdata['p1_time']
    var p1_name = txtdata['p1_name'];
    var p2_name = txtdata['p2_name'];
    var p1_ground = txtdata['p1_ground'];
    var p2_ground = txtdata['p2_ground'];
    var p1_air = txtdata['p1_air'];
    var p2_air = txtdata['p2_air'];
    var p1_misc = txtdata['p1_misc'];
    var p2_misc = txtdata['p2_misc'];
    var max_val = Math.abs(Math.max(...supply_delta));
    var min_val = Math.abs(Math.min(...supply_delta));
    var ylim = Math.max(max_val, min_val);
    var xmax = Math.max(...p2_time)
    var trace1 = {
      x: p1_time,
      y: supply_delta,
      mode:"lines",
        line:{
          width: 0
        },
        fill: 'tozeroy',
        fillcolor: 'red',
        name: p1_name
    };
    var trace2 = {
      x: p1_time,
      y: supply_delta2,
      mode:"lines",
        line:{
          width: 0
        },
        fill: 'tozeroy',
        fillcolor: 'blue',
        name: p1_name
    };

    var data = [trace1, trace2];
    const layout = {
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      showlegend: false,
      xaxis: {
          visibile: true,
          showgrid: false,
          showline: false,
          tickfont: {
              size: 40
          },
          color:'#FFFFFF',
         // title: {
         //      text: 'Game Time',
         //     font: { size: 40}
         // },
          automargin: true
      },
      yaxis: {
          showgrid:false,
          tickfont:{size:40},
          color:'#FFFFFF',
          text:'Supply',
          range: [-1.2*ylim, 1.2*ylim],
         //  title: {
         //      text: 'Supply',
         //     font: { size: 40}
         // },
          automargin: true
         },
      annotations: [

        {
          x: 0.05*xmax,
          y: 0.8*ylim,
          xref: 'x',
          yref: 'y',
          text: p1_name,
          showarrow: false,
          font: {
            size:40,
            color:'#FFFFFF'
          },

        },
        {
          x: 0.05*xmax,
          y: -0.8*ylim,
          xref: 'x',
          yref: 'y',
          text: p2_name,
            font: {
            size:40,
            color:'#FFFFFF'
          },
          showarrow: false,

        }],
    };
    Plotly.newPlot("myPlot", data, layout);

    //Names
    var name_height = "20px"
    var xpos = 50;
    var div = document.createElement('p1_name');
    div.style.width = "960px";
    div.style.height = "100px";
    // div.style.background = "white";
    div.style.top = name_height;
    div.style.left = "0px";
    div.style.position = "absolute";
    div.style.fontStyle = "ESL Legend";
    div.style.color = "white";
    div.style.position = "absolute";
    div.innerHTML = p1_name;
    div.style.textAlign = "center";
    div.style.fontWeight = "bold";
    div.style.fontSize = '40pt';
    document.getElementById('p1Container').appendChild(div);

    var div = document.createElement('p2_name');
    div.style.width = "960px";
    div.style.height = "100px";
    // div.style.background = "white";
    div.style.top = name_height;
    div.style.left = "0px";
    div.style.position = "absolute";
    div.style.fontStyle = "ESL Legend";
    div.style.color = "white";
    div.style.position = "absolute";
    div.innerHTML = p2_name;
    div.style.textAlign = "center";
    div.style.fontWeight = "bold";
    div.style.fontSize = '40pt';
    document.getElementById('p2Container').appendChild(div);







    var upgrade_size = '62px';
    var text_xpos = '5px';
    var text_ypos = '-15px';
    var upgrade_offset = 70;

    var baseline_ypos =200;
    // Ground Labels
    var label = "Attack";
    var name_height = (baseline_ypos - 90).toString() + "px";
    var div = document.createElement('p1_ground');
    div.style.width = "960px";
    div.style.height = "100px";
    // div.style.background = "white";
    div.style.top = name_height;
    div.style.left = xpos.toString()+"px";
    div.style.position = "absolute";
    div.style.fontStyle = "ESL Legend";
    div.style.color = "white";
    div.style.position = "absolute";
    div.innerHTML = "Attack";
    div.style.textAlign = "left";
    div.style.fontWeight = "bold";
    div.style.fontSize = '40pt';
    document.getElementById('p1Container').appendChild(div);

    var div = document.createElement('p2_ground');
    div.style.width = "960px";
    div.style.height = "100px";
    // div.style.background = "white";
    div.style.top = name_height;
    div.style.left = xpos.toString()+"px";
    div.style.position = "absolute";
    div.style.fontStyle = "ESL Legend";
    div.style.color = "white";
    div.style.position = "absolute";
    div.innerHTML = "Attack";
    div.style.textAlign = "left";
    div.style.fontWeight = "bold";
    div.style.fontSize = '40pt';
    document.getElementById('p2Container').appendChild(div);

    var counter_up = 0;
    var counter_down = 0;
    var counter = 0;
    var indexer = 0;
    for (var i in p1_ground){
        var div = document.createElement("testDiv");
        var h1 = document.createElement('H1');
        div.name = "ground".concat(counter.toString());
        div.style.width = upgrade_size;
        div.style.height = upgrade_size;
        div.style.background = i;
        div.style.backgroundSize = "cover";
        div.style.backgroundRepeat = "no-repeat";

       if (counter*upgrade_offset + xpos > 960-5*70) {
            var ypos = (baseline_ypos+70).toString()+"px";
            var pos = (xpos + (counter-indexer)*upgrade_offset);
        } else {
            var ypos = baseline_ypos.toString()+"px";
            var pos = (xpos + (counter)*upgrade_offset);
            indexer += 1;
        }


        div.style.top = ypos;
        div.style.left = pos.toString() + "px";
        div.style.position = "absolute";

        h1.style.fontStyle = "ESL Legend";

        h1.style.color = "white";
        h1.style.position = "absolute";
        h1.style.textAlign = "center";
        h1.style.fontWeight = "bold";
        h1.style.fontSize = '15pt';
        h1.style.bottom = text_ypos;
        h1.style.left = text_xpos;
        h1.style.webkitTextStrokeColor = "black";
        h1.style.webkitTextStrokeWidth = '1px';

        h1.innerHTML = p1_ground[i];

        // div.style.
        div.appendChild(h1);
        document.getElementById("p1Container").appendChild(div);
        counter += 1;
    }

    var counter_up = 0;
    var counter_down = 0;
    var counter = 0;
    var indexer = 0;

    for (var i in p2_ground){
        var div = document.createElement("testDiv");
        var h1 = document.createElement('H1');
        div.name = "ground".concat(counter.toString());
        div.style.width = upgrade_size;
        div.style.height = upgrade_size;
        div.style.background = i;
        div.style.backgroundSize = "cover";
        div.style.backgroundRepeat = "no-repeat";


       if (counter*upgrade_offset + xpos > 960-5*70) {
            var ypos = (baseline_ypos+70).toString()+"px";
            var pos = (xpos + (counter-indexer)*upgrade_offset);
        } else {
            var ypos = baseline_ypos.toString()+"px";
            var pos = (xpos + (counter)*upgrade_offset);
            indexer += 1;
        }


        div.style.top = ypos;
        div.style.left = pos.toString() + "px";
        div.style.position = "absolute";

        h1.style.fontStyle = "ESL Legend";

        h1.style.color = "white";
        h1.style.position = "absolute";
        h1.style.textAlign = "center";
        h1.style.fontWeight = "bold";
        h1.style.fontSize = '15pt';
        h1.style.bottom = text_ypos;
        h1.style.left = text_xpos;
        h1.style.webkitTextStrokeColor = "black";
        h1.style.webkitTextStrokeWidth = '1px';

        h1.innerHTML = p2_ground[i];

        // div.style.
        div.appendChild(h1);
        document.getElementById("p2Container").appendChild(div);
        counter += 1;
    }
    // Armor
    var baseline_ypos = 380;


    var label = "Armor";
    var name_height = (baseline_ypos - 90).toString() + "px";
    var div = document.createElement('p1_air');
    div.style.width = "960px";
    div.style.height = "100px";
    // div.style.background = "white";
    div.style.top = name_height;
    div.style.left = xpos.toString()+"px";
    div.style.position = "absolute";
    div.style.fontStyle = "ESL Legend";
    div.style.color = "white";
    div.style.position = "absolute";
    div.innerHTML = label
    div.style.textAlign = "left";
    div.style.fontWeight = "bold";
    div.style.fontSize = '40pt';
    document.getElementById('p1Container').appendChild(div);

    var div = document.createElement('p2_air');
    div.style.width = "960px";
    div.style.height = "100px";
    div.style.top = name_height;
    div.style.left = xpos.toString()+"px";
    div.style.position = "absolute";
    div.style.fontStyle = "ESL Legend";
    div.style.color = "white";
    div.style.position = "absolute";
    div.innerHTML = label
    div.style.textAlign = "left";
    div.style.fontWeight = "bold";
    div.style.fontSize = '40pt';
    document.getElementById('p2Container').appendChild(div);

    var counter_up = 0;
    var counter_down = 0;
    var counter = 0;
    var indexer = 0;

    for (var i in p1_air){
        var div = document.createElement("testDiv");
        var h1 = document.createElement('H1');
        div.name = "ground".concat(counter.toString());
        div.style.width = upgrade_size;
        div.style.height = upgrade_size;
        div.style.background = i;
        div.style.backgroundSize = "cover";
        div.style.backgroundRepeat = "no-repeat";


       if (counter*upgrade_offset + xpos > 960-5*70) {
            var ypos = (baseline_ypos+70).toString()+"px";
            var pos = (xpos + (counter-indexer)*upgrade_offset);
        } else {
            var ypos = baseline_ypos.toString()+"px";
            var pos = (xpos + (counter)*upgrade_offset);
            indexer += 1;
        }


        div.style.top = ypos;
        div.style.left = pos.toString() + "px";
        div.style.position = "absolute";

        h1.style.fontStyle = "ESL Legend";

        h1.style.color = "white";
        h1.style.position = "absolute";
        h1.style.textAlign = "center";
        h1.style.fontWeight = "bold";
        h1.style.fontSize = '15pt';
        h1.style.bottom = text_ypos;
        h1.style.left = text_xpos;
        h1.style.webkitTextStrokeColor = "black";
        h1.style.webkitTextStrokeWidth = '1px';

        h1.innerHTML = p1_air[i];

        // div.style.
        div.appendChild(h1);
        document.getElementById("p1Container").appendChild(div);
        counter += 1;
    }

    var counter_up = 0;
    var counter_down = 0;
    var counter = 0;
    var indexer = 0;
    for (var i in p2_air){
        var div = document.createElement("testDiv");
        var h1 = document.createElement('H1');
        div.name = "ground".concat(counter.toString());
        div.style.width = upgrade_size;
        div.style.height = upgrade_size;
        div.style.background = i;
        div.style.backgroundSize = "cover";
        div.style.backgroundRepeat = "no-repeat";


       if (counter*upgrade_offset + xpos > 960-5*70) {
            var ypos = (baseline_ypos+70).toString()+"px";
            var pos = (xpos + (counter-indexer)*upgrade_offset);
        } else {
            var ypos = baseline_ypos.toString()+"px";
            var pos = (xpos + (counter)*upgrade_offset);
            indexer += 1;
        }


        div.style.top = ypos;
        div.style.left = pos.toString() + "px";
        div.style.position = "absolute";

        h1.style.fontStyle = "ESL Legend";

        h1.style.color = "white";
        h1.style.position = "absolute";
        h1.style.textAlign = "center";
        h1.style.fontWeight = "bold";
        h1.style.fontSize = '15pt';
        h1.style.bottom = text_ypos;
        h1.style.left = text_xpos;
        h1.style.webkitTextStrokeColor = "black";
        h1.style.webkitTextStrokeWidth = '1px';

        h1.innerHTML = p2_air[i];

        // div.style.
        div.appendChild(h1);
        document.getElementById("p2Container").appendChild(div);
        counter += 1;
    }

    //Misc
    var baseline_ypos = 550;
    var label = "Misc";
    var name_height = (baseline_ypos - 90).toString() + "px";
    var div = document.createElement('p1_misc');
    div.style.width = "960px";
    div.style.height = "100px";
    // div.style.background = "white";
    div.style.top = name_height;
    div.style.left = xpos.toString()+"px";
    div.style.position = "absolute";
    div.style.fontStyle = "ESL Legend";
    div.style.color = "white";
    div.style.position = "absolute";
    div.innerHTML = label;
    div.style.textAlign = "left";
    div.style.fontWeight = "bold";
    div.style.fontSize = '40pt';
    document.getElementById('p1Container').appendChild(div);

    var div = document.createElement('p2_misc');
    div.style.width = "960px";
    div.style.height = "100px";
    // div.style.background = "white";
    div.style.top = name_height;
    div.style.left = xpos.toString()+"px";
    div.style.position = "absolute";
    div.style.fontStyle = "ESL Legend";
    div.style.color = "white";
    div.style.position = "absolute";
    div.innerHTML = label;
    div.style.textAlign = "left";
    div.style.fontWeight = "bold";
    div.style.fontSize = '40pt';
    document.getElementById('p2Container').appendChild(div);

    var counter_up = 0;
    var counter_down = 0;
    var counter = 0;
    var indexer = 0;
    for (var i in p1_misc){
        var div = document.createElement("testDiv");
        var h1 = document.createElement('H1');
        div.name = "ground".concat(counter.toString());
        div.style.width = upgrade_size;
        div.style.height = upgrade_size;
        div.style.background = i;
        div.style.backgroundSize = "cover";
        div.style.backgroundRepeat = "no-repeat";
        if (counter*upgrade_offset + xpos > 960-5*70) {
            var ypos = (baseline_ypos+70).toString()+"px";
            var pos = (xpos + (counter-indexer)*upgrade_offset);
        } else {
            var ypos = baseline_ypos.toString()+"px";
            var pos = (xpos + (counter)*upgrade_offset);
            indexer += 1;
        }


        div.style.top = ypos;
        div.style.left = pos.toString() + "px";
        div.style.position = "absolute";

        h1.style.fontStyle = "ESL Legend";

        h1.style.color = "white";
        h1.style.position = "absolute";
        h1.style.textAlign = "center";
        h1.style.fontWeight = "bold";
        h1.style.fontSize = '15pt';
        h1.style.bottom = text_ypos;
        h1.style.left = text_xpos;

        h1.innerHTML = p1_misc[i];
        h1.style.webkitTextStrokeColor = "black";
        h1.style.webkitTextStrokeWidth = '1px';

        // div.style.
        div.appendChild(h1);
        document.getElementById("p1Container").appendChild(div);
        counter += 1;
    }

    var counter_up = 0;
    var counter_down = 0;
    var counter = 0;
    var indexer = 0;
    for (var i in p2_misc){
        var div = document.createElement("testDiv");
        var h1 = document.createElement('H1');
        div.name = "ground".concat(counter.toString());
        div.style.width = upgrade_size;
        div.style.height = upgrade_size;
        div.style.background = i;
        div.style.backgroundSize = "cover";
        div.style.backgroundRepeat = "no-repeat";
        if (counter*upgrade_offset + xpos > 960-5*70) {
            var ypos = (baseline_ypos+70).toString()+"px";
            var pos = (xpos + (counter-indexer)*upgrade_offset);
        } else {
            var ypos = baseline_ypos.toString()+"px";
            var pos = (xpos + (counter)*upgrade_offset);
            indexer += 1;
        }


        div.style.top = ypos;
        div.style.left = pos.toString() + "px";
        div.style.position = "absolute";

        h1.style.fontStyle = "ESL Legend";

        h1.style.color = "white";
        h1.style.position = "absolute";
        h1.style.textAlign = "center";
        h1.style.fontWeight = "bold";
        h1.style.fontSize = '15pt';
        h1.style.bottom = text_ypos;
        h1.style.left = text_xpos;

        h1.innerHTML = p2_misc[i];
        h1.style.webkitTextStrokeColor = "black";
        h1.style.webkitTextStrokeWidth = '1px';

        // div.style.
        div.appendChild(h1);
        document.getElementById("p2Container").appendChild(div);
        counter += 1;
    }

});


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

function makeArr(startValue, stopValue, cardinality) {
  var arr = [];
  var step = (stopValue - startValue) / (cardinality - 1);
  for (var i = 0; i < cardinality; i++) {
    arr.push(Math.round(startValue + (step * i)));
  }
  return arr;
}

readTextFile("../json/datastream.json", function(text){
    var txtdata = JSON.parse(text);
    var supply_delta = txtdata['supply_delta_up']
    var supply_delta2 = txtdata['supply_delta_down']
    var p2_time = txtdata['p2_time']
    var p1_time = txtdata['p1_time']
    var p1_name = txtdata['p1_name'];
    var p2_name = txtdata['p2_name'];
    var p1_upgrade_time = txtdata['p1_upgrade_time']
    var p2_upgrade_time = txtdata['p2_upgrade_time']
    var p1_upgrade_stream = txtdata['p1_upgrade_stream']
    var p2_upgrade_stream = txtdata['p2_upgrade_stream']
    var max_val = Math.abs(Math.max(...supply_delta));
    var min_val = Math.abs(Math.min(...supply_delta));
    var ylim = Math.max(max_val, min_val);
    var xmax = Math.max(...p2_time)
    var upgrade_array = []

    var last_xloc = p1_upgrade_stream[Object.keys(p1_upgrade_stream)[0]];
    var xloc = p1_upgrade_stream[Object.keys(p1_upgrade_stream)[0]];
    var yloc = 0.5;
    var image_size = 0.07; //Math.round(p1_upgrade_time.slice(-1)/2);
    var counter = 0;
    var img_opacity = "0.90"
    for (var upgrade in p1_upgrade_stream){
        var image_path = upgrade.split('url(')[1].split(')')[0];
        xloc = p1_upgrade_stream[upgrade]/p1_time.slice(-1);// - image_size/2;
        if (Math.abs(last_xloc-xloc) < image_size/9 && counter > 0){
            yloc += image_size;
        } else {
            yloc = 0.5;
        }
        if (p1_upgrade_stream[upgrade] < p1_time.slice(-1))
        {
            upgrade_array.push({
                "source": image_path,
                "xref": "paper",
                "yref": "paper",
                "x": xloc,
                "y": yloc,
                "sizex": image_size,
                "sizey": image_size,
                "xanchor": "left",
                "yanchor": "bottom",
                "opacity": img_opacity
            });
        }
        counter += 1;
        last_xloc = xloc;
    }

    var last_xloc = p2_upgrade_stream[Object.keys(p2_upgrade_stream)[0]];
    var xloc = p2_upgrade_stream[Object.keys(p2_upgrade_stream)[0]];
    var yloc = .5;
    var counter = 0;
    for (var upgrade in p2_upgrade_stream){
        var image_path = upgrade.split('url(')[1].split(')')[0];
        xloc = p2_upgrade_stream[upgrade]/p2_time.slice(-1);
        if (Math.abs(last_xloc-xloc) < image_size/3 && counter > 0){
            yloc -= image_size;
        } else {
            yloc = .5-image_size;
        }
        console.log(yloc)
        console.log(xloc)
        upgrade_array.push({
            "source": image_path,
            "xref": "paper",
            "yref": "paper",
            "x": xloc,
            "y": yloc,
            "sizex": image_size,
            "sizey": image_size,
            "xanchor": "left",
            "yanchor": "bottom",
            "opacity": img_opacity
        });
        counter += 1;
        last_xloc = xloc;
    }
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
    var yticks = makeArr(-ylim, ylim, 7)
    // yticks.splice(3, 0, 0)
    const ytick_abs = (array) => {
        return array.map(Math.abs);
    }
    var ytick_names = ytick_abs(yticks)
    console.log(p1_time.slice(-1));
    const layout = {
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      showlegend: false,
      // margin:{l:60},
      xaxis: {
          visibile: true,
          showgrid: false,
          showline: false,
          range:[-.1,Math.round(p1_time.slice(-1))],
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
          tickfont:{
              family: "Roboto",
              size:40},
          position: -0.1,
          color:'#FFFFFF',
          text:'Supply',
          range: [-1.1*ylim, 1.1*ylim],
          tickvals: yticks,
          ticktext: ytick_names,
         //  title: {
         //      text: 'Supply',
         //     font: { size: 40}
         // },
          automargin: true
         },
      annotations: [

        {
          x: 0.01*xmax,
          y: 0.8*ylim,
          xref: 'x',
          yref: 'y',
          text: p1_name,
          xanchor: "left",
          showarrow: false,
          font: {
            size:40,
            color:'#FFFFFF'
          },

        },
        {
          x: 0.01*xmax,
          y: -0.8*ylim,
          xref: 'x',
          yref: 'y',
          xanchor: "left",
          text: p2_name,
            font: {
            size:40,
            color:'#FFFFFF'
          },
          showarrow: false,

        }],
        images:  upgrade_array,
    };

    var trace1 = {
      x: p1_time,
      y: supply_delta,
      mode:"lines",
        line:{
          width: 6,
          color: 'red'
        },

        name: p1_name
    };
    var trace2 = {
      x: p1_time,
      y: supply_delta2,
      mode:"lines",
        line:{
          width: 6,
          color: 'blue'

        },
        name: p1_name
    };

    var data2 = [trace1, trace2];
    const layout2 = {
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

    };
    Plotly.newPlot("myPlot", data, layout);
    console.log(document.getElementsByClassName("yaxislayer-above")[0])


});


google.charts.load('current', {
  callback: function () {
    var rawData = [
      [0, 0],
      [1, 2],
      [2, 1],
      [3, 4],
      [4, 2],
      [5, 8],
      [6, 3],
      [7, 16],
      [8, 4],
      [9, 32]
    ];

    var data = new google.visualization.DataTable({
      "cols": [
        {"id":"","label":"X","type":"number"},
        {"id":"","label":"Y","type":"number"}
      ]
    });

    var options = {
      pointSize: 4,
      animation:{
        startup: true,
        duration: 200,
        easing: 'in'
      },
      legend: 'none',
      hAxis: {
        title: 'Days',
        viewWindow: {
          min: 0,
          max: 9
        }
      },
      vAxis: {
        title: 'Patients',
        viewWindow: {
          min: 0,
          max: 32
        }
      },
      series: {
           0: { color: "#18d38e" },
         }
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

    drawChart();
    setInterval(drawChart, 200);

    var rowIndex = 0;
    function drawChart() {
      if (rowIndex < rawData.length) {
        data.addRow(rawData[rowIndex++]);
        chart.draw(data, options);
      }
    }
  },
  packages:['corechart']
});

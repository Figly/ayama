
var mock_data = [['Year', 'Future'],[0,100],[1,110],[2,125],[3,150]]

google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(drawChart);

function getInputValue(){

	var pre_data = [['Year', 'Future']];
    var I = document.getElementById("initial_investment").value;
    var T = document.getElementById("years").value;
    var R = document.getElementById("interest").value;

    for (i = 0; i <= T; i++) {
  		pre_data.push([i,I*Math.pow((1+(R/100)),i)])
		}
    console.log(pre_data);
    this.drawChart(pre_data);
    }


function drawChart(pre_data) {

	pre_data = pre_data || mock_data;
    var data = google.visualization.arrayToDataTable(pre_data);

    var options = {
    	chart: {
        	title: 'Awe',
        	subtitle: 'Awe',
      		},
      	bars: 'vertical'
    	};

    var chart = new google.charts.Bar(document.getElementById('barchart_material'));

    chart.draw(data, google.charts.Bar.convertOptions(options));

    var btns = document.getElementById('btn-group');
    }


var mock_data = [['Year', 'Future'],[0,100],[1,110],[2,125],[3,150]]

google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(drawChart2);

function getInputValue2(){

    var pre_data = [['Year', 'Future']];
    var P = document.getElementById("savings_amount_per_period").value;
    var age = document.getElementById("age").value;
    var retire = document.getElementById("retire").value;
    var I = document.getElementById("interest2").value;
    var salary = document.getElementById("salary_at_retirement").value;
    var ob = document.getElementById("initial_investment1").value || 0;
    var balance;
    console.log(balance);

    T = retire  - age;
    var r = I/1200;
    var t;

    for (i = 1; i <= T; i++) {
        t = i*12;
        brac = Math.pow(1+r,t);
        numerator = P*(brac - 1);
        denumerator = r;
        bal = ob*Math.pow((1+(I/100)),i)
        balance = bal + numerator/denumerator;
        pre_data.push([Number(age) + Number(i),balance]);
        }

    for(i = 1; i <= 35; i ++){
        t = 12;
        brac = Math.pow(1+r,t);
        numerator = salary*(brac - 1);
        denumerator = r;
        balance = balance*brac - (salary*12)*(1+r);
        if(balance > 0){
        pre_data.push([Number(retire) + Number(i),balance]);
    }
    }

    console.log(pre_data);
    this.drawChart2(pre_data);
    }


function drawChart2(pre_data) {

    pre_data = pre_data || mock_data;
    var data = google.visualization.arrayToDataTable(pre_data);

    var options = {
        chart: {
            title: 'Monthly Payment Calculator',
            subtitle: 'Awe',
            },
        bars: 'vertical'
        };

    var chart = new google.charts.Bar(document.getElementById('monthly_payment'));

    chart.draw(data, google.charts.Bar.convertOptions(options));

    var btns = document.getElementById('btn-group');
    }

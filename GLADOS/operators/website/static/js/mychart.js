var ctx = document.getElementById("myChart").getContext("2d");
    var lineChart = new Chart(ctx,{
    type:"line",
    data:{
        labels : {{chart_labels | safe}},
        datasets: [
            {
                label : "Data Points",
                data : {{ chart_values | safe}},
                fill: false,
                borderColor: "rgb(75,192,192)",
                lineTension:0.1
            }
        ]
    },
    options:{
        responsive: false
    }});
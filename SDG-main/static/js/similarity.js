var similarData = [];
var weightData = [];
var amountData = [];

function setTableData(data){
    $('#SDG_Table').DataTable().clear().destroy();
    $('#SDG_Table').DataTable({
        data: data,
        "columns":[
            {"data":"Keywords"},
            {"data":"SDGKeyphrase"},
            {"data":"SDGzh"},
            {"data":"Similarity"},
            {"data":"Weight"},
            {"data":"SDG_NO"},
        ]  
    });
}

function setChartData(data){
    for(var i=0;i<data.length;i++){
        similarData[i]={
            name: data[i]['SDG_NO'],
            y: data[i]['Similarity']
        }
        weightData[i]={
            name: data[i]['SDG_NO'],
            y: data[i]['Weight']
        }
        amountData[i]={
            name: data[i]['SDG_NO'],
            y: data[i]['Size']
        }
    }
    chart('sim_column_chart', similarData,'Similarity','column');
    chart('weight_column_chart', weightData,'Weight','column');
    chart('amount_column_chart', amountData,'Amount','pie');
}

function chart(id,data,label,chart_type){
    Highcharts.chart(id, {
        chart: {
            type: chart_type
        },
        title: {
            text: label + ' Chart'
        },
        subtitle: {
            text: 'Subtitle'
        },
        accessibility: {
            announceNewData: {
            enabled: true
            }
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
            text: 'Total percent market share'
            }

        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y:.1f}'
            }
            }
        },

        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> of total<br/>'
        },

        series: [
            {
            name: label,
            colorByPoint: true,
            data: data
            }
        ] 
    });
}

$(document).ready(function () {
            
    $("#submit").click(function () {
        var form_data = new FormData();
        form_data.append('text',$("#wordTextarea").val());
        form_data.append('lang',$("#lang").val());
        // alert($("#lang").val());
        $("#body").loading();
        $.ajax({
            type: "POST",
            url: "/get_table_data",
            data: form_data,
            contentType: false,
            processData: false,
            dataType: "json",
        }).done(function(data){
            console.log(data)
            tdata = data.tableData
            cdata = data.chartData
            setTableData(tdata);
            document.getElementById("table").style.display="";
            setChartData(cdata);
        })
    });

});
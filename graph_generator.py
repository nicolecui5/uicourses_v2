#!/usr/bin/env python

pie_html = '''
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    google.charts.load('current', {
        'packages': ['corechart']
    });
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ['Task', 'Percentage'],
            ['Lecture', %s],
            ['Discussion', %s],
            ['Homework', %s],
            ['Lab', %s],
            ['Quiz', %s],
            ['Midterms', %s],
            ['Project', %s],
            ['Final', %s],
            ['ExtraCredit', %s],
            ['Other', %s]
        ]);
        var options = {
            title: 'Percentage Breakdown',
            colors: ['#99CBE5', '#A2D4D5', '#F8DED8', '#F8B5BB', '#A69C94', '#99CBE5', '#A2D4D5', '#F8DED8', '#F8B5BB', '#A69C94']
        };
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
    }
</script>

<div style="float:cen;clear:both;">
    <div id="piechart" style="width: 500px; height: 300px; float:left;clear:left;"></div>
</div>
'''

bar_html = '''
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    google.charts.load("current", {
        packages: ["corechart"]
    });
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ["Element", "Difficulty", {
                role: "style"
            }],
            ['Lecture', %f, '#99CBE5'],
            ['Discussion', %f, '#A2D4D5'],
            ['Homework', %f, '#F8DED8'],
            ['Lab', %f, '#F8B5BB'],
            ['Quiz', %f, '#A69C94'],
            ['Midterms', %f, '#99CBE5'],
            ['Project', %f, '#A2D4D5'],
            ['Final', %f, '#F8DED8'],
        ]);
        var view = new google.visualization.DataView(data);
        var options = {
            title: "Difficulty",
            bar: {
               
            },
            legend: {
                position: "none"
            },
        };
        var chart = new google.visualization.BarChart(document.getElementById("barchart_values"));
        chart.draw(view, options);
    }
</script>
<div style="float:cen;clear:both;">
    <div id="barchart_values" style="width: 500px; height: 300px; float:left;clear:right;"></div>
</div>
'''


def graph_gen (subject, code, pct_list, diff_list):
    fh = open("/home/uicourses/public_html/graphs/" + subject.upper() + code + "_pie.html", "w")
    ret = pie_html % pct_list
    fh.write(ret)
    fh.close()
    fh = open("/home/uicourses/public_html/graphs/" + subject.upper() + code + "_bar.html", "w")
    ret = bar_html % diff_list  # (0,1,2,3,4,5,6,7)
    fh.write(ret)
    fh.close()

function stats_pie (target, title, rows, data) {
    $.jqplot(target, [data], {
		 title: title,
		 grid: {
		     drawBorder: false,
		     drawGridlines: false,
		     background: '#ffffff',
		     shadow: false
		 },
		 seriesDefaults:{
		     renderer: $.jqplot.PieRenderer,
		     rendererOptions: {
			 showDataLabels: true
		     },
		 },
		 legend: {
		     show: true,
		     rendererOptions: {
			 numberRows: rows
		     },
		     location: 's'
		 },
		 cursor: {
		     show: false
		 }
	     });
}

function stats_bar (target, title, ticks, counts) {
    $.jqplot(target, [counts], {
		 title: title,
		 seriesDefaults: {
                     renderer: $.jqplot.BarRenderer,
		     rendererOptions: {
			 varyBarColor: true
		     }
		 },
		 axes: {
                     xaxis: {
			 renderer: $.jqplot.CategoryAxisRenderer,
			 ticks: ticks
                     },
		     yaxis: {
			 min: 0,
		     }
		 },
		 cursor: {
		     show: false
		 }
	     });
}

function stats_setup (src, tick_field) {
    res = {
	pie: [],
	bar: {
	    ticks: [],
	    counts: []
	}
    };

    $.each (src, function (index, value) {
		res.pie.push ([value[tick_field], value.count]);
		res.bar.ticks.push (value[tick_field]);
		res.bar.counts.push (value.count);
	    });

    return res;
}

function time_plot (src) {
    $.jqplot('time_plot', [src], { 
		 title: 'Hourly messages over time', 
		 series:[
		     {
			 label: "Messages",
			 showMarker: true,
		     }
		 ],
		 axes: {
		     yaxis: {
			 min: 0,
			 label: "Messages received",
			 labelRenderer: $.jqplot.CanvasAxisLabelRenderer,

			 labelOptions: {
			     angle: -90,
			 },
		     },
		     xaxis: {
			 tickRenderer: $.jqplot.CanvasAxisTickRenderer,
			 tickOptions: {
			     showLabel: true,
			     isMinorTick: true,
			     formatString: "%F, %Hh"
			 },
			 labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
			 label: "Date",
			 autoscale: true,
			 renderer: $.jqplot.DateAxisRenderer,
		     },
		 },
		 cursor: {
		     followMouse: true,
		     showTooltipDataPosition: true,
		     showVerticalLine: true
		 }
	     });
}

$(document).ready (
    function () {
	if (typeof host_stats !== 'undefined') {
	    r = stats_setup (host_stats, "host");

	    stats_pie ("host_stats_pie", "Host message contribution", Math.max (1, r.bar.counts.length / 5), r.pie);
	    stats_bar ("host_stats_bar", "Messages / Host", r.bar.ticks, r.bar.counts);
	}
	if (typeof prog_stats !== 'undefined') {
	    r = stats_setup (prog_stats, "program.name");

	    stats_pie ("prog_stats_pie", "Program message contribution", Math.max (1, r.bar.counts.length / 5), r.pie);
	}
	if (typeof time_stats !== 'undefined') {
	    r = [];
	    d = time_stats.sort (function (a, b) {
				     return a.date - b.date;
				 });
	    $.each (d, function (index, value) {
			t = new Date (value.date * 1000);
			r.push ([t.getFullYear () + '-' + (t.getMonth() + 1) + '-' + t.getDate () + ' ' + t.getHours() + ':00:00', value.count]);
		    });
	    time_plot (r);
	}
    });

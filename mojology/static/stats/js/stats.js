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

function stats_bar (target, title, data) {
    $.jqplot(target, [data], {
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
    var res = {
	data: [],
	ts: 0
    };

    $.each (src, function (index, value) {
		res.data.push ([value._id, value.value.count]);
		res.ts = value.value.stamp['$date'];
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

function set_timestamp (ts) {
    t = new Date (ts);

    $("time").html (t.toString ());
}

$(document).ready (
    function () {
	$.jqplot.config.enablePlugins = true;
	var r;

	if (typeof host_stats !== 'undefined') {
	    r = stats_setup (host_stats);

	    stats_pie ("host_stats_pie", "Host message contribution", Math.max (1, r.data.length / 5), r.data);
	    stats_bar ("host_stats_bar", "Messages / Host", r.data);
	}
	if (typeof prog_stats !== 'undefined') {
	    r = stats_setup (prog_stats);

	    stats_pie ("prog_stats_pie", "Program message contribution", Math.max (1, r.data.length / 5), r.data);
	}
	if (typeof time_stats !== 'undefined') {
	    r = {
		data: [],
		ts: 0
	    };
	    d = time_stats.sort (function (a, b) {
				     return a.ts - b.ts;
				 });
	    $.each (d, function (index, value) {
			t = new Date (value['_id'] * 1000);
			r.data.push ([t.getFullYear () + '-' + (t.getMonth() + 1) + '-' + t.getDate () + ' ' + t.getHours() + ':00:00', value.value.count]);
			r.ts = value['_id'] * 1000;
		    });
	    time_plot (r.data);
	}
	set_timestamp (r.ts);
    });

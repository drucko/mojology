function stats_pie (target, legend, data) {
    $.plot (target, data, {
		series: {
		    pie: {
			show: true,
			radius: 1,
			stroke: {
			    color: "#000"
			},
			label: {
			    show: true,
			    radius: 2/3,
			    treshold: 0.1,
			    formatter: function (label, series) {
				return '<div class="pie-label">' + label + '<br>' + Math.round (series.percent) + '%</div>';
			    },
			    background: {
				color: "#000",
				opacity: 0.5
			    }
			}
		    }
		},
		grid: {
		    hoverable: true,
		},
		legend: {
		    container: legend
		},
	    });
    legend.find ("table").css ("font-size", "");
    target.bind ("plothover", function (event, pos, item) {
		     if (!item)
			 return;
		     l = target.find (".pieLabelBackground");
		     l.hide();
		     x = l[item.seriesIndex];
		     $(x).css ("visibility", "visible").show();

		     l = target.find (".pie-label");
		     l.hide();
		     x = l[item.seriesIndex];
		     $(x).css ("opacity", 1).show();
		 });
    target.bind ("mouseout", function () {
		     target.find (".pie-label").hide ();
		     target.find (".pieLabelBackground").hide ();
		 });
};

function stats_setup (src, tick_field) {
    var res = {
	data: [],
	ts: 0
    };

    $.each (src, function (index, value) {
		res.data.push ({ label: value._id, data: value.value.count});
		res.ts = value.value.stamp['$date'];
	    });

    return res;
}

function time_plot (src) {
}

function set_timestamp (ts) {
    t = new Date (ts);

    $("time").html (t.toString ());
}

$(document).ready (
    function () {
	var r;

	if (typeof host_stats !== 'undefined') {
	    r = stats_setup (host_stats);

	    stats_pie ($("#host_stats_pie"), $("#host_stats_legend"), r.data);
	}
	if (typeof prog_stats !== 'undefined') {
	    r = stats_setup (prog_stats);

	    stats_pie ($("#prog_stats_pie"), $("#prog_stats_legend"), r.data);
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
			r.ts = value.value.stamp['$date'];
		    });
	    //time_plot (r.data);
	}
	set_timestamp (r.ts);
    });

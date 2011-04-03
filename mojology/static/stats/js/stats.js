max_slices = 20;

function stats_pie (target, legend, data) {
    var threshold = null;

    if (data.data[max_slices - 1]) {
	threshold = data.data[max_slices - 1].data / data.total;
    }

    $.plot (target, data.data, {
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
				return '<div class="pie-label">' + label + '<br>' + series.data[0][1] + ' (' + Math.round (series.percent) + '%)</div>';
			    },
			    background: {
				color: "#000",
				opacity: 0.5
			    }
			},
			combine: {
			    color: "#999",
			    threshold: threshold
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
	ts: 0,
	total: 0
    };

    $.each (src, function (index, value) {
		res.data.push ({ label: value._id, data: value.value.count});
		res.ts = value.value.stamp['$date'];
		res.total += value.value.count;
	    });
    res.data = res.data.sort (function (a, b) { return b.data - a.data; });

    return res;
}

function stats_time (target, data) {
    $.plot (target, [data], {
		xaxis: {
		    mode: "time",
		    timeformat: "%y-%0m-%0d",
		    minTickSize: [1, "day"],
		},
		grid: {
		    hoverable: true
		},
		series: {
		    lines: {
			show: true,
			fill: true
		    },
		    points: {
			show: true
		    }
		}
	    });
    
    function showTooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css( {
							       position: 'absolute',
							       display: 'none',
							       top: y + 5,
							       left: x + 5,
							       border: '1px solid #fdd',
							       padding: '2px',
							       'background-color': '#fee',
							       opacity: 0.80
							   }).appendTo("body").fadeIn(200);
    }

    function pad2 (number) {
        return (number < 10 ? '0' : '') + number
    }
 
    var previousPoint = null;
    target.bind("plothover", function (event, pos, item) {
        $("#x").text(pos.x.toFixed(2));
        $("#y").text(pos.y.toFixed(2));
 
        if ($("#enableTooltip:checked").length > 0 || 1) {
            if (item) {
                if (previousPoint != item.dataIndex) {
                    previousPoint = item.dataIndex;
                    
                    $("#tooltip").remove();
                    var x = new Date (item.datapoint[0]);
                    var y = item.datapoint[1];
		    var d = x.getFullYear () + '-' + pad2 (x.getMonth() + 1) + '-' + pad2 (x.getDate ()) + ' ' + pad2 (x.getHours()) + 'h';
                    
                    showTooltip(item.pageX, item.pageY,
                                "Log messages at " + d + ": " + y);
                }
            }
            else {
                $("#tooltip").remove();
                previousPoint = null;            
            }
        }
    });
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

	    stats_pie ($("#host_stats_pie"), $("#host_stats_legend"), r);
	}
	if (typeof prog_stats !== 'undefined') {
	    r = stats_setup (prog_stats);

	    stats_pie ($("#prog_stats_pie"), $("#prog_stats_legend"), r);
	}
	if (typeof time_stats !== 'undefined') {
	    r = {
		data: [],
		ts: 0
	    };
	    d = time_stats.sort (function (a, b) {
				     return a['_id'] - b['_id'];
				 });
	    $.each (d, function (index, value) {
			r.data.push ([value['_id'], value.value.count]);
			r.ts = value.value.stamp['$date'];
		    });
	    stats_time ($("#time_stats"), r.data);
	}
	set_timestamp (r.ts);
    });

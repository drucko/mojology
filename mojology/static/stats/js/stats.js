function host_stats_pie (data) {
    $.jqplot('host_stats_pie', [data], {
		 title: "Host message contribution",
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
			 numberRows: 1
		     },
		     location: 's'
		 },
	     });
}

function host_stats_bar (hosts, counts) {
    $.jqplot('host_stats_bar', [counts], {
		 title: "Messages / Host",

		 seriesDefaults: {
                     renderer: $.jqplot.BarRenderer,
		     rendererOptions: {
			 varyBarColor: true,
		     }
		 },
		 axes: {
                     xaxis: {
			 renderer: $.jqplot.CategoryAxisRenderer,
			 ticks: hosts
                     },
		     yaxis: {
			 min: 0,
		     }
		 }
	     });
}

$(document).ready (function () {
		       var hpie = [];
		       var hbar = {
			   hosts: [],
			   counts: []
		       };
		       $.each (host_stats, function (index, value) {
				   hpie.push ([value.host, value.count]);
				   hbar.hosts.push (value.host);
				   hbar.counts.push (value.count);
			       });
		       host_stats_pie (hpie);
		       host_stats_bar (hbar.hosts, hbar.counts);
		   });


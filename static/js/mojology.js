$(document).ready (function () {
		       function log_details_set (self, data) {
			   $(".log_details").remove ();
			   $(self).after (data);
			   $(".log_details").css ({display: "none"}).fadeIn (500, function () {
										 $("body").removeClass ('busy');
									     });
		       }
		       function log_details_change (self, data) {
			   if ($(".log_details").attr ('class')) {
			       $(".log_details").fadeOut (500, function () { log_details_set (self, data); });
			   } else {
			       log_details_set (self, data);
			   }
		       }
		       function log_details_fiddle (obj) {
			   $("body").addClass ('busy');
			   if (obj.next ().attr ('class') == "log_details") {
			       $(".log_details").fadeToggle ("fast", function () { $("body").removeClass ('busy'); });
			       return;
			   }
			   $.get ($SCRIPT_ROOT + "/log/" + obj.attr ('data-id') + "/dyn",
				  function (data) {
				      log_details_change (obj, data);
				  });
		       };

		       $("tr.clickable").click (function (event) {
						    event.stopPropagation ();
						    log_details_fiddle ($(this));
						});
		       $("a.hidden").click (function (event) {
						event.preventDefault ();
						event.stopPropagation ();
						log_details_fiddle ($(this).closest ("tr"));
					    });

		       $.each ($("#main_table > thead tr").children (), function (k ,v) {
				   $(v).css ({ width: $(v).width () });
		       });

		       $("#slider").slider ({
						min: 1,
						value: $("#page_counter").html (),
						max: $("#maxpage").html (),
						slide: function (event, widget) {
						    $("#page_counter").html (widget.value);
						},
						change: function (event, widget) {
						    window.history.replaceState ({
										     page: widget.value,
										 }, "", $BASE_URL + "page/" + widget.value);
						    $("#main_table").load ($BASE_URL + "page/" + widget.value +" #main_table");
						}
					    });
});

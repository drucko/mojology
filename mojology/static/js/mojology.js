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

		       $("tr.clickable").live ("click", function (event) {
						   event.stopPropagation ();
						   log_details_fiddle ($(this));
					       });
		       $("a.hidden").live ("click", function (event) {
					       event.preventDefault ();
					       event.stopPropagation ();
					       log_details_fiddle ($(this).closest ("tr"));
					   });

		       $.each ($("#main_table > thead tr").children (), function (k ,v) {
				   $(v).css ({ width: $(v).width () });
		       });

		       $("#slider").slider ({
						min: 1,
						value: parseInt ($("#page_counter").html (), 10),
						max: parseInt ($("#maxpage").html (), 10),
						slide: function (event, widget) {
						    $("#page_counter").html (widget.value);
						},
						change: function (event, widget) {
						    $("body").addClass ("busy");
						    if (window.history.replaceState)
							window.history.replaceState ({
											 page: widget.value,
										     }, "", $BASE_URL + "page/" + widget.value);
						    $("nav").fadeOut (250);
						    $("#main_table").fadeOut (500, function () {
										  $.get ($BASE_URL + "page/" + widget.value,
											 function (r) {
											     $("nav").html ($(r).find ("nav").html ()).fadeIn (500);
											     $("#main_table").html ($(r).find ("#main_table").html ()).
												 fadeIn (500, function () {
													     $("body").removeClass ("busy");
													 });
											 });
									      });
						}
					    });
});

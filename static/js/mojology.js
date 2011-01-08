$(document).ready (function () {
		       function log_details_set (self, data) {
			   $("#log_details").remove ();
			   $(self).after ("<tr id=\"log_details\" style=\"display: none;\"><td colspan=\"5\">" + data + "</td></tr>");
			   $("#log_details").fadeIn (500);
		       }
		       function log_details_change (self, data) {
			   if ($("#log_details").attr ('id')) {
			       $("#log_details").fadeOut (500, function () { log_details_set (self, data); });
			   } else {
			       log_details_set (self, data);
			   }
		       }
		       function log_details_fiddle (obj) {
			   if (obj.next ().attr ('id') == "log_details") {
			       $("#log_details").fadeToggle ("fast");
			       return;
			   }
			   $.get ("/log/" + obj.attr ('id') + "/dyn",
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
});

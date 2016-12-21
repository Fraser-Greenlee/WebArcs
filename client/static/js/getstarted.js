/*jshint multistr: true */

function getstarted() {
	var feed = page;
	if (feed in gajax) {
		gajax[feed].abort();
	}
	$("#feedpage").append(loading);
	gajax[feed] = $.ajax({
		type: 'POST',
		url: "f/parsers/displaybars",
		async: true,
		success:
			function (html) {
				$("#feedpage #loading").remove();
				$("#feedpage").append('\
				<div class="msgbox">\
					<h1>Add Sites Below</h1>\
					<p>These will appear in your feed.</p>\
				</div>\
				'+html);
			}
	});
}

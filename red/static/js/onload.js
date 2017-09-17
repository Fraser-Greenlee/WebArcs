
function loadfeed() {
	$("#Feed").html('<div id="loading"></div>');
	$.ajax({
		type: 'POST',
		url: 'feed',
		async: true,
		success:
			function (returnedData) {
				$("#Feed").html(returnedData);
			}
	});
}

function loadsubs() {
	$("#Subs").html(`
		Unfinished
	`);
}

loadfeed();
loadsubs();

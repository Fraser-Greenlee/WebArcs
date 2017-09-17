

//!!!! globals.js


function viewFeed() {
	$("#feedbut").addClass('selected');
	$("#subsbut").removeClass('selected');
	$("#Subs").removeClass('open');
	$("#Feed").addClass('open');
}

function viewSubs() {
	$("#feedbut").removeClass('selected');
	$("#subsbut").addClass('selected');
	$("#Feed").removeClass('open');
	$("#Subs").addClass('open');
}




//!!!! onload.js


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



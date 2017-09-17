
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

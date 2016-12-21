
function hovermsq(msg) {
	shadeOn('hoverhide');
	$("#holdoverscreen").html("<div>"+msg+"</div>");
	$("#holdoverscreen").addClass("showit");
}
function hoverhide() {
	onOffShade = '';
	shadeOff();
	$("#holdoverscreen").removeClass("showit");
}

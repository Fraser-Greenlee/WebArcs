/*jshint multistr: true */

var opening = false;
function moreOptions(nm,params) {
	setTimeout(function() { openOptions(); }, 1200);
}

function openOptions(nm,params) {
	if ($('#authform').length === 0) {
		$('#main').append('\
			<div id="authform"">\
			<h1>Pin this to my feed.</h1>\
			</div>');
		shadeOn('closeauth');
	}
}

function closeOptions() {
	$('#authform').remove();
	shadeOff();
}

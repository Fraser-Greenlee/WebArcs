
var onOffShade = '';

function shadeOn(fnCall) {
	$('#shadecover').css('display','block');
	onOffShade = fnCall;
	stopbodyscrolling();
}

/*
	Can send a string to the functions in regular format;
	name('var')
*/
function shadeOff(opt) {
	if (opt !== undefined && onOffShade !== '') {
		if (onOffShade.indexOf('(') > -1) {
			onOffShade = onOffShade.split('(');
			window[onOffShade[0]](onOffShade[1].substr(1,onOffShade[1].length-3));
		} else {
			window[onOffShade]();
		}
		onOffShade = '';
	}
	startbodyscrolling();
	$('#shadecover').attr('style','');
}

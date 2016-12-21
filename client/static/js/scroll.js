/*jshint multistr: true */

function onscroll() {
	if (page in loading && loading[page][0] === false && loading[page][1] != -1 && $(window).scrollTop() > ($(document).height() - $(window).height()) - 300) {
		getfeed(page, mergObj(gparams[page], {'more':loading[page][1]})  );
	}
}

$(window).scroll(function() {
	if ($(window).scrollTop() >= 0) {
	    onscroll();
	}
});

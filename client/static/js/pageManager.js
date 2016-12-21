
var scrollpages = {};

function setpage(name) {
	if (page != name) {
		scrollpages[page] = $(window).scrollTop();
		onclose(page);
		onopen(name);
		if (name in scrollpages) {
			$(window).scrollTop(scrollpages[name]);
		}

	} else {
		clearfilters();
		resetpage();
	}
}
function onopen(name) {
	page = name;
	ChangeGetParam('page', page);
    $("#icon"+name).attr('class', "on");
    $("#"+name+"page").attr('class',"active");
	$('body').addClass(name);

	if (['feed','sites','new'].indexOf(name) > -1) {
		if (name == 'sites') {
			if ($("#"+page+"page").html() === '') {
				$("#"+page+"page").html(LikDisStarbars);
			}
		}
		viewfeed(name, {});

	} else if (['login','signup'].indexOf(name) > -1) {
		if (name == 'login') {
			loginform();
		} else {
			signupform();
		}

	} else if (['more','search'].indexOf(name) > -1) {
		if ($("#"+name+"page").html() === '') {
			$("#"+name+"page").html(window[name+"Statichtml"]());
		}

	}
}
function onclose(name) {
	$("#icon"+name).attr('class', "");
    $("#"+name+"page").attr('class', "");
	$('body').removeClass(name);
}

function resetpage() {
	if (page in gajax) {
		gajax[page].abort();
	}
	$("#"+page+"page").html('');
    refreshing = true;
    onopen(page);
}

function temporypage(nm) {
	lastpage = page;
	page = nm;
	gparams[nm] = {};
	$("#pages > div").removeClass('active');
	if ($("#side").css('display') != 'none') {
		sideOff();
	}
	if ($("#"+nm+"page").length === 0) {
		$('#pages').append('<div id="'+nm+'page" class="active"></div>');
	} else {
		$("#"+nm+"page").html('').addClass('active');
	}
}

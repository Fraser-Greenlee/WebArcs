
var refreshing = false,
    loading = {};
feedpages.forEach(function functionName(fname) {
    loading[fname] = [false,0];
});

function addGloabalParams(feed, params) {
    if (feed in gparams && jQuery.isEmptyObject(gparams.feed) === false) {
        $.extend(params, gparams.feed);
    }
    return params;
}

function minsdiff(after,before) {
    var diffMs = (after - before);
    return Math.round((diffMs % 86400000) / 3600000)*60 + Math.round(((diffMs % 86400000) % 3600000) / 60000);
}

var lastupdated = {};
function viewfeed(feed, params) {
    if ( refreshing || !(page in lastupdated) || minsdiff(Date(),lastupdated[page]) > 10) {
        refreshing = false;
		loading[feed][1] = 1;
        getfeed(feed, params);
    }
}

function getfeed(feed, params, resetfeed) {
	resetfeed = (typeof resetfeed === 'undefined') ? true : resetfeed;
	params = (typeof params === 'undefined') ? {} : params;

	if ( $("#"+feed+"page #loading").length === 0 ) {
		if (resetfeed) {
			$("#"+feed+"page").append(loadingicon);
		}
	    params = addGloabalParams(feed, params);
		if (feed in gajax) {
			gajax[feed].abort();
		}
	    gajax[feed] = $.ajax({
	        type: 'POST',
	        url: "f/parsers/"+feed,
	        async: true,
	        data: params,
	        success:
				function (html) {
					if (html == 'None') {
						return false;
					}
					if (resetfeed) {
						$("#"+feed+"page #loading").remove();
					}
					loading[feed][1] += 1;
					if (resetfeed) {
						$("#"+feed+"page").append(html);
					} else {
						$("#"+feed+"page").html(html);
					}
					if (feed == 'feed' && 'more' in params === false) {
						filterfeedorder();
					}
					if (html.substr(0,6) == '<end/>') {
						loading[page][1] = -1;
					}
					lastupdated[feed] = Date();
					// incase page hieght is smaller than window
					if (loading[page][1] != -1 && $(document).height() - 10 < $(window).height()) {
						loading[page][1] += 1;
						getfeed(page, {'more':loading[page][1]});
					}
			}
	    });
	}
}

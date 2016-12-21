/* esversion: 6 */

var stdfilters = ['news','video','writing','podcasts','other','reporting'],
	filtertemp = `
		<div class="f$type ftype filter" onclick="filtertype( this, '$type' )">
			<img src="static/images/svg/$type.svg">
			<span>$type</span>
		</div>`;

function clearfilters() {
    $('.filter').removeClass('selected');
	$('body').removeClass('filtering');
    gparams.feed = {};
}

function filtertype(e,type) {
	if (e == -1) {
		e = $('.f'+type);
	}
	$('.contentopenbox').removeClass('hide');
    if ('filter' in gparams.feed === false || type != gparams.feed.filter) {
        $('.filter').removeClass('selected');
        $(e).addClass('selected');
		$('body').addClass('filtering');
        gparams.feed.filter = type;
		$('.contentopenbox:not(.has'+type+')').addClass('hide');
		loading[page][1] = 1;
		onscroll();
    } else {
        $(e).removeClass('selected');
		$('body').removeClass('filtering');
        delete gparams.feed.filter;
    }
}

function showfilter() {
	$('#filterbar').css('top','44px');
}

function filterfeedorder() {
	var addedfilters = [];
	var notsubedfilters = stdfilters;
	var filterbarhtml = "";
	$("#"+page+"page .contentopenbox").each(
		function () {
			var nm = "";
			var classes = $(this).attr('class').split(' ');
			classes.forEach(function(classnm) {
				if (classnm.substr(0,3) == 'has') {
					nm = classnm.substr(3);
				}
			});
			if (addedfilters.indexOf(nm) == -1) {
				filterbarhtml += temp(filtertemp,{'type':nm});
			}
			addedfilters.push(nm);
			if (notsubedfilters.indexOf(nm) > -1) {
				delete notsubedfilters[notsubedfilters.indexOf(nm)];
			}
		}
	);
	notsubedfilters.forEach(function(nm) {
		filterbarhtml += temp(filtertemp,{'type':nm});
	});
	$("#filterseg").html(filterbarhtml);
}

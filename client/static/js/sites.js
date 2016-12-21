/*jshint multistr: true */

var LikDisStarbars = `
    <span class="feedbarlink" onclick="openEntry('like')">
        <img src="static/images/like.png" class="buticon"> likes
    </span>
    <span class="feedbarlink" onclick="openEntry('star')">
        <img src="static/images/star.png" class="favouriteicon buticon"> star
    </span>
    <span class="feedbarlink" onclick="openEntry('history')">
        <img src="static/images/history.png" class="favouriteicon buticon"> history
    </span>`;

function openSite(e,id,name) {
	if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();

	ChangeGetParam('hubid',id);
	ChangeGetParam('hubname',name);
    $('#sitebar').remove();
    $('#filterbar').attr('class','off disabled');

	temporypage('site');
	gparams.site = {'id':id};

	if ($("#sub_"+id).length > 0 && $("#sub_"+id).hasClass('Subscribed')) {
		sub = 'Subscribed';
	} else {
		sub = 'Subscribe';
	}

    $('#head').append('\
        <div id="sitebar" class="topsitebar" data-id="'+id+'">\
            <div id="closesite" onclick="closeSite()"></div><span class="nameholder">'+name+'</span><button id="sub_'+id+'" class="subscribe '+sub+'" onclick="subscribe('+id+')">'+sub+'</button>\
        </div>\
    ');
	$("#sitepage").html($(".feedpostsbar#"+id+" .postsbar").html());
	// do not empty feed
    getfeed('site', gparams.site, false);
    setTimeout(
    	function() {
        	$('#sitebar').css('bottom','0px');
    	},
		10
	);

	return false;
}

function openFromUrl(e,id) {
	if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();

	$('#sitebar').remove();
	$('#filterbar').attr('class','off disabled');

	temporypage('site');

	var name = $('#'+id+'.feedpostsbar .nameholder').html().replace(RegExp('<.*?>'),''),
		url = $('#'+id+'.feedpostsbar').attr('data-url');
    $('#head').append('\
        <div id="sitebar" class="topsitebar" data-id="'+id+'">\
			<div id="closesite" onclick="closeSite()"></div><span class="nameholder">'+name+'</span><button id="sub_'+id+'" class="subscribe Subscribe" onclick="subscribe('+url+')">Subscribe</button>\
        </div>\
    ');
	$("#sitepage").html($(".feedpostsbar#"+id+" .postsbar").html());
	setTimeout(
    	function() {
        	$('#sitebar').css('bottom','0px');
    	},
		10
	);
	return false;
}

function closeSite() {
	page = lastpage;
	removeGetParam('hubid');
	removeGetParam('hubname');
    $('#sitebar').remove();
    $('#sitepage').remove();
    $('#filterbar').attr('class','off');
	$("#pages > div").removeClass('active');
    $('#'+page+'page').attr('class','active');
}

var plural = {
	'like':'likes',
	'star':'starred',
	'history':'history'
};
function openEntry(nm) {
	temporypage('marked');
	gparams.marked = {'type':nm};

    $('#sitebar').remove();
    $('#filterbar').attr('class','off disabled');

    $('#head').append('\
        <div id="sitebar" class="topsitebar">\
            <div id="closesite" onclick="closeSite()"></div><span class="nameholder">'+plural[nm]+'</span>\
        </div>\
    ');
    getfeed('marked', gparams.marked);
    setTimeout(
    	function() {
        	$('#sitebar').css('bottom','0px');
    	},
		10
	);
}

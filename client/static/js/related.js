/*jshint multistr: true */

function getlinkdata(url,id) {
	return {
        'title':$("#postbox_"+id).attr('data-title'),
        'url':url,
        'id':id,
        'date':$("#postbox_"+id).attr('data-date'),
        'clickcount':$("#postbox_"+id).attr('data-clickcount'),
        'like':$("#postbox_"+id).attr('data-like'),
        'dislike':$("#postbox_"+id).attr('data-dislike'),
		'comments':$("#postbox_"+id).attr('data-comments'),

        'siteid':$("#postbox_"+id).attr('data-site-id'),
        'sitename':$("#postbox_"+id).attr('data-site-name'),
        'siteurl':$("#postbox_"+id).attr('data-site-url'),
        'sitehueangle':$("#postbox_"+id).attr('data-site-hueangle')
    };
}

function link(url,id) {
	$("#postbox_"+id).removeClass("bigview");
    var styles = $('#responcebar_'+id+' div').attr('style');
    var d = getlinkdata(url,id);
    $("#postbox_"+id).addClass('visited');
    openrelated(d);
}

function openrelated(d) {
	$('#relpages #relpage.closed').removeClass('closed');
	$('#relforward').attr('class','off');
	if ($('#relpages #relpage:not(.closed)').length > 0) {
		$('#relback').attr('class','on');
	} else {
		$('#relback').attr('class','off');
	}

    for (var id in ['side','related']) {
        if ($('#'+id).attr('class') == id+'off') {
            $('#'+id).attr('class','');
        }
    }
	stopbodyscrolling();
	var comments = '';
	if (d.comments === false || d.comments === null|| d.comments === '') {
		comments = '<span class="relbut comments" id="commenthold'+d.id+'" onclick="opencomments('+d.id+')"></span>';
	} else {
		comments = '<a class="relbut comments" href="'+d.comments+'" target="_blank"></a>';
	}

	var extralink = '';
	if (d.id == 18) {
		extralink = '\
			<div id="sitebar">\
				<span id="sitename" onclick=""><img src="http://www.google.com/s2/favicons?domain_url='+d.url+'"/> '+d.url.substr(23,'r/'+d.urlsubstr(25).indexOf('/'))+'</span><button class="add" id="add_'+d.siteid+'" onclick="subscribe('+d.siteid+')">Add</button>\
		    </div>';
	}

    $('#relpages').append('\
    <div id="relpage" class="rid'+d.id+'" onscroll="styleUiBar()">\
        <a class="title" href="http://webarcs.com/link/'+d.id+'" target="_blank">'+d.title+'</a>\
        <p>'+d.clickcount+' views</p>\
        <div class="respondbar">\
			'+comments+'\
            <span class="thumbtxt" id="likehold'+d.id+'"><div class="butlike thumb relbut" onclick="respond('+d.id+',\'like\')"></div><span>'+d.like+'</span></span>\
            <span class="thumbtxt" id="dislikehold'+d.id+'"><div class="butdislike thumb relbut" onclick="respond('+d.id+',\'dislike\')"></div><span>'+d.dislike+'</span></span>\
            <div class="butstar relbut" id="starhold'+d.id+'" onclick="respond('+d.id+',\'star\')"></div>\
            <div class="butshare relbut" onclick="share(\''+d.url+'\')"></div>\
        </div>\
		'+extralink+'\
        <div id="sitebar">\
            <span id="sitename" onclick="sideOff();openSite('+d.siteid+',\''+d.sitename+'\')"><img src="http://www.google.com/s2/favicons?domain_url='+d.siteurl+'"/> '+d.sitename+'</span><button class="subscribe" id="sub_'+d.siteid+'" onclick="subscribe('+d.siteid+')">Subscribe</button>\
        </div>\
		<div id="commentbox" class="shut">\
			<span>Comming Soon</span>\
		</div>\
        <div id="relatedposts">\
            <div id="loading"></div>\
        </div>\
    </div>\
    ');
    if($("#side").css('display') == 'none') {
        sideOn();
    }
    // close all backed out of pages
    $('#relpages .closed').remove();
    $.post("f/parsers/related", {'id':d.id},
        function (html) {
            $("#relatedposts #loading").remove();
            $("#relpage #relatedposts").last().append(html);
    });
	$('#related').scrollTop(0);
	$('#uibar').removeClass('active');
}

function sideOff() {
    shadeOff();
	$("#side").css('display','none');
	$("#pages").attr('class','');
	$("#related").css('left','');
	startbodyscrolling();
}
function sideOn() {
    $("#side").css('display','');
    $("#pages").attr('class','mainWidth');
}

function styleUiBar() {
    if ($("#relpages #relpage:not(.closed)").last().scrollTop() > 6) {
        $("#uibar").attr('class','active');
    } else if ($("#uibar").attr('class') == 'active') {
        $("#uibar").attr('class','');
    }
}

function stopbodyscrolling() {
    $("body").css('overflow','hidden');
}
function startbodyscrolling() {
    $("body").css('overflow','');
}



//!!!! globals.js

/*jshint multistr: true */

function mergObj(a,b) {
	var c = {};
    for (var k in a) { c[k] = a[k]; }
    for (var k in b) { c[k] = b[k]; }
    return c;
}

function OpenInNewTab(url) {
	event.stopPropagation();
	var win = window.open(url, '_blank');
	win.focus();
}

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

function temp(tmp,ob) {
	var res = tmp;
	for (var k in ob) {
		res = res.replaceAll( "$"+k, ob[k] );
	}
	return res;
}

// html vars
var loadingicon = '<div id="loading"></div>';

// global page vars
var page = 'new',
	lastpage = 'new';

var feedpages = ['new','feed','sites','site','marked'],
    gparams = {
        'new':{},
        'feed':{},
        'sites':{},
		'marked':{}
    },

	gajax = {};




//!!!! accounts.js

/*jshint multistr: true */

var phoneloginid = '';

function logout() {
    $.ajax({
        type: 'POST',
        url: 'f/loginout/logout',
        async:false,
        data: {},
        success:
            function (returnedData) {
                location.reload();
            }
    });
}

function checkmail() {
    $.ajax({
        type: 'POST',
        url: 'f/parsers/checkmail',
        async:false,
        data:   {
                'e':$('#signuppage #email').val()
            },
        success:
            function (returnedData) {
                if (returnedData == 'True') {
                    $('#signuppage #email').attr('class', "True");
                } else {
                    $('#signuppage #email').attr('class', "False");
                    $('#signuppage #errorstatus').html(returnedData);
                }
            }
    });
}

function signup() {
    if($('#signuppage #password1').val() != $('#signuppage #password2').val()) {
        $('#signuppage #errorstatus').html("Passwords do not match.");
    }
    $("#signuppage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/editors/signup',
        async: true,
        data:   {
                'e':$('#signuppage #email').val(),
                'p':$('#signuppage #password1').val(),
				'loginid':phoneloginid
            },
        success:
            function (returnedData) {
				console.log(returnedData);
                if(returnedData == 'True') {
                    location.reload();
                } else {
                    $('#signuppage #errorstatus').html(returnedData);
                    $("#signuppage button").attr('class','');
                }
            }
    });
}

function login() {
    if (page != 'login') {
        return false;
    }
    $("#loginpage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/loginout/login',
        async: true,
        data:   {
                'e':$('#loginpage #email').val(),
                'p':$('#loginpage #password').val(),
				'loginid':phoneloginid
            },
        success:
            function (returnedData) {
                if (returnedData != '0' && !isNaN(returnedData)) {
                    location.reload();
                } else {
                    $("#loginpage button").attr('class','');
                    if (returnedData == '0') {
                        $('#loginpage #errorstatus').html("login failed");
                    } else {
                        $('#loginpage #errorstatus').html(returnedData);
                    }
                }
            }
    });
}

function resetpass() {
	if (page != 'login') {
        return false;
    }
	$("#loginpage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/editors/newpass',
        async: true,
        data:   {
                'e':$('#loginpage #email').val(),
            },
        success:
            function (returnedData) {
                if (returnedData == 'v') {
					$('#loginpage').html(
				        '<div class="form">\
				            <img src="static/images/loading.png">\
				            <h2>Sent</h2>\
							<span>Check your email for a reset password request.</span>\
				        </div>');
                } else {
					$("#loginpage button").attr('class','');
	                if (returnedData == '0') {
	                    $('#loginpage #errorstatus').html("login failed");
	                } else {
	                    $('#loginpage #errorstatus').html(returnedData);
	                }
                }
            }
    });
}

function forgotpass() {
	if (page != 'login') {
        return false;
    }
    $("#loginpage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/editors/forgotpass',
        async: true,
        data:   {
                'e':$('#loginpage #email').val(),
            },
        success:
            function (returnedData) {
                if (returnedData == 'v') {
					$('#loginpage').html(
				        '<div class="form">\
				            <img src="static/images/loading.png">\
				            <h2>Sent</h2>\
							<span>Check your email for a reset password request.</span>\
				        </div>');
                } else {
					$("#loginpage button").attr('class','');
	                if (returnedData == '0') {
	                    returnedData = "incorrect address";
	                }
					$('#loginpage #errorstatus').html(returnedData);
                }
            }
    });
}

function resetpass() {
	if (page != 'login') {
        return false;
    }
	$("#loginpage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/editors/newpass',
        async:false,
        data:   {
                'p':$('#loginpage #password').val(),
				'key':urlvars.resetpass,
				'id':urlvars.id
            },
        success:
            function (returnedData) {
                if (returnedData == 'v') {
					$('#loginpage').html(
				        '<div class="form">\
				            <img src="static/images/loading.png">\
				            <h2>Done</h2>\
							<span>You can now login with your new password.</span>\
				        </div>');
                } else {
					$("#loginpage button").attr('class','');
	                if (returnedData == '0') {
	                    returnedData = "bad password";
	                }
	                $('#loginpage #errorstatus').html(returnedData);
                }
            }
    });
}

function forgotpassform() {
    $('#loginpage').html(
        '<div class="form">\
            <img src="static/images/loading.png">\
            <h2>forgot password</h2>\
            <span id="errorstatus"></span>\
            <div>\
                <span>email</span> <input id="email" type="email" placeholder="email">\
            </div>\
            <button onmousedown="forgotpass()">Send</button><span class="forgotpass" onclick="loginform()">back</span>\
        </div>'
    );
}
function resetpassform() {
	$('#loginpage').html(
        '<div class="form">\
            <img src="static/images/loading.png">\
            <h2>reset password</h2>\
            <span id="errorstatus"></span>\
            <div>\
                <span>password</span> <input id="password" type="password" placeholder="password">\
            </div>\
            <button onmousedown="resetpass()">Send</button><span class="forgotpass" onclick="loginform()">back</span>\
        </div>'
    );
}
function loginform() {
    $('#loginpage').html(
        '<div class="form">\
            <img src="static/images/loading.png">\
            <h2>Login</h2>\
            <span id="errorstatus"></span>\
            <div>\
                <span>email</span> <input id="email" type="email" placeholder="email">\
            </div>\
            <div>\
                <span>password</span> <input id="password" type="password" placeholder="password">\
            </div>\
            <button onmousedown="login()">Login</button><span class="forgotpass" onclick="forgotpassform()">forgot password</span>\
        </div>'
    );
}
function signupform() {
    $('#signuppage').html(
        '<div class="form">\
            <img src="static/images/loading.png">\
            <h2>Signup</h2>\
            <span id="errorstatus"></span>\
            <div>\
                <span>email</span> <input id="email" type="email" placeholder="email" onblur="checkmail()">\
            </div>\
            <div>\
                <span>password</span> <input id="password1" type="password" placeholder="password">\
            </div>\
            <div>\
                <span>confirm password</span> <input id="password2" type="password" placeholder="confirm password">\
            </div>\
            <button onmousedown="signup()">Signup</button>\
        </div>'
    );
}




//!!!! addsites.js

/*jshint multistr: true */

var addforms = {

	'twitter':'\
		<h2><img src="static/images/sites/twitter.png">Add your twitter follows.</h2>\
		<span>@<input type="text" placeholder="Your Username"></span>\
		<button onclick="addtwitter()">Submit</button><button class="cancel" onclick="closeauth()">Cancel</button>',

	'opml':'\
		<form method="POST" enctype="multipart/form-data" action="fs/api/xmlfeeds">\
			<h1>Upload OPML file.</h1>\
			<input type="file" name="myfile" />\
			<br/>\
			<input type="submit" />\
		</form>\
		<button class="cancel outside" onclick="closeauth()">Cancel</button>'
};

function connectsite(site) {
	if ($('#authform').length === 0) {
		$('#main').append('<div id="authform" class="'+site+'">'+addforms[site]+'</div>');
		shadeOn('closeauth');
	}
}

function closeauth() {
	$('#authform').remove();
	shadeOff();
}

function addtwitter() {
	if ($('#authform').length !== 0 && $('#authform input')[0].value !== "") {
		$.ajax({
	        type: 'POST',
	        url: 'f/api/twitter/getuserfriends',
	        async: true,
	        data: {'name':$('#authform input')[0].value},
	        success:
	            function (returnedData) {
	            	console.log(returnedData);
					$('#authform').remove();
	            }
	    });
	}
}

function addnewfeed(e) {
	$(e).addClass('loading');
	$.ajax({
        type: 'POST',
        url: 'f/addfeed/add',
        async: true,
        data: {'id':$(e).attr('data-id')},
        success:
            function (returnedData) {
				if (returnedData == 'v') {
					closesearch();
					notifyshow('Added to your feeds.');
					$(e).html('Added');
				} else {
					$(e).addClass('error');
					$(e).html(returnedData);
				}
            }
    });
}

function addurlfeed(e) {
	$(e).addClass('loading');
	$.ajax({
        type: 'POST',
        url: 'f/addfeed/add',
        async: true,
        data: {'url':$(e).attr('data-url')},
        success:
            function (returnedData) {
				if (returnedData == 'v') {
					closesearch();
					notifyshow('Added to your feeds.');
					$(e).html('Added');
				} else {
					$(e).addClass('error');
					$(e).html(returnedData);
				}
            }
    });
}




//!!!! feedback.js

/*jshint multistr: true */

function getfeedback() {
	if (userid === "") {
		hovermsq("\
			<h1>Hi there we'd love to hear what you think WebArcs.</h1>\
			<p>\
				WebArcs is super new and it will be shaped by your feedback.<br>\
				You can get in touch by signing up and comming back here.\
			</p>\
		");
	} else {
		hovermsq("\
			<h1>Hi there we'd love to hear what you think of WebArcs.</h1>\
			<p>\
				We'll be sending you an email for feedback soon but until then you can message us on twitter <a href='https://twitter.com/FraserGreenlee' target='_blank'>@WebArcs</a>\
			</p>\
		");
	}
}




//!!!! feedmanager.js


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




//!!!! filterBar.js

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




//!!!! functions.js


function stopPropagation(e) {
	if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();
	e.preventDefault();
	return false;
}

function subscribe(inp,e) {
	if (e !== undefined) {
		if (!e) var e = window.event;
	    e.cancelBubble = true;
	    if (e.stopPropagation) e.stopPropagation();
		e.preventDefault();
	}

	if (userid == "0") {
		notifyshow('To Subscribe <button class="loglink" onclick="setpage(\'signup\')">Signup</button>');
	} else {

		console.log('Subscribe: '+inp);

		var urltype = inp[0] == 'h';
		if (urltype) {
			var data = {
					'url':inp
				};
		} else {
			var data = {
					'id':inp
				};
		}
		if (urltype) {
			id = $('*[data-url="'+inp+'"]')[0].id;
		} else {
			id = inp;
		}
		$("#sub_"+id).attr('class','subscribe loading');
		$.ajax({
			type: 'POST',
			url: 'f/editors/subscribe',
			async: true,
			data: data,
			success:
				function (returnedData) {
					subscribeRet(id,returnedData);
				}
		});
	}
	return false;
}
function subscribeRet(id,returnedData) {
	if (returnedData == 'subscribed') {
		$("#sub_"+id)
			.html("Subscribed")
			.attr('class','subscribe off Subscribed');
		$(".feedpostsbar#"+id).removeClass('unsubbed');
	} else if (returnedData == 'unsubscribed') {
		$("#sub_"+id)
			.html("Subscribe")
			.attr('class','subscribe Subscribe');
		$(".feedpostsbar#"+id).addClass('unsubbed');
	} else {
		console.log('error, '+returnedData);
	}
}

function notifyshow(msg) {
	$("#notification").html(msg);
	$("#notification").addClass('showing');
}
function notifyhide() {
	$('#notification').removeClass('showing');
}




//!!!! getstarted.js

/*jshint multistr: true */

function getstarted() {
	var feed = page;
	if (feed in gajax) {
		gajax[feed].abort();
	}
	$("#feedpage").append(loading);
	gajax[feed] = $.ajax({
		type: 'POST',
		url: "f/parsers/displaybars",
		async: true,
		success:
			function (html) {
				$("#feedpage #loading").remove();
				$("#feedpage").append('\
				<div class="msgbox">\
					<h1>Add Sites Below</h1>\
					<p>These will appear in your feed.</p>\
				</div>\
				'+html);
			}
	});
}




//!!!! getvarhandeling.js


function joinInnerArray(r,j) {
    for(var i=0;i<r.length;i++) {
        r[i] = r[i].join(j);
    }
    return r;
}

function getUrlVars() {
	var GETvars = {}, hash;
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	for (var i = 0; i < hashes.length; i++) {
	    hash = hashes[i].split('=');
	    GETvars[hash[0]] = hash[1];
	}
    return GETvars;
}

function ChangeGetParam(param,val) {
    url = window.location.href;
    if(location.hash.length > 0) {
        url = url.slice(0,-location.hash.length);
    }
    url = url.split('?');
    if(url.length == 2) {
        var setGetVar = false;
        url[1] = url[1].split('&');
        for(var i=0;i<url[1].length;i++) {
            url[1][i] = url[1][i].split('=');
            if(url[1][i][0] == param) {
                url[1][i][1] = val;
                setGetVar = true;
            }
        }
        if(!setGetVar) {
            url[1].push([param,val]);
        }
        url = url[0]+'?'+joinInnerArray(url[1],'=').join('&');
    } else if(url.length == 1) {
        url = url[0]+'?'+param+'='+val;
    } else {//  bad url, reset it
        url = '?page='+CurrentPage;
    }
    window.history.pushState({},val, url);
}

function removeGetParam(param) {
	url = window.location.href;
    if(location.hash.length > 0) {
        url = url.slice(0,-location.hash.length);
    }
    url = url.split('?');
    if(url.length == 2) {
		var spliceAt = -1;
        url[1] = url[1].split('&');
        for(var i=0;i<url[1].length;i++) {
            url[1][i] = url[1][i].split('=');
            if(url[1][i][0] == param) {
				spliceAt = i;
            }
        }
		if (spliceAt > -1) {
			url[1].splice(spliceAt,1);
		}
        url = url[0]+'?'+joinInnerArray(url[1],'=').join('&');
    } else if(url.length == 1) {
        url = url[0]+'?';
    } else {//  bad url, reset it
        url = '?page='+CurrentPage;
    }
    window.history.pushState({},'Open Site', url);
}




//!!!! hovermsg.js


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




//!!!! moreoptions.js

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




//!!!! morePage.js



function moreStatichtml() {
	if (userid == '0') {
		return `
			<ol>
				<li>Signup to access extra features.</li>
			</ol>
		`;
	} else {
		return `
			<ol>
				<li onclick="connectsite('twitter')"><img src="static/images/sites/twitter.png">Connect</li>
				<li onclick="connectsite('opml')">Upload OPML File</li>
				<li onclick="logout()">Logout</li>
			</ol>
		`;
	}
}




//!!!! pageManager.js


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




//!!!! related.js

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




//!!!! relatedwindow.js


function pageback() {
	if ($('#relpages #relpage:not(.closed)').length > 1) {
		$('#relpages #relpage:not(.closed)').last().addClass('closed');
		$('#relforward').attr('class','on');
		$('#related').scrollTop(0);
		if ($('#relpages #relpage:not(.closed)').length < 2) {
			$('#relback').attr('class','off');
		}
	}
}
function pageforward() {
	if ($('#relpages #relpage.closed').length > 0) {
		$('#relpages #relpage.closed').last().removeClass('closed');
		$('#relback').attr('class','on');
		$('#related').scrollTop(0);
		if ($('#relpages #relpage.closed').length === 0) {
			$('#relforward').attr('class','off');
		}
	}
}




//!!!! respond.js


function respond(id,responce) {
	if ($("#"+responce+"hold"+id).hasClass('voted')) {
		$("#"+responce+"hold"+id).removeClass('voted');
	} else {
		$("#"+responce+"hold"+id).addClass('voted');
	}
	$.post(
		"f/editors/respond",
		{
			'id':id,
			'responce':responce
		},
		function (msg) {
			console.log('msg,');
			console.log(msg);
			if (msg == 'inserted') {
				if ($("#"+responce+"hold"+id).hasClass('voted') === false) {
					$("#"+responce+"hold"+id).addClass('voted');
				}
				if (['like','dislike'].indexOf(responce) > -1) {
					if (responce == 'like') {
						$("#likehold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())+1);
						if ($("#dislikehold"+id).hasClass('voted')) {
							$("#dislikehold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())-1);
							$("#dislikehold"+id).removeClass('voted');
						}
					} else {
						$("#dislikehold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())+1);
						if ($("#likehold"+id).hasClass('voted')) {
							$("#likehold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())-1);
							$("#likehold"+id).removeClass('voted');
						}
					}
				}
			} else {
				if ($("#"+responce+"hold"+id).hasClass('voted')) {
					$("#"+responce+"hold"+id).removeClass('voted');
				}
				if (['like','dislike'].indexOf(responce) > -1) {
					$("#"+responce+"hold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())-1);
				}
			}
		}
	);
}

function opencomments(id) {
	if ($(".rid"+id+" #commentbox").hasClass("shut")) {
		$(".rid"+id+" #commentbox").removeClass("shut");
	} else {
		$(".rid"+id+" #commentbox").addClass("shut");
	}
}

function share(url) {
	hovermsq('<span>'+url+'<span>');
}




//!!!! scroll.js

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




//!!!! searchPage.js

/*jshint multistr: true */

function searchStatichtml() {
	searchTimeOut = setTimeout(function() {
		$("#searchinput").focus();
	}, 600);
	return `
	<div id="searchform" class="empty">
		<input id="searchinput" placeholder="Enter feed name." type="text" oninput="searchHandler()" autocomplete="off" tabindex="1" value="" autocapitalize="off" autocorrect="off"><div id="searchcross" onclick="clearsearch()"></div><div id="searchenter" onclick="search()"></div>
	</div>
	<div id="searchresults"></div>
	`;
}

function search() {
	searchQuery($("#searchinput")[0].value);
}

$( window ).keypress(function(event) {
    if (event.which == 47) {
        $("#searchinput").focus();
    }
});

var lastq = "",
	searchTimeOut;

function searchHandler() {
	clearTimeout(searchTimeOut);
	var q = $("#searchinput")[0].value;
	if (q === "") {
		clearsearch();
		return false;
	}
	$("#searchform").removeClass('empty');
	searchTimeOut = setTimeout(function() {
		var q = $("#searchinput")[0].value;
		if (q != lastq) {
			searchQuery(q);
		}
		lastq = q;
	}, 950);
}

function searchQuery(q) {
	$("#searchresults").html(loadingicon);
	$.ajax({
		type: 'POST',
		url: 'f/generalweb/search',
		async: true,
		data: {'q':q},
		success:
			function (returnedData) {
				$("#searchresults").html(returnedData);
				$(".feedpostsbar[data-loadposts='True']").each(function(i,e) {
					loadposts(e.id,e.getAttribute('data-url'));
				});
			}
	});
}

function loadposts(id,url) {
	$('.feedpostsbar#'+id+' .postsbar').html(loadingicon);
	$.ajax({
		type: 'POST',
		url: 'f/generalweb/posts',
		async: true,
		data: {'url':url},
		success:
			function (returnedData) {
				if (returnedData == 'False') {
					$('.feedpostsbar#'+id).remove();
				} else {
					data = JSON.parse(returnedData);
					$(".feedpostsbar#"+id+" .nameholder").html('<img src="http://www.google.com/s2/favicons?domain_url='+data.url+'">'+data.name);
					$('.feedpostsbar#'+id+' .postsbar').html(data.posts);
					if (data.viewtype !== '') {
						$('.feedpostsbar#'+id).addClass(data.viewtype);
					}
					if (data.Subscribed) {
						$(".feedpostsbar#"+id+" .subscribe").removeClass('Subscribe');
						$(".feedpostsbar#"+id+" .subscribe").addClass('Subscribed');
						$(".feedpostsbar#"+id+" .subscribe").html('Subscribed');
					}
				}
			}
	});
}

function clearsearch() {
	$("#searchinput").val('');
	$("#searchform").addClass('empty');
	$("#searchresults").html('');
	$("#searchinput").focus();
}




//!!!! shade.js


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




//!!!! sites.js

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




//!!!! tools.js


String.prototype.capFirst = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

function replaceList(str,replist){
	var evenkeys = Array.apply(null, Array(replist.length/2)).map(function (_, i) {return i*2;});
	evenkeys.forEach(function(even) {
		str = str.replaceAll(replist[even], replist[even+1]);
	});
	return str;
}




//!!!! onload.js

/*jshint multistr: true */

var phoneloginid = "",

	pageSets = {
		'loggedout': [
			'new','login','signup','search','more'
		],
		'loggedin': [
			'new','feed','sites','search','more'
		],
		'loginid': [
			'signup','login'
		]
	};


function openpageset(nm) {
    var c = '';
    $("#pages").empty();
    pageSets[nm].forEach(function(id) {
		if (['login','signup'].indexOf(id) > -1) {
			$("#headoptions").append('<div id="icon'+id+'" style="background-image:url(\'static/images/'+id+'.png\')" onclick="setpage(\''+id+'\')"><button class="loglink">'+id+'</button></div>');
		} else {
			$("#headoptions").append('<div id="icon'+id+'" style="background-image:url(\'static/images/'+id+'.png\')" onclick="setpage(\''+id+'\')">'+id+'</div>');
		}
        $("#pages").append('<div id="'+id+'page"></div>');
    });

	page = urlvars.page;

	if (page !== undefined && pageSets[nm].indexOf(page) > -1) {
		setpage(page);
	} else {
		if (nm == 'loggedin') {
			setpage(pageSets[nm][1]);
		} else {
			setpage(pageSets[nm][0]);
		}
	}
	if ('hubid' in urlvars && 'hubname' in urlvars) {
		console.log(urlvars);
		openSite(urlvars.hubid,unescape(urlvars.hubname));
	}
}

function userlogresp(retid) {
	userid = retid;
	filterfeedorder();
	if (userid == '0') {
		openpageset('loggedout');
		if ('resetpass' in urlvars && 'id' in urlvars) {
			setpage('login');
			resetpassform();
		}
	} else {
		$('body').addClass('loggedin');
		$('#menu').append('\
			<div onclick="connectsite(\'twitter\')"><img src="static/images/sites/twitter.png">Connect</div>\
			<div onclick="connectsite(\'opml\')">Upload OPML File</div>\
			<div onclick="logout()">logout</div>\
		');
		openpageset('loggedin');
	}
}

var udata = {};
var userid = '0';
function onloaded() {
	urlvars = getUrlVars();
	url = window.location.href;
	if (url.indexOf('?') > -1) {
		url = url.substr(0,url.indexOf('?'));
		window.history.pushState({},'new', url);
	}
	if ('loginid' in urlvars && urlvars.loginid != '') {
		phoneloginid = urlvars.loginid;
		udata = {
			'loginid':phoneloginid
		};
	} else {
		udata = {};
	}
	$.ajax({
		type: 'POST',
		url: 'f/loginout/loginstatus',
		async: true,
		data: udata,
		success:
			function (returnedData) {
				if ('loginid' in urlvars && returnedData == 'loginphone') {
					$('body').addClass('expandbars');
					phoneloginid = urlvars.loginid;
					openpageset('loginid');
				} else {
					userlogresp(returnedData);
				}
			}
	});
}
onloaded();



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

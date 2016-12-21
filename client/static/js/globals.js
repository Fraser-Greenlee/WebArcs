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

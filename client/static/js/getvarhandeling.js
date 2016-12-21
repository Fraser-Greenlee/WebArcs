
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
